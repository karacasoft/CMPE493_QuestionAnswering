import re
import math
from operator import itemgetter
import pickle

#-------------------------------------------------------

num2paragraphs = dict()
punctuations = list()
num2vectors = dict()
idf = dict()
question2label = dict()
question2vector = dict()
question2calculated = dict()
full_text = list()

content = open("derlem.txt", encoding='utf-16').read()
paragraphs = re.findall(r'(\d+)\s(.*)', content)
punctuations = open("punctuations.txt").read()

question_groups_file = open("soru_gruplari.txt", encoding='utf-16').read()
question_groups = question_groups_file.split('\n\n')

#-------------------------------------------------------------
# SETUP RELATED FUNCTIONS
def preprocess_text(text):
    text = text.lower()
    for punc in punctuations:
        text = text.replace(punc, ' ')
    return text

def assign_questions_to_answer(questions, answer):
    for question in questions:
        question2label[question] = answer
        
def assign_questions_to_vector(question_pairs):
    for question_num, question_text in question_pairs:
        question_text = preprocess_text(question_text)
        question2vector[question_num] = generate_vector_space(question_text)
      
def generate_vector_space(text):
    text = preprocess_text(text)
    tokens = text.split()
    tf = {i:tokens.count(i) for i in set(tokens)}
    vector = {}
    for term in tf:
        if term in full_text:
            vector[term] = tf[term]
            temp = len(num2paragraphs)/idf[term]
            vector[term] *= math.log(temp)
        else:
            vector[term] = 0
    return vector
def length_vector(vector):
    total = 0
    for dim in vector:
        total += vector[dim]*vector[dim]
    return math.sqrt(total)

def dot_product(vector1, vector2):
    product = 0
    for dim in vector1:
        if dim in vector2:
            product += vector1[dim] * vector2[dim]
    return product

def cosine_similarity(vector1, vector2):
    return dot_product(vector1, vector2) / (length_vector(vector1)*length_vector(vector2))

#-------------------------------------------------------------

for paragraph in paragraphs:
    num = paragraph[0]
    text = paragraph[1]
    text_updated = preprocess_text(text)
    tokens = text_updated.split()
    tokens = list(set(tokens))
    num2paragraphs[num] = text
    for token in tokens:
        if token in idf:
            idf[token] +=1
        else:
            idf[token]=1
    full_text = full_text + tokens

for paragraph in paragraphs:
    num = paragraph[0]
    text = paragraph[1]
    text_updated = preprocess_text(text)
    num2vectors[num] = generate_vector_space(text_updated)

#-----------------------------------------------------------------

for question_group in question_groups:
    question_nums = re.findall(r'^(S\d+):', question_group)
    label = re.search(r'İlintili Paragraf:\s(\d+)', question_group)
    if label:
        label = label.group(1)
        assign_questions_to_answer(question_nums, label)
    questions = re.findall(r'^S\d+:\s(.*)', question_group)
    question_pairs = [(question_nums[i], questions[i]) for i in range(0, len(question_nums))]
    assign_questions_to_vector(question_pairs)

#---------------------------------------------------------------------------
import json 
"""
with open("full_text.json", 'w+') as file:
    file.write('\n'.join(full_text))

with open("num2paragraphs.json", "w+") as file:
    file.write(json.dumps(num2paragraphs))

with open("nums2vector.json", 'w+') as file:
    file.write(json.dumps(num2vectors))

with open('question2vector.json', 'w') as file:
     file.write(json.dumps(question2vector))

with open("question2label.json", "w+") as file:
    file.write(json.dumps(question2label))


"""

#----------------------------------------------------------------------------
# TRAINING THE SUGGESTIONS
for question in question2vector:
    question2calculated[question] = []
    for num in num2vectors:
        score = cosine_similarity(num2vectors[num], question2vector[question])
        question2calculated[question].append((num, score))
    question2calculated[question].sort(key=itemgetter(1), reverse=True)


pickle.dump(num2paragraphs, open("num2paragraphs.pickle", 'wb'))
pickle.dump(num2vectors, open("num2vectors.pickle", 'wb'))
pickle.dump(idf, open("idf.pickle", 'wb'))
pickle.dump(question2label, open("question2label.pickle", 'wb'))
pickle.dump(question2vector, open("question2vector.pickle", 'wb'))
pickle.dump(question2calculated, open("question2calculated.pickle", 'wb'))
pickle.dump(full_text, open("full_text.pickle", 'wb'))

"""    
with open("cosine_scores.json", 'w+') as file:
    file.write(json.dumps(question2calculated))
"""

# RESULTCALCULATION FUNCTIONS
def suggest_k_paragraphs_to_question(question, k):
    return question2calculated[question][0:k]

def suggest_k_paragraphs_to_question_text(question, k):
    question_vector = generate_vector_space(question)
    scores = []
    for num in num2vectors:
        scores.append((num, cosine_similarity(question_vector, num2vectors[num])))
    scores.sort(key=itemgetter(1), reverse=True)
    return scores[0:k]



def calculate_accuracy(k):
    for question in question2calculated:
        if question == 'S2068':
            continue
        q_list = list(map(lambda x: x[0], question2calculated[question]))
        if question2label[question] in q_list[0:k]:
            num_correct += 1
    print("Accuracy for "+k+": "+num_correct/len(question2label))
    return num_correct/len(question2label)

# Several sample questions from the paragraphs

#question = "Altın arama işlemi hangi kimyasal ile yapılmaktadır?"
#question = "Toprak oluşumu nasıl başlar?"
question = "En düşük sıcaklık nerde gözlemlenir?"
print("Suggested answer paragraphs for question: "+question)
print(suggest_k_paragraphs_to_question_text(question, 5))



