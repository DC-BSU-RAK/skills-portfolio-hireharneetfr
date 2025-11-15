import tkinter as tk
import tkinter.messagebox as msgbox
import sys
import random
from PIL import Image, ImageTk

EASY_RANGE = (1, 9)
MODERATE_RANGE = (10, 99)
ADVANCED_RANGE = (1000, 9999)

class MathsQuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("01- Maths Quiz!")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        self.master.configure(bg="#FCE2E6")

        self.difficulty_level = None
        self.current_question = 0
        self.score = 0
        self.current_answer = None
        self.chances_left = 2
        self.current_num1 = 0
        self.current_num2 = 0
        self.current_operation = ''

        self.question_text = tk.StringVar(master, value="Select Difficulty Level")
        self.score_text = tk.StringVar(master, value="Score: 0")
        self.user_answer = tk.StringVar()
        self.feedback_text = tk.StringVar(master, value="")

        self.frames = {}
        self.frames["start"] = self._create_start_page()
        self.frames["menu"] = self._create_menu_frame()
        self.frames["quiz"] = self._create_quiz_frame()
        
        self._show_frame("start")    

        self.frames = {}
        self.frames["start"] = self._create_start_page()
        self.frames["menu"] = self._create_menu_frame()
        self.frames["quiz"] = self._create_quiz_frame()
        
        self._show_frame("start")

    def _show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def _create_start_page(self):
        frame = tk.Frame(self.master, bg="#FCE2E6") 
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        try:
            original_image = Image.open("Resources\images\start.png")
            resized_image = original_image.resize((600, 400), Image.Resampling.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(frame, image=self.background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            tk.Label(frame, text="MATH QUIZ - Image Not Found", bg="#FCE2E6", fg="#FF0073", font=("Roboto", 30, "bold")).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            
        tk.Button(frame, 
                  text="START", 
                  command=lambda: self._show_frame("menu"),
                  fg="#FFFFFF",
                  bg="#ffa9c2",
                  activebackground="#ffa9c2",
                  font=("Roboto", 16, "bold"),
                  relief=tk.FLAT,
                  bd=0,
                  highlightthickness=0,
                 ).place(relx=0.5, rely=0.74, anchor=tk.CENTER) 

        return frame

    def _create_menu_frame(self):
        frame = tk.Frame(self.master, bg="#FCE2E6")
        frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        try:
            original_image = Image.open("Resources\images\MENU.png") 
            resized_image = original_image.resize((600, 400), Image.Resampling.LANCZOS)
            self.menu_background_photo = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(frame, image=self.menu_background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            tk.Label(frame, text="CHOOSE DIFFICULTY - Image Not Found", bg="#FCE2E6", fg="#FF0073", font=("Roboto", 30, "bold")).pack(pady=(40, 30))
            
        button_style = {
                "bg": "#fff8f3",           
                "activebackground": "#fff8f3",
                "fg": "#2e1940",
                "activeforeground": "#2e1940",
                "font": ("Roboto", 9, "bold"),
                "relief": tk.FLAT,
                "bd": 0,
                "highlightthickness": 0,
                "cursor": "hand2",
                }
        
        tk.Button(
            frame,
            text="EASY",
            command=lambda: self._start_quiz('easy'),
            **button_style
        ).place(relx=0.21, rely=0.7, anchor=tk.CENTER)

        tk.Button(
            frame,
            text="MODERATE",
            command=lambda: self._start_quiz('moderate'),
            **button_style
        ).place(relx=0.50, rely=0.7, anchor=tk.CENTER)

        tk.Button(
            frame,
            text="ADVANCED",
            command=lambda: self._start_quiz('advanced'),
            **button_style
        ).place(relx=0.79, rely=0.7, anchor=tk.CENTER)
        
        return frame
    
    def _create_quiz_frame(self):
        frame = tk.Frame(self.master, bg="#FCE2E6")
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        try:
            original_image = Image.open("Resources/images/QUIZ.png")
            resized_image = original_image.resize((600, 400), Image.Resampling.LANCZOS)
            self.quiz_bg = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(frame, image=self.quiz_bg)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            frame.configure(bg="#FCE2E6")

        tk.Button(frame, text="Back", command=lambda: self._show_frame("menu"),
                  bg="#fff", fg="#333", font=("Roboto", 9, "bold"),
                  relief=tk.FLAT, bd=0, highlightthickness=0, cursor="hand2",
                  padx=6, pady=2).place(relx=0.05, rely=0.08, anchor="w")

        tk.Label(frame, textvariable=self.question_text,
                 bg="#fff8f3", fg="#D42470",
                 font=("Roboto", 26, "bold")).place(relx=0.43, rely=0.34, anchor="center")

        tk.Entry(frame, textvariable=self.user_answer,
                 width=10, font=("Roboto", 20),
                 justify="center").place(relx=0.43, rely=0.47, anchor="center")

        tk.Button(frame, text="Submit", command=self._submit_answer,
                  bg="#FF69A6", fg="white", activebackground="#FF8ABA",
                  font=("Roboto", 14, "bold"), relief=tk.FLAT, bd=0,
                  padx=20, pady=6, cursor="hand2").place(relx=0.43, rely=0.61, anchor="center")

        tk.Label(frame, textvariable=self.score_text,
                 bg="#fff8f3", fg="#2e1940",
                 font=("Roboto", 14, "bold")).place(relx=0.43, rely=0.73, anchor="center")

        return frame
    
    def _start_quiz(self, difficulty):
        self.difficulty_level = difficulty
        self._reset_quiz()
        self._show_frame("quiz")
        self._next_problem()

    def _reset_quiz(self):
        self.current_question = 0
        self.score = 0
        self.score_text.set("Score: 0")
        self.feedback_text.set("Quiz started! Good luck.")
        self.user_answer.set("")

    def _random_int(self):
        if self.difficulty_level == 'easy':
            min_val, max_val = EASY_RANGE
        elif self.difficulty_level == 'moderate':
            min_val, max_val = MODERATE_RANGE
        else:
            min_val, max_val = ADVANCED_RANGE
        return random.randint(min_val, max_val)

    def _decide_operation(self):
        return random.choice(['+', '-'])

    def _display_problem(self):
        self.current_num1 = self._random_int()
        self.current_num2 = self._random_int()
        self.current_operation = self._decide_operation()

        if self.current_operation == '-' and self.current_num2 > self.current_num1:
            self.current_num1, self.current_num2 = self.current_num2, self.current_num1

        if self.current_operation == '+':
            self.current_answer = self.current_num1 + self.current_num2
        else:
            self.current_answer = self.current_num1 - self.current_num2

        self.question_text.set(f"{self.current_num1} {self.current_operation} {self.current_num2} = ?")
        self.user_answer.set("")
        self.chances_left = 2

    def _submit_answer(self):
        text = self.user_answer.get()
        if not text:
            self.feedback_text.set("Please enter an answer.")
            return

        try:
            guess = int(text)
        except ValueError:
            self.feedback_text.set("Invalid input. Enter a number.")
            return

        if guess == self.current_answer:
            self._mark_correct()
        else:
            self._mark_incorrect()

    def _mark_correct(self):
        points = 10 if self.chances_left == 2 else 5
        self.score += points
        self.score_text.set(f"Score: {self.score}")
        self.feedback_text.set(f"Correct! (+{points} points)")
        self._next_problem()

    def _mark_incorrect(self):
        self.chances_left -= 1
        if self.chances_left >= 1:
            self.feedback_text.set(f"Wrong answer. {self.chances_left} chance left.")
        else:
            self.feedback_text.set(f"Wrong. Answer was {self.current_answer}.")
            self._next_problem()

    def _next_problem(self):
        self.current_question += 1
        if self.current_question > 10:
            self._finish_quiz()
        else:
            self._display_problem()

    def _finish_quiz(self):
        rank = "C"
        if self.score > 90:
            rank = "A+"
        elif self.score > 70:
            rank = "A"
        elif self.score > 50:
            rank = "B"

        msg = f"Quiz Finished!\nScore: {self.score}/100\nRank: {rank}"
        msgbox.showinfo("Quiz Results", msg)

        if msgbox.askyesno("Play Again?", "Play another quiz?"):
            self._show_frame("menu")
            self.question_text.set("Select Difficulty Level")
            self.feedback_text.set("Welcome to the Maths Quiz!")
        else:
            self.master.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = MathsQuizApp(root)
    root.mainloop()
