from lm import SecondOrderMarkovModel, FirstOrderMarkovModel
from myParser import MyHTMLParser
import json


test = "This is a test piece of text to train the models.\n \
And this is the second sentence with special characters: comma, carrot^."

books = ["http://www.gutenberg.org/files/98/98-0.txt",
         "http://www.gutenberg.org/files/1342/1342-0.txt"]

simpleSite = ["https://motherfuckingwebsite.com/"]

scienceSites = ["https://en.wikipedia.org/wiki/Computer_science",
        "https://en.wikipedia.org/wiki/Computational_linguistics",
        "https://en.wikipedia.org/wiki/Linguistics",
        "https://en.wikipedia.org/wiki/Language",
        "https://en.wikipedia.org/wiki/Natural_language_processing",
        "https://en.wikipedia.org/wiki/Culture",
        "https://en.wikipedia.org/wiki/War",
        "https://en.wikipedia.org/wiki/Peace",
        "https://en.wikipedia.org/wiki/Human",
        "https://en.wikipedia.org/wiki/Science",
        "https://en.wikipedia.org/wiki/Space",
        "https://en.wikipedia.org/wiki/Galaxy",
        "https://en.wikipedia.org/wiki/Star"]

TrainingSet = 'Literature'


modelTri = SecondOrderMarkovModel()
modelBi = FirstOrderMarkovModel()
parser = MyHTMLParser(isWiki=False)

for url in books:

    print('Now processing: ' + url)

    htmlStr = MyHTMLParser.grabTextURL(url)

    parser.feed(htmlStr)

    #update model
    for i in parser.getData():
        if len(i) > 2:
            modelTri.update(i)
            modelBi.update(i)

#write to txt file
with open(f"Models/lm{TrainingSet}TrigramProb.txt", "w") as text_file:
    #format string: print(f"Purchase Amount: {TotalAmount}", file=text_file)
    #print(str(model.getLMProb()).encode("utf-8"), file=text_file)
    print(json.dumps(modelTri.getLMProb()), file=text_file)

with open(f"Models/lm{TrainingSet}TrigramCount.txt", "w") as text_file:
    print(json.dumps(modelTri.getLMCount()), file=text_file)

#write to txt file
with open(f"Models/lm{TrainingSet}BigramProb.txt", "w") as text_file:
    print(json.dumps(modelBi.getLMProb()), file=text_file)

with open(f"Models/lm{TrainingSet}BigramCount.txt", "w") as text_file:
    print(json.dumps(modelBi.getLMCount()), file=text_file)