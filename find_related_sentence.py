from get_paragraphs import suggest_k_paragraphs_to_question_text, get_paragraph
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import jaccard_distance

def find_related_sentence(question):
    q_words = word_tokenize(question, language='turkish')
    suggested = suggest_k_paragraphs_to_question_text(question, 5)

    sentences = sent_tokenize(get_paragraph(suggested[0][0]), language='turkish')
    highest_score = 0
    highest_score_sent = None
    for sent in sentences:
        sent_words = word_tokenize(sent, language='turkish')
        score = 1 - jaccard_distance(set(q_words), set(sent_words))
        if score > highest_score:
            highest_score = score
            highest_score_sent = sent
    return highest_score_sent, highest_score

print(find_related_sentence("Dünya genelinde bir yıl içinde meydana gelen doğum sayısının toplam nüfusa oranına ne denir?"))
