import pickle, math
from operator import itemgetter
import os

PICKLE_DIR = "./pickle"

num2paragraphs = pickle.load(open(os.path.join(PICKLE_DIR, "num2paragraphs.pickle"), "rb"))
num2vectors = pickle.load(open(os.path.join(PICKLE_DIR, "num2vectors.pickle"), "rb"))
idf = pickle.load(open(os.path.join(PICKLE_DIR, "idf.pickle"), "rb"))
question2label = pickle.load(open(os.path.join(PICKLE_DIR, "question2label.pickle"), "rb"))
question2vector = pickle.load(open(os.path.join(PICKLE_DIR, "question2vector.pickle"), "rb"))
question2calculated = pickle.load(open(os.path.join(PICKLE_DIR, "question2calculated.pickle"), "rb"))
full_text = pickle.load(open(os.path.join(PICKLE_DIR, "full_text.pickle"), "rb"))

punctuations = open("punctuations.txt").read()

def preprocess_text(text):
    text = text.lower()
    for punc in punctuations:
        text = text.replace(punc, ' ')
    return text

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


def suggest_k_paragraphs_to_question_text(question, k):
    question_vector = generate_vector_space(question)
    scores = []
    for num in num2vectors:
        scores.append((num, cosine_similarity(question_vector, num2vectors[num])))
    scores.sort(key=itemgetter(1), reverse=True)
    return scores[0:k]

question = "En düşük sıcaklık nerde gözlemlenir?"
print("Suggested answer paragraphs for question: "+question)
print(suggest_k_paragraphs_to_question_text(question, 5))
