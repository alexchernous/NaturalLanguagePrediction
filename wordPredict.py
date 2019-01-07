import json
import random
import math
from operator import itemgetter
from myParser import StringProcessor

'''
need prediction to be based on weighted random choice not max()

need smoothing for unseen words, so program doesn't stop if you enter words not in model
https://en.wikipedia.org/wiki/N-gram#Smoothing_techniques
'''


class WordPredict:

    def __init__(self, triFile, biFile):
        file = open(f"{triFile}.txt", "r")
        dict_bytes = file.read()
        self.lmTri = json.loads(dict_bytes)
        file = open(f"{biFile}.txt", "r")
        dict_bytes = file.read()
        self.lmBi = json.loads(dict_bytes)

        self.input_hist = []
        self.user_input = ''

    def predict(self):

        #assume the default to be more than 1 word entry and 2nd order markov model has it
        try:
            print("accesing 2nd order markov model")
            lm_bucket = self.lmTri["__TRIGRAM__"][self.user_input[-2]][self.user_input[-1]]

        #catch situation where user gives less than 2 words or model can't find 2nd order markov chain
        except:
            #not in 2nd order markov model
            if len(self.user_input) > 1:
                #fall back to __BIGRAM__ model
                print("accesing 1st order markov model")
                lm_bucket = self.lmBi["__BIGRAM__"][self.user_input[-1]]

            #user string is less than 2 words
            else:
                print("accesing 2nd order markov model, for sentence initial words")
                if not self.user_input[-1] in self.lmTri["__2ndWrd__"].keys():
                    raise ValueError("(except) sentence prediction stumbled upon a word not in the keys", self.user_input[-1])

                lm_bucket = self.lmTri["__2ndWrd__"][self.user_input[-1]]

        # most_prob.. can be instance variable #
        '''
        NEED WEIGHTED RANDOM CHOICE NOT MAX
        '''
        most_probable_choices = [k for k,v in lm_bucket.items() if v == max(lm_bucket.values())]
        print('all choices:', lm_bucket.items() )
        print('most_probable_choices:', most_probable_choices)

        return self.choose(most_probable_choices)


    def choose(self, most_probable_choices):

        next_word = most_probable_choices[0]

        #print('choose (before repeat check):', next_word)

        #repetition check
        # if the __BIGRAM__ already exists..
        if next_word in self.input_hist and self.input_hist[self.input_hist.index(next_word)-1] == self.user_input:
            #print("repetition found")

            '''
            if after repetition there's still only 1 option... might want to remake this though
            '''
            if len(most_probable_choices) < 2:
                next_word = random.choice(list(self.lmTri.keys()))
                print('choose:', next_word)
                return next_word

            return self.handle_repetition(next_word)

        elif len(most_probable_choices) > 1:
            '''
            will probably want to have this not just random but random given a certain POS tag
            but for now it's just random if we have multiple choices with the same prob
            '''
            next_word = random.choice(most_probable_choices)
            print('choose:', next_word)
            return next_word

        print('choose (after repeat check):', next_word)
        return next_word


    def handle_repetition(self, next_word):
        #remove the next word from the list of choices, we want to avoid loop
        # and pass it back to the function
        new_choices = [x for x in self.lmTri[self.user_input].items() if x[0] != next_word]
        print('repeat:', new_choices)

        '''
        NEED WEIGHTED RANDOM CHOICE NOT MAX
        '''
        most_probable_choices = [k for k,v in new_choices if v == max(new_choices,key=itemgetter(1))[1]]
        print('repeat:', most_probable_choices)

        return self.choose(most_probable_choices)


    def runFinish_Predict(self, user_input):
        strProcess = StringProcessor()

        #take only the last phrase if user inputs multiple sentences
        try:
            #-1 cuz the user might give multiple sentences
            self.user_input = strProcess.chunkSentences(user_input)[-1]
            self.input_hist.extend(self.user_input)
        except:
            raise IndexError("I'll need a longer string to start prediction")

        while(True):
            print(self.user_input)
            next_word = self.predict()
            if next_word == 'END':
                return self.input_hist

            self.input_hist.append(next_word)
            self.user_input.append(next_word)


    def runSentence_Predict(self):

        #generate a sentence on a random __BIGRAM__

        self.user_input = [random.choice(list(self.lmTri["__1stWrd__"].keys()))]
        self.user_input.append(random.choice(list(self.lmTri["__2ndWrd__"][self.user_input[0]])))
        self.input_hist.extend(self.user_input)

        while(True):
            print(self.user_input)
            next_word = self.predict()
            if next_word == 'END':
                return self.input_hist

            self.input_hist.append(next_word)
            self.user_input.append(next_word)


    def runWord_Predict(self, user_input):

        strProcess = StringProcessor()
        #take only the last phrase if user inputs multiple sentences
        try:
            #-1 cuz the user might give multiple sentences
            self.user_input = strProcess.chunkSentences(user_input)[-1]
        except:
            raise IndexError("I'll need a longer string to start prediction")

        print("user_input:",self.user_input)

        self.input_hist.append(self.user_input)

        return self.predict()


    def flushHistory(self):
        self.user_input = []
        self.input_hist = []





