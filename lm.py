'''INTERFACE NEEDED FOR THESE 2 CLASSES
'''

class SecondOrderMarkovModel:
    """2nd order markov language model
    1st word prob dist + 2nd word __BIGRAM__ dist + all else trigrams"""

    def __init__(self):
        self._lm_count = {"__1stWrd__":{}, "__2ndWrd__":{}, "__TRIGRAM__":{}}
        self._lm_prob = {"__1stWrd__":{}, "__2ndWrd__":{}, "__TRIGRAM__":{}}

    def getLMCount(self):
        return self._lm_count

    def getLMProb(self):
        return self._lm_prob

    def _addUnigram(self, word):
        """adding 0th order markov dist (1st word prob)"""
        try:
            self._lm_count["__1stWrd__"][word]+=1

        except:
            self._lm_count["__1stWrd__"][word]=1
            self._lm_prob["__1stWrd__"][word]=0


    def _addBigram(self, first, second):
        """adding 1st order markov dist (__BIGRAM__)"""

        try:
            self._lm_count["__2ndWrd__"][first][second]+=1

        except KeyError:
            #print(self.__lm_count[first])
            if first in self._lm_count["__2ndWrd__"]:
                self._lm_count["__2ndWrd__"][first][second]=1
                self._lm_prob["__2ndWrd__"][first][second]=0
            else:
                self._lm_count["__2ndWrd__"][first]={second:1}
                self._lm_prob["__2ndWrd__"][first]={second:0}


    def _addTrigram(self, first, second, third):
        """adding 2nd order markov dist (__TRIGRAM__)"""
        try:
            self._lm_count["__TRIGRAM__"][first][second][third]+=1

        except KeyError:
            #print(self.__lm_count[first])
            if first in self._lm_count["__TRIGRAM__"]:
                if second in self._lm_count["__TRIGRAM__"][first]:
                    self._lm_count["__TRIGRAM__"][first][second][third]=1
                    self._lm_prob["__TRIGRAM__"][first][second][third]=0
                else:
                    self._lm_count["__TRIGRAM__"][first][second]={third:1}
                    self._lm_prob["__TRIGRAM__"][first][second]={third:0}
            else:
                self._lm_count["__TRIGRAM__"][first]={second:{third:1}}
                self._lm_prob["__TRIGRAM__"][first]={second:{third:0}}


    def update(self, sent_chunk):

        #1st word prob dist
        self._addUnigram(sent_chunk[0])
        self._updateProbs("__1stWrd__")

        #2nd word (1st order markov model)
        self._addBigram(sent_chunk[0], sent_chunk[1])
        self._updateProbs("__2ndWrd__", sent_chunk[0])

        #the rest of the words (2nd order markov model)
        #run through chunked sentence and input counts in model
        for i, word in enumerate(sent_chunk):

            if i>len(sent_chunk)-3:
                break
            self._addTrigram(word, sent_chunk[i+1], sent_chunk[i+2])
            self._updateProbs("__TRIGRAM__", word, sent_chunk[i+1])

        #last __TRIGRAM__
        self._addTrigram(sent_chunk[-2], sent_chunk[-1], 'END')
        self._updateProbs("__TRIGRAM__", sent_chunk[-2], sent_chunk[-1])


    def _updateProbs(self, distribution, *args):
        """update probabilities of distributions"""

        ''' *args and checking len of args is O(1)
        **args and checking 'in args' might also be O(1)? not sure,
        cuz generally 'in' depends on size of list, but what about
        for dict?'''

        if len(args) > 2:
            raise ValueError("You gave too many optional arguments")

        #trigrams
        if len(args) > 1:
            lm_count_bucket = self._lm_count[distribution][args[0]][args[1]]
            lm_prob_bucket = self._lm_prob[distribution][args[0]][args[1]]
        #bigrams
        elif len(args) > 0:
            lm_count_bucket = self._lm_count[distribution][args[0]]
            lm_prob_bucket = self._lm_prob[distribution][args[0]]
        #unigram
        else:
            lm_count_bucket = self._lm_count[distribution]
            lm_prob_bucket = self._lm_prob[distribution]


        for i, word in enumerate(lm_count_bucket):
            lm_prob_bucket[word] = lm_count_bucket[word]/sum(list(lm_count_bucket.values()))



class FirstOrderMarkovModel:
    """1st order markov language model
    1st word prob dist + 2nd word __BIGRAM__ dist"""

    def __init__(self):
        self._lm_count = {"__1stWrd__":{}, "__BIGRAM__":{}}
        self._lm_prob = {"__1stWrd__":{}, "__BIGRAM__":{}}

    def getLMCount(self):
        return self._lm_count

    def getLMProb(self):
        return self._lm_prob

    def _addUnigram(self, word):
        """adding 0th order markov dist (1st word prob)"""
        try:
            self._lm_count["__1stWrd__"][word]+=1

        except:
            self._lm_count["__1stWrd__"][word]=1
            self._lm_prob["__1stWrd__"][word]=0

    def _addBigram(self, first, second):
        """adding 1st order markov dist (__BIGRAM__)"""

        try:
            self._lm_count["__BIGRAM__"][first][second]+=1

        except KeyError:
            #print(self.__lm_count[first])
            if first in self._lm_count["__BIGRAM__"]:
                self._lm_count["__BIGRAM__"][first][second]=1
                self._lm_prob["__BIGRAM__"][first][second]=0
            else:
                self._lm_count["__BIGRAM__"][first]={second:1}
                self._lm_prob["__BIGRAM__"][first]={second:0}


    def update(self, sent_chunk):
        #1st word prob dist
        self._addUnigram(sent_chunk[0])
        self._updateProbs("__1stWrd__")

        #the rest of the words (1st order markov model)
        #run through chunked sentence and input counts in model
        for i, word in enumerate(sent_chunk):

            if i>len(sent_chunk)-2:
                break

            self._addBigram(word, sent_chunk[i+1])
            self._updateProbs("__BIGRAM__", word)

        #last __BIGRAM__
        self._addBigram(sent_chunk[-1], 'END')
        self._updateProbs("__BIGRAM__", sent_chunk[-1])


    def _updateProbs(self, distribution, *args):
        """update probabilities of distributions
        can give optional arguments for __BIGRAM__/__TRIGRAM__"""

        ''' *args and checking len of args is O(1)
        **args and checking 'in args' might also be O(1)? not sure,
        cuz generally 'in' depends on size of list, but what about
        for dict?'''

        if len(args) > 1:
            raise ValueError("You gave too many optional arguments")

        #bigrams
        if len(args) > 0:
            lm_count_bucket = self._lm_count[distribution][args[0]]
            lm_prob_bucket = self._lm_prob[distribution][args[0]]
        #unigram
        else:
            lm_count_bucket = self._lm_count[distribution]
            lm_prob_bucket = self._lm_prob[distribution]


        for i, word in enumerate(lm_count_bucket):
            lm_prob_bucket[word] = lm_count_bucket[word]/sum(list(lm_count_bucket.values()))