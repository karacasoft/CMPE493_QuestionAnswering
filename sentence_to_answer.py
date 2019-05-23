# %%
import re
from zemberek_wrapper import ZemberekMorphologyWrapper


question = "Besin üretme özelliğine sahip olmayan canlılara ne ad verilir"
sentence = "Tüketiciler, besin üretme özelliğine sahip olmayan canlılardır."
expectedAnswer = "Tüketici"

question = "Atlas Okyanusu ile Büyük Okyanusu birbirine bağlayan kanal hangisidir?"
sentence = "Panama Kanalı, Orta Amerika’nın dar bir kesiminde Atlas Okyanusu ile Büyük Okyanusu deniz ulaşımı açısından birbirine bağlar."
expectedAnswer = "Panama Kanalı"

question = "Ülkemizde bakır yatakları nerelerde bulunmaktadır?"
sentence = "Kastamonu’nun Küre, Artvin’in Murgul ve Rize’nin Çayeli ilçelerinde de bakır yatakları bulunmaktadır."
expectedAnswer = "Kastamonu’nun Küre Artvin’in Murgul ve Rize’nin Çayeli ilçeleri"


# %%


def morphString(string):
    with ZemberekMorphologyWrapper() as morph:
        res = morph.analyze(string)
    return res
# %%

def getAnswer(question, sentence):
    answer = []

    lemmasSentence = {}
    lemmasQuestion = {}    
    lemmasAnswer = []  

    question = morphString(question)
    sentence = morphString(sentence)

    for i in range(len(question)):
        try:
            lemma = (question[i]["prop"])
            lemma = re.findall(r'\[(.+)\]', lemma)
            lemmasQuestion[lemma[0]] = question[i]        
        except TypeError:
            lemma = (question[i]["word"])
            lemmasQuestion[lemma] = question[i]

    for i in range(len(sentence)):
        try:
            lemma = (sentence[i]["prop"])
            lemma = re.findall(r'\[(.+)\]', lemma)
            lemmasSentence[lemma[0]] = sentence[i]

        except TypeError:
            lemma = (sentence[i]["word"])
            lemmasSentence[lemma] = sentence[i]


    for lem in lemmasSentence:
        if lem not in lemmasQuestion:

            answer.append(lemmasSentence[lem])

    for i in range(len(answer)):
        lemma = (answer[i]["word"])
        lemmasAnswer.append(lemma)
        
    answerString = ' '.join(lemmasAnswer)
    return answerString

#%%

print("System's answer: ")
print(getAnswer(question, sentence))
print("Expected answer: ")
print(expectedAnswer)

#%%
