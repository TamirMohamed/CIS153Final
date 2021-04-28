#Trivia quiz game

from tkinter import *
import random


class Application(Frame):

    def __init__(self, master): #Initialize frame
        Frame.__init__(self, master) 
        self.grid()
        self.makeElements()
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=0)
        self.rowconfigure(3, weight=1)

    def makeElements(self):
        #Place elements (rough)
        Button(self, text = "Play", command = self.playGame).grid(row = 0, column = 0, sticky = W)
        Button(self, text = "Help", command = self.playGame).grid(row = 0, column = 1, sticky = W) #Help button function to be implemented
        Button(self, text = "Statistics", command = self.getStats).grid(row = 0, column = 2, sticky = W)

        Label(self, text = "Answer:").grid(row = 2, column = 0, sticky = W)
        self.answerEntry = Entry(self)
        self.answerEntry.grid(row = 2, column = 1, sticky = W)
        
        Label(self, text = "Username:").grid(row = 1, column = 0, sticky = W)
        self.username = Entry(self)
        self.username.grid(row = 1, column = 1, sticky = W)

        Label(self, text = "Press submit to check your answer:").grid(row = 3, column = 0, sticky = W)
        Button(self, text = "Submit", command = self.checkAnswer).grid(row = 3, column = 1, sticky = W)

        instructions = 'Enter a username and press "Statistics" to get statistics for that user. \nPress stats with no username for general user information. \nPress "help" for instructions on how to play the game. \nOtherwise enter a username and press play to get quizzed!'

        self.textBox = Text(self, width = 70, height = 10, wrap = WORD)
        self.textBox.grid(row = 4, column = 0, columnspan = 3)
        
        self.textBox.insert(0.0, instructions)
        
    def getRandomNum(self): #Gets random number for question index
        num = random.randrange(1, 40)
        return num

    def playGame(self):
        textToPrint=''
        questions = open('trivia.txt', encoding="utf8")
        rand = self.getRandomNum()
        if self.username.get() == '': #Username field must be filled to play
            self.textBox.delete(0.0, END)
            self.textBox.insert(0.0, "You need to insert a username before playing!")
        else:
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
                    textToPrint += "\n\n" + options
            self.textBox.delete(0.0, END)
            self.textBox.insert(0.0, textToPrint)
        
    def checkAnswer(self):
        logFile = open('log.txt', 'a')
        isCorrect = "Incorrect"
        guess = self.answerEntry.get()
        username = self.username.get()
        log = ''
        if self.username.get() == '':
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
                
    def getStats(self):
        users = dict()
        max = 0
        maxAddress = ''
        logFile = open('log.txt')
        if self.username.get() == '': #If username field isn't filled in, get general stats
            for line in logFile:
                line = line.rstrip()
                string = line
                usernamePlace = string.find('USERNAME: ')
                questionPlace = string.find('QUESTION: ')
                username = (string[usernamePlace+10:questionPlace])
                if username not in users: #Fill users dict
                    users[username] = 1 
                else:
                    users[username] += 1 
                    
            for username in users:  #For all usernames
                if users[username] > max: #Find max
                    max = users[username] 
                    maxAddress = username  
            self.textBox.delete(0.0, END)
            self.textBox.insert(0.0, "The user that made the most guesses is " + maxAddress + "and they made " + str(max) + " guesses.")
        else: #Otherwise show specific user stats
            numCorrect = 0
            numWrong = 0
            username = self.username.get()
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

        
root = Tk()
root.title("Trivia")
app = Application(root)
root.mainloop()