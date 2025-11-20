import tkinter as tk #importing tkinkter
import tkinter.messagebox as msgbox #message boxes
import random #for random numbers
from PIL import Image, ImageTk #for importing images
import winsound

# PLEASE NOTE ON AI ASSISTANCE:
# This program was written by me based on the module lecture notes.
# ChatGPT was only used to help debug small issues (e.g. showing the feedback text label and tweaking widget positions)
# what was said: "above is the code with ss as how the placement is i want the spacing to be nice" or simply a "what is the error"

EASY_RANGE = (1, 9) #choosing the range for the easy level
MODERATE_RANGE = (10, 99) #choosing the range for moderate level
ADVANCED_RANGE = (1000, 9999) #choosing the range for advanced level 

class MathsQuizApp: #class being made 
    def __init__(self, master):
        self.master = master
        self.master.title("01- Maths Quiz!") #the title of the window
        self.master.geometry("600x400") #the size of the window
        self.master.resizable(False, False) #window is non resizeable 
        self.master.configure(bg="#FCE2E6") #the color for the window

        self.difficulty_level = None #to track the chosen difficulty 
        self.current_question = 0 #the counter of the questions
        self.score = 0 #tracks the score
        self.current_answer = None #to store the answer
        self.chances_left = 2 #chances per question 
        self.current_num1 = 0 #number 1 in question
        self.current_num2 = 0 #number 2 in question
        self.current_operation = '' # chooses + or - 

        self.question_text = tk.StringVar(master, value="Select Difficulty Level")  
        self.score_text = tk.StringVar(master, value="Score: 0") #displays the score
        self.user_answer = tk.StringVar() #input binding 
        self.feedback_text = tk.StringVar(master, value="") #for feedback text
        self.question_number_text = tk.StringVar(master, value="")
        self.frames = {} #using dictionary of frames
        self.frames["start"] = self._create_start_page() #start page frame
        self.frames["menu"] = self._create_menu_frame() #menu page frame 
        self.frames["quiz"] = self._create_quiz_frame() #quiz page frame
        
        self._show_frame("start") #to show the start page first

    def _show_frame(self, page_name): #to help switch pages
        frame = self.frames[page_name] #to get frame from dictionary
        frame.tkraise() #frame comes on top

    def _create_start_page(self): #start screen
        frame = tk.Frame(self.master, bg="#FCE2E6") #creates frame with the color
        frame.place(x=0, y=0, relwidth=1, relheight=1) #to place the frame and cover the window

        try:
            original_image = Image.open("Resources\images\start.png") #uploaded the image in the back
            resized_image = original_image.resize((600, 400), Image.Resampling.LANCZOS) #resizes the image to fit the window
            self.background_photo = ImageTk.PhotoImage(resized_image) #to convert the image for tkinter
            background_label = tk.Label(frame, image=self.background_photo) #label to show the background image
            background_label.place(x=0, y=0, relwidth=1, relheight=1) #place of the bg image
        except FileNotFoundError: #if the image is not found the below is displayed on the screen
            tk.Label(frame, text="MATH QUIZ - Image Not Found", bg="#FCE2E6", fg="#FF0073", font=("Roboto", 30, "bold")).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            
        tk.Button(frame, 
                  text="START", #the text on button 
                  command=lambda: self._show_frame("menu"), #when clciked takes to menu
                  fg="#FFFFFF", #text color
                  bg="#ffa9c2", # background color
                  activebackground="#ffa9c2", #colod when clicked
                  font=("Roboto", 16, "bold"), #font size
                  relief=tk.FLAT, #flat button
                  bd=0, #no borders
                  highlightthickness=0, #no highlight borders
                 ).place(relx=0.5, rely=0.74, anchor=tk.CENTER) #the position of the button

        return frame #returns the start frame

    def _create_menu_frame(self): #creates the menu page
        frame = tk.Frame(self.master, bg="#FCE2E6") #background color and frame
        frame.place(x=0, y=0, relwidth=1, relheight=1) #covers the entire window
        
        try:
            original_image = Image.open("Resources\images\MENU.png") #loads the image
            resized_image = original_image.resize((600, 400), Image.Resampling.LANCZOS) #resizes to fit window
            self.menu_background_photo = ImageTk.PhotoImage(resized_image) #converts to tkinter
            background_label = tk.Label(frame, image=self.menu_background_photo) #label with image
            background_label.place(x=0, y=0, relwidth=1, relheight=1) #places background image
        except FileNotFoundError: #if the image is not found the below is displayed on the screen
            tk.Label(frame, text="CHOOSE DIFFICULTY - Image Not Found", bg="#FCE2E6", fg="#FF0073", font=("Roboto", 30, "bold")).pack(pady=(40, 30))
            
        button_style = {
                "bg": "#fff8f3",    #background color       
                "activebackground": "#fff8f3", #button color when clciked
                "fg": "#2e1940", #text color
                "activeforeground": "#2e1940", #text color when clicked
                "font": ("Roboto", 9, "bold"), #font
                "relief": tk.FLAT, #flat vbutton
                "bd": 0, #no border
                "highlightthickness": 0, #no highliught border
                "cursor": "hand2", #cursor changes to hand
                }
        
        tk.Button( 
            frame,
            text="EASY", #text on the button
            command=lambda: self._start_quiz('easy'),
            **button_style
        ).place(relx=0.21, rely=0.7, anchor=tk.CENTER) #position of the button

        tk.Button(
            frame,
            text="MODERATE", #text on the button
            command=lambda: self._start_quiz('moderate'),
            **button_style
        ).place(relx=0.50, rely=0.7, anchor=tk.CENTER) #position of the button

        tk.Button(
            frame,
            text="ADVANCED", #text on the button
            command=lambda: self._start_quiz('advanced'),
            **button_style
        ).place(relx=0.79, rely=0.7, anchor=tk.CENTER) #position of the button
        
        return frame #returns menu page
    
    def _create_quiz_frame(self): #creates quuiz page
        frame = tk.Frame(self.master, bg="#FCE2E6") #frame of the quix with background color
        frame.place(x=0, y=0, relwidth=1, relheight=1) #covers the whole window

        try:
            original_image = Image.open("Resources/images/QUIZ.png") #loads the image
            resized_image = original_image.resize((600, 400), Image.Resampling.LANCZOS) #resizes the image to fit the window
            self.quiz_bg = ImageTk.PhotoImage(resized_image) #converts the image to tkinter
            background_label = tk.Label(frame, image=self.quiz_bg) #label to show the background
            background_label.place(x=0, y=0, relwidth=1, relheight=1) #places the image in frame
        except: #if the image is not found the below is displayed on the screen
            frame.configure(bg="#FCE2E6")

        tk.Button(frame, text="Back", command=lambda: self._show_frame("menu"), #button for menu, when pressed shows menu
                  bg="#fff", fg="#333", font=("Roboto", 9, "bold"), #button background, text colour
                  relief=tk.FLAT, bd=0, highlightthickness=0, cursor="hand2", # flat button, no border, no highlight border and hand cursor
                  padx=6, pady=2).place(relx=0.05, rely=0.08, anchor="w") #horizontal and veritical padding with placement of button
        
        tk.Label(frame,
            textvariable=self.question_number_text,     #to show the question number
            bg="#ffc0d2", #its background color
            fg="#2e1940", #text color
            font=("Roboto", 18, "bold") #font
        ).place(relx=0.23, rely=0.18, anchor="w") #placement of the label

        tk.Label(frame, textvariable=self.question_text, #the question text is shown
                 bg="#fff8f3", fg="#D42470", #label background and the text colour
                 font=("Roboto", 26, "bold")).place(relx=0.43, rely=0.32, anchor="center") #position of question label

        tk.Entry(frame, textvariable=self.user_answer, #entry to user_answer variable
                 width=10, font=("Roboto", 20), #width of entry box, font
                 justify="center").place(relx=0.43, rely=0.43, anchor="center") #text in centre and psoition of answer entry

        tk.Button(frame, text="Submit", command=self._submit_answer, #text on button, calls function to check the answer
                  bg="#FF69A6", fg="white", activebackground="#FF8ABA", #button background, text color, button color when clciked
                  font=("Roboto", 14, "bold"), relief=tk.FLAT, bd=0, #font style, flat button, no border
                  padx=20, pady=6, cursor="hand2").place(relx=0.43, rely=0.57, anchor="center") #horizontal, vertical padding anc hand on hover + position of the button

        tk.Label(frame, textvariable=self.score_text, #shows current score
                 bg="#fff8f3", fg="#2e1940", #text and background color
                 font=("Roboto", 14, "bold")).place(relx=0.43, rely=0.69, anchor="center") #font for score and position of label
        
        tk.Label(
            frame,textvariable=self.feedback_text, #feedback text like incorrect or correct
            bg="#fff8f3", fg="#D42470",  #background and text color
            font=("Roboto", 12, "bold") #font
        ).place(relx=0.43, rely=0.78, anchor="center") #position of the button

        return frame #returns frame
    
    def _start_quiz(self, difficulty): #game starts with the chosen difficulty
        self.difficulty_level = difficulty #stores the choise
        self._reset_quiz() #resets the score and querstions
        self._show_frame("quiz") #switches to quiz page
        self._next_problem() #load the first question 

    def _reset_quiz(self): #resets the quiz values
        self.current_question = 0 #resets the question counter
        self.score = 0 #resets the score
        self.score_text.set("Score: 0") #updates the score label 
        self.user_answer.set("") #clear the old answer
        self.question_number_text.set("") #clears the question number

    def _random_int(self): #gets random number based on difficulty
        if self.difficulty_level == 'easy': #if easy selected
            min_val, max_val = EASY_RANGE #if easy selected
        elif self.difficulty_level == 'moderate': #if moderate selected
            min_val, max_val = MODERATE_RANGE #use moderate range
        else:
            min_val, max_val = ADVANCED_RANGE #otherwise use advanced range
        return random.randint(min_val, max_val) #return random number between min and max

    def _decide_operation(self): #decides which math operation to use
        return random.choice(['+', '-']) #chooses between + or -

    def _display_problem(self): #creates and shows a new question
        self.current_num1 = self._random_int() #get first random number 
        self.current_num2 = self._random_int() #get second random number
        self.current_operation = self._decide_operation() #chooses between + or -

        if self.current_operation == '-' and self.current_num2 > self.current_num1: #if subtraction would go negative
            self.current_num1, self.current_num2 = self.current_num2, self.current_num1 #swap so result stays positive

        if self.current_operation == '+': #if operation is addition
            self.current_answer = self.current_num1 + self.current_num2 #calculate answer for +
        else:
            self.current_answer = self.current_num1 - self.current_num2 #calculate answer for -

        self.question_number_text.set(f"Question {self.current_question}") #updates question number
        self.question_text.set(f"{self.current_num1} {self.current_operation} {self.current_num2} = ?") #updates the label to show the question
        self.user_answer.set("") #clears previous input from entry
        self.chances_left = 2  #resets the chances back to 2 for new question

    def _submit_answer(self): #checks the answer
        text = self.user_answer.get() #get text typed 
        if not text: #if nothign is entered below is shown
            self.feedback_text.set("Please enter an answer.")
            return #exits 

        try:
            guess = int(text) #try converting input to an integer
        except ValueError:
            self.feedback_text.set("Invalid input. Enter a number.") #error if not a number
            return #exit function if invalid

        if guess == self.current_answer: #if user got correct answer
            self._mark_correct() #call function to handle correct answer
        else:
            self._mark_incorrect() #call function to handle wrong answer

    def _mark_correct(self):  #handles correct answers
        points = 10 if self.chances_left == 2 else 5 #10 points if correct answer on first try orelse 5 points
        self.score += points #add points to score
        self.score_text.set(f"Score: {self.score}") #update score label
        self.feedback_text.set(f"Correct! (+{points} points)") #feedback saying answer is correct
        self._next_problem() #go to next question

    def _mark_incorrect(self): #handles the wrong answers
        self.chances_left -= 1  #reduces chances by 1
        if self.chances_left >= 1: #if 1 chance is left brlow is shown
            self.feedback_text.set(f"Wrong answer. {self.chances_left} chance left.") # chance left 1 is shown
        else:
            self.feedback_text.set(f"Wrong. Answer was {self.current_answer}.") #shows the correct answer
            self._next_problem() #goes to the next wuestion

    def _next_problem(self): #to move to the next problem
        self.current_question += 1 #increase the question count by 1
        if self.current_question > 10: #to ask 10 questions
            self._finish_quiz() #finish it there and show results
        else:
            self._display_problem() #orelse more questions

    def _finish_quiz(self): #what diaplays when the quiz ends
        rank = "C" #default rank
        if self.score > 90: #rank a+ is shown if scored points are more thn 90 
            rank = "A+"
        elif self.score > 70: #rank a is shown if scored more thn 70
            rank = "A"
        elif self.score > 50: #rank b is shown is scored more thn 50
            rank = "B"

        msg = f"Quiz Finished!\nScore: {self.score}/100\nRank: {rank}" #final message 
        msgbox.showinfo("Quiz Results", msg) #the popup showning the score and rank

        if msgbox.askyesno("Play Again?", "Play another quiz?"): #asks the user if they want to play again
            self._show_frame("menu") #takes back to menu
            self.question_text.set("Select Difficulty Level") #resets the question text
            self.feedback_text.set("Welcome to the Maths Quiz!") #and also the feedback text
        else:
            self.master.quit() #closes the window if user says no to playing again

if __name__ == '__main__': #checks if the file is run directly
    root = tk.Tk() #creates the main window
    winsound.PlaySound(
        r"\Resources\images\TUNIC  - Lifeformed.wav",
        winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
    )
    app = MathsQuizApp(root) #creates an instance of the class
    root.mainloop() #keeps the window open 
