from zemberek_wrapper import ZemberekMorphologyWrapper

with ZemberekMorphologyWrapper() as morph:
    res = morph.analyze("Ülkemizde bakır yatakları nerelerde bulunmaktadır?")

    print(res)

