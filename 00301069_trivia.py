#Tamir Mohamed
#ID: 00301069
#Final
#CIS 153
#Trivia quiz game
from tkinter import *
import random


class MyWindow:

    def __init__(self, win): #Initialize frame
        self.usernameLabel=Label(win, text='Username ', height=1, width=25)
        self.answerLabel=Label(win, text='Answer ')
        self.usernameLabel.place(x=232, y=60)
        self.answerLabel.place(x=297, y=110)
        self.usernameEntry=Entry(win, width=25)
        self.answerEntry=Entry(win, width=25)
        self.usernameEntry.place(x=243, y=85)
        self.answerEntry.place(x=243, y=134)
        
        self.textBox = Text(win, width = 78, height = 10, wrap = WORD)
        self.textBox.place(x=10, y=233)
        
        
        
        self.playButton = Button(win, text='Play', height=2, width=25, command = self.playGame)
        self.helpButton = Button(win, text='Help', height=2, width=25, command = self.showHelp)
        self.statsButton = Button(win, text='Stats', height=2, width=25, command = self.getStats)
        self.submitButton = Button(win, text='Submit', height=2, width=25, command = self.checkAnswer)
        self.playButton.place(x=10, y=10)
        self.helpButton.place(x=450, y=10)
        self.statsButton.place(x=230, y=10)
        self.submitButton.place(x=230, y=172)
        
        self.textBox.insert(0.0, "-Enter a username and press Stats to get statistics for that user. \n-Press stats with no username for general user information. \n-Press 'help' to return to these instructions on how to play the game. \n-Once you press play, you'll be prompted with a question. \n-Enter the corresponding letter to whichever answer you think is correct. \n-The program will tell you if you were correct or incorrect. \n-Your results will be logged and can be viewed with the 'stats' button.")
        self.textBox.configure(state='disabled')
        
    def getRandomNum(self): #Gets random number for question index
        num = random.randrange(1, 40)
        return num
        
    def getQuestionStats(self, passedQuestion):
        text = ''
        questionWrong = 0
        questionRight = 0
        logFile = open('log.txt')
        for line in logFile:
            line = line.rstrip()
            string = line
            questionPlace = string.find('QUESTION: ')
            resultPlace = string.find('RESULT: ')
            question = (string[questionPlace+10:resultPlace-1])
            result = (string[resultPlace+8:])
            if int(question) == passedQuestion and result == "Incorrect":
                questionWrong+=1
            elif int(question) == passedQuestion:
                questionRight+=1
        if questionRight + questionWrong > 0:
            text += "This question was guessed a total of " + str(questionWrong + questionRight) + " times with a " + str(round((questionRight/(questionRight + questionWrong)*100),2)) + "% success rate."    
        else:
            text += "This question hasn't been guessed yet." 
        return text
        
    def showHelp(self):
        self.textBox.configure(state='normal')
        self.textBox.delete(0.0, END)
        self.textBox.insert(0.0, "-Enter a username and press 'Statistics' to get statistics for that user. \n-Press stats with no username for general user information. \n-Press 'help' to return to these instructions on how to play the game. \n-Once you press play, you'll be prompted with a question. \n-Enter the corresponding letter to whichever answer you think is correct. \n-The program will tell you if you were correct or incorrect. \n-Your results will be logged and can be viewed with the 'stats' button.")
        self.textBox.configure(state='disabled')
        
    def getQuestion(self, questions):
        textToPrint=''
        rand = self.getRandomNum()
        for line in questions:
            line = line.rstrip()
            if line.startswith(str(rand) + ")"): #Find question at random index in file(to be seperated into function)
                string = line
                self.questionNumber = rand
                
                #Parse line
                numberPlace = string.find(')')
                firstOption = string.find('A)')
                answerPlace = string.find('Answer: ')
                self.question = (string[numberPlace+2:firstOption])
                options = (string[firstOption:answerPlace])
                self.ans = (string[answerPlace+8:])
                textToPrint += self.question
                textToPrint += "\n\n" + options + "\n\n" + self.getQuestionStats(rand)
        return textToPrint
        

    def playGame(self):
        questions = open('trivia.txt', encoding="utf8")
        self.textBox.configure(state='normal')
        if self.usernameEntry.get() == '': #Username field must be filled to playself.textBox.configure(state='disabled')
            self.textBox.delete(0.0, END)
            self.textBox.insert(0.0, "You need to insert a username before playing!")
        else:
            text = self.getQuestion(questions)
            self.textBox.delete(0.0, END)
            self.textBox.insert(0.0, text)
        self.textBox.configure(state='disabled')
        
    def checkAnswer(self):
        self.textBox.configure(state='normal')
        logFile = open('log.txt', 'a')
        isCorrect = "Incorrect"
        guess = self.answerEntry.get()
        username = self.usernameEntry.get()
        log = ''
        if self.usernameEntry.get() == '':
            self.textBox.delete(0.0, END)
            self.textBox.insert(0.0, "Please make sure you have entered a username.")
        else:
            if guess.upper() != self.ans:
                textToPrint = "You guessed incorrectly. Press 'Play' to get a new question!"
                log += "USERNAME: " + username + " QUESTION: " + str(self.questionNumber) + " RESULT: " + isCorrect + "\n"
                self.textBox.delete(0.0, END)
                self.textBox.insert(0.0, textToPrint)
                logFile.write(log)
                self.answerEntry.delete(0, END)
            else:
                isCorrect = "Correct"
                textToPrint = "That's the right choice! Well done! Press 'Play' for a new question!"
                log += "USERNAME: " + username + " QUESTION: " + str(self.questionNumber) + " RESULT: " + isCorrect + "\n"
                self.textBox.delete(0.0, END)
                self.textBox.insert(0.0, textToPrint)
                logFile.write(log)
                self.answerEntry.delete(0, END)
        self.textBox.configure(state='disabled')
                
    def getStats(self):
        self.textBox.configure(state='normal')
        users = dict()
        scores = dict()
        max = 0
        maxAddress = ''
        logFile = open('log.txt')
        if self.usernameEntry.get() == '': #If username field isn't filled in, get general stats
            for line in logFile:
                line = line.rstrip()
                string = line
                usernamePlace = string.find('USERNAME: ')
                questionPlace = string.find('QUESTION: ')
                resultPlace = string.find('RESULT: ')
                question = (string[questionPlace+10:resultPlace-1])
                result = (string[resultPlace+8:])
                username = (string[usernamePlace+10:questionPlace])
                if username not in users: #Fill users dict
                    users[username] = 1 
                else:
                    users[username] += 1 
                    
                if username not in scores and result == "Correct": #Fill users dict
                    scores[username] = 1 
                elif result == "Correct":
                    scores[username] += 1 
                    
            for username in users:  #Find user with most guesses
                if users[username] > max: #Find max
                    max = users[username] 
                    maxAddress = username  
                    
            sortedScores = (sorted(scores.items(), key = 
             lambda kv:(kv[1], kv[0]))) #Not reversed because the text box inserts items in the reverse order
            
                    
            self.textBox.delete(0.0, END)
            
            
            i = 5
            while i > 0:
                for key,value in sortedScores:
                    self.textBox.insert(0.0, str(i) + "." + key + "|" + " SCORE: " + str(value) + "\n")
                    i-=1
            self.textBox.insert(0.0, "--TOP FIVE LEADERBOARD--\n")        
            self.textBox.insert(0.0, "The user that made the most guesses is " + maxAddress + "and they made " + str(max) + " guesses.\n\n")
                
        else: #Otherwise show specific user stats
            numCorrect = 0
            numWrong = 0
            username = self.usernameEntry.get()
            for line in logFile:
                
                line = line.rstrip()
                string = line
                
                usernamePlace = string.find('USERNAME: ')
                questionPlace = string.find('QUESTION: ')
                resultPlace = string.find('RESULT: ')
                
                if username == (string[usernamePlace+10:questionPlace-1]):
                    if (string[resultPlace+8:]) == "Correct":
                        numCorrect+=1
                    else:
                        numWrong+=1
            self.textBox.delete(0.0, END)            
            self.textBox.insert(0.0, "User '" + username + "' made " + str(numCorrect + numWrong) + " total guesses. " + str(numCorrect) + " were correct and " + str(numWrong) + " were incorrect.")
        self.textBox.configure(state='disabled')

        
window=Tk()
mywin=MyWindow(window)
window.title('Trivia')
window.geometry("650x410")
window.resizable(False, False) 
window.mainloop()