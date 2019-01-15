from wordPredict import WordPredict

TrainingSet = "Literature"

wp = WordPredict(TrainingSet)

while(True):
    user_input = input("sentece/word: ")

    if user_input.lower() == 'word':
        while(True):

            user_input = input("\nStart typing your phrase and press enter when \nyou'd like to get a prediction for the next word:\n")

            if user_input.lower() == 'break':
                break

            wp.runWord_Predict(user_input)

    else:
        while(True):
            user_input = input("go?: ")

            if user_input.lower() == 'break':
                break
            else:
                wp.runSentence_Predict()

    print(wp.input_hist)
    wp.flushHistory()