import tkinter as tk
from wordPredict import WordPredict

class Application(tk.Tk):
    def displayPredictionWrd(self, predictionFunction):
        user_input = self.inputTextBox.get("1.0",'end-1c')
        print(user_input)
        if not (user_input == ' ' or user_input == ''):
            prediction = predictionFunction(user_input) + "\n\n"
            print(prediction)
            self.outputText.config(state="normal")
            self.outputText.insert(tk.END, prediction)
            self.outputText.see(tk.END)
            self.outputText.config(state="disabled")
        wp.flushHistory()

    def displayPredictionSent(self, predictionFunction):
        prediction = predictionFunction()
        prediction.append("\n\n")
        self.outputText.config(state="normal")
        self.outputText.insert(tk.END, ' '.join(prediction))
        self.outputText.see(tk.END)
        self.outputText.config(state="disabled")
        wp.flushHistory()

    def displayFinishMySent(self, predictionFunction):
        user_input = self.inputTextBox.get("1.0",'end-1c')
        print(user_input)
        if user_input == ' ' or user_input == '':
            return self.displayPredictionSent(wp.runSentence_Predict)

        prediction = predictionFunction(user_input)
        prediction.append("\n\n")
        self.outputText.config(state="normal")
        self.outputText.insert(tk.END, ' '.join(prediction))
        self.outputText.see(tk.END)
        self.outputText.config(state="disabled")
        wp.flushHistory()

    def clearText(self, box):
        self.outputText.config(state="normal")
        box.delete('1.0', tk.END)
        self.outputText.config(state="disabled")

    def addEntryBox(self):
        self.userInput = tk.Frame(self, bg="#c7ffaf")
        self.userInput.pack(side="top", fill="both")

        self.label= tk.Label(self, text="INPUT", bg="#c7ffaf")
        self.label.pack(in_=self.userInput, side="top")

        self.clear = tk.Button(self, text="Clear Text",
                                    width=10,
                                    command=lambda: self.clearText(self.inputTextBox))

        self.clear.pack(in_=self.userInput, side="right", fill="y", expand=True)

        #scrollbar for text entry
        self.inputTextBox = tk.Text(self, width=50, height=5, bg="#c7ffaf")
        self.scrollbarEntry = tk.Scrollbar(self)
        self.scrollbarEntry.config(command=self.inputTextBox.yview)

        #configure scrollbar to actually scroll and pack
        self.inputTextBox.config(yscrollcommand=self.scrollbarEntry.set)
        self.scrollbarEntry.pack(in_=self.userInput, side="right", fill="y")
        self.inputTextBox.pack(in_=self.userInput, side="left", fill="both", expand=True)
        self.inputTextBox.focus_set()


    def addAnswerBox(self):
        self.output = tk.Frame(self, bg="#fffeaf")
        self.output.pack(side="top", fill="both")

        self.label= tk.Label(self, text="OUTPUT", bg="#fffeaf")
        self.label.pack(in_=self.output, side="top")

        self.clear = tk.Button(self, text="Clear Text",
                                    width=10,
                                    command=lambda: self.clearText(self.outputText))

        self.clear.pack(in_=self.output, side="right", fill="y", expand=True)

        #same but for output
        self.outputText = tk.Text(self, width=50, height=20, bg="#fffeaf")
        self.scrollbarAnswer = tk.Scrollbar(self)
        self.scrollbarAnswer.config(command=self.outputText.yview)

        self.outputText.config(yscrollcommand=self.scrollbarAnswer.set)
        self.scrollbarAnswer.pack(in_=self.output, side="right", fill="y")
        self.outputText.pack(in_=self.output, side="left", fill="both", expand=True)


    def addButtons(self):
        self.buttons = tk.Frame(self)
        self.buttons.pack(side="bottom", fill="both", expand=True)

        #lambda cuz tkinter doesn't give control of giving arguments to the function call
        self.singleWord = tk.Button(self, text="Predict Next Word",
                                    width=20,
                                    command=lambda: self.displayPredictionWrd(wp.runWord_Predict))
        #self.singleWord.pack({"anchor": "w"})
        self.singleWord.pack(in_=self.buttons, side="left", fill="both", expand=True)

        self.fullSentence = tk.Button(self, text="Predict Full Sentence",
                                      width=20,
                                      command=lambda: self.displayPredictionSent(wp.runSentence_Predict))
        #self.fullSentence.pack({"anchor": "w"})
        self.fullSentence.pack(in_=self.buttons, side="left", fill="both", expand=True)

        self.finishSentence = tk.Button(self, text="Finish My Sentence",
                                        width=20,
                                      command=lambda: self.displayFinishMySent(wp.runFinish_Predict))
        #self.finishSentence.pack({"anchor": "w"})
        self.finishSentence.pack(in_=self.buttons, side="left", fill="both", expand=True)


    def createWidgets(self):
        #frames
        self.addEntryBox()
        self.addAnswerBox()
        self.addButtons()

        #self.e = tk.Entry(self, width=60)#, textvariable = self.text)
        #self.e.pack({"anchor": "w"})
        #self.e.focus_set()


    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('{}x{}'.format(450, 500))
        self.resizable(width=False, height=False)
        self.title("Natural Language Prediction")
        self.entry = tk.StringVar()
        self.createWidgets()


TrainingSet = "Wiki"
wp = WordPredict(TrainingSet)
app = Application()
app.mainloop()

