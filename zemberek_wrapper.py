from subprocess import Popen, PIPE

class ZemberekMorphologyWrapper:

    def __enter__(self):
        process = Popen(["java", "-jar", "zemberek-full.jar", "MorphologyConsole"], stdin=PIPE, stdout=PIPE)
        process.stdout.readline()
        self._process = process
        return self
    
    def analyze(self, sentence):
        process = self._process
        process.stdin.write("{sentence}\n".format(sentence=sentence).encode("UTF-8"))
        process.stdin.flush()

        process.stdout.readline() # new line
        sentence = process.stdout.readline().decode("UTF-8")
        words = []
        word = process.stdout.readline().decode("UTF-8")[:-1]
        while word != "":
            prop = process.stdout.readline().decode("UTF-8")[:-1]
            word_prop = {
                "word" : word,
                "prop" : None
            }
            while prop[:1] == "[":
                if word_prop["prop"] == None:
                    word_prop["prop"] = prop
                if prop[-1:] == "*":
                    word_prop["prop"] = prop[:-1]
                prop = process.stdout.readline().decode("UTF-8")[:-1]
            word = prop
            words.append(word_prop)
        
        return words
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._process.stdin.write("quit\n".encode("UTF-8"))
        self._process.stdin.flush()
