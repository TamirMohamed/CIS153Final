#Trivia quiz game

from tkinter import *
import random
import time

class Application(Frame):

    def getRandomNum(self): #Gets random number between 1 and 40
        num = random.randrange(1, 40)
        return num

    def __init__(self, master): #initialize frame
        Frame.__init__(self, master) 
        self.grid()
        self.makeElements()
        self.number = random.randint(1, 101)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=0)
        self.rowconfigure(3, weight=1)

    def makeElements(self):
        
        Button(self, text = "Play", command = self.playGame).grid(row = 0, column = 0, sticky = W)
        Button(self, text = "Help", command = self.playGame).grid(row = 0, column = 1, sticky = W)
        Button(self, text = "Statistics", command = self.getStats).grid(row = 0, column = 2, sticky = W)

        Label(self, text = "Answer:").grid(row = 2, column = 0, sticky = W)
        self.answerEntry = Entry(self)
        self.answerEntry.grid(row = 2, column = 1, sticky = W)
        
        Label(self, text = "Username:").grid(row = 1, column = 0, sticky = W)
        self.username = Entry(self)
        self.username.grid(row = 1, column = 1, sticky = W)

        Label(self, text = "Press submit to check your answer:").grid(row = 3, column = 0, sticky = W)
        Button(self, text = "Submit", command = self.checkAnswer).grid(row = 3, column = 1, sticky = W)

        instructions = 'Enter a username and press "stats" to get statistics for that user. Press "help" for instructions on how to play the game. Otherwise press play to get quizzed!'

        self.text = Text(self, width = 70, height = 10, wrap = WORD)
        self.text.grid(row = 4, column = 0, columnspan = 3)
        
        self.text.insert(0.0, instructions)

    def playGame(self):
        print_text=''
        questions = open('trivia.txt', encoding="utf8")
        rand = self.getRandomNum()
        if self.username.get() == '':
            self.text.delete(0.0, END)
            self.text.insert(0.0, "You need to insert a username before playing!")
        else:
            for line in questions:
                line = line.rstrip()
                if line.startswith(str(rand) + ")"):
                    string = line
                    self.questionNumber = rand
                    numberPlace = string.find(')')
                    firstOption = string.find('A)')
                    answerPlace = string.find('Answer: ')
                    self.question = (string[numberPlace+2:firstOption])
                    options = (string[firstOption:answerPlace])
                    self.ans = (string[answerPlace+8:])
                    print_text += self.question
                    print_text += "\n\n" + options
            self.text.delete(0.0, END)
            self.text.insert(0.0, print_text)
        
    def checkAnswer(self):
        logFile = open('log.txt', 'a')
        isCorrect = "Incorrect"
        guess = self.answerEntry.get()
        username = self.username.get()
        log = ''
        if self.username.get() == '':
            self.text.delete(0.0, END)
            self.text.insert(0.0, "Please make sure you have entered a username.")
        else:
            if guess.upper() != self.ans:
                print_text = "You guessed incorrectly. Press 'Play' to get a new question!"
                log += "USERNAME: " + username + " QUESTION: " + str(self.questionNumber) + " RESULT: " + isCorrect + "\n"
                self.text.delete(0.0, END)
                self.text.insert(0.0, print_text)
                logFile.write(log)
                self.answerEntry.delete(0, END)
            else:
                isCorrect = "Correct"
                print_text = "That's the right choice! Well done! Press 'Play' for a new question!"
                log += "USERNAME: " + username + " QUESTION: " + str(self.questionNumber) + " RESULT: " + isCorrect + "\n"
                self.text.delete(0.0, END)
                self.text.insert(0.0, print_text)
                logFile.write(log)
                self.answerEntry.delete(0, END)
                
    def getStats(self):
        users = dict()
        max = 0
        maxAddress = ''
        logFile = open('log.txt')
        if self.username.get() == '': #If username field is blank
            for line in logFile:
                line = line.rstrip()
                string = line
                usernamePlace = string.find('USERNAME: ')
                questionPlace = string.find('QUESTION: ')
                username = (string[usernamePlace+10:questionPlace])
                if username not in users:
                    users[username] = 1 #Count first instance
                else:
                    users[username] += 1 #Count further
                    
            for username in users:  #For all addresses
                if users[username] > max: #If new max  
                    max = users[username] #Store max
                    maxAddress = username   #Store address
            self.text.delete(0.0, END)
            self.text.insert(0.0, "The user that made the most guesses is " + maxAddress + "and they made " + str(max) + " guesses.")
        else:
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
            self.text.delete(0.0, END)            
            self.text.insert(0.0, "User '" + username + "' made " + str(numCorrect + numWrong) + " total guesses. " + str(numCorrect) + " were correct and " + str(numWrong) + " were incorrect.")

        
root = Tk()
root.title("Trivia")
app = Application(root)
root.mainloop()