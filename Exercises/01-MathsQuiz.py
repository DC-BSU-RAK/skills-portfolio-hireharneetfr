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
        self.feedback_text = tk.StringVar(master, value="Welcome to the Maths Quiz!")
        self.score_text = tk.StringVar(master, value="Score: 0")
        self.user_answer = tk.StringVar()

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
                  bg="#FCE2E6",
                  fg="#FFC0CB",
                  font=("Roboto", 24, "bold"),
                  relief=tk.FLAT,
                  bd=0,
                  highlightthickness=0,
                  width=7,
                 ).place(relx=0.5, rely=0.67, anchor=tk.CENTER) 

        return frame

    def _create_menu_frame(self):
        frame = tk.Frame(self.master, bg="#FCE2E6")
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(frame, text="DIFFICULTY LEVEL", bg="#000000", fg="black", font=("Roboto", 18, "bold")).pack(pady=20)

        tk.Button(frame, text="1. Easy (Single Digit)", command=lambda: self._start_quiz('easy'), bg="#FF4397", fg="black", font=("Roboto", 12)).pack(pady=5, ipadx=10)
        tk.Button(frame, text="2. Moderate (Double Digit)", command=lambda: self._start_quiz('moderate'), bg="#FF0073", fg="black", font=("Roboto", 12)).pack(pady=5, ipadx=10)
        tk.Button(frame, text="3. Advanced (4-Digit)", command=lambda: self._start_quiz('advanced'), bg="#F6197C", fg="black", font=("Roboto", 12)).pack(pady=5, ipadx=10)

        return frame

    def _create_quiz_frame(self):
        frame = tk.Frame(self.master, bg="#000000")
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(frame, textvariable=self.question_text, bg="#000000", fg="#FFD700", font=("Roboto", 20, "bold")).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        tk.Entry(frame, textvariable=self.user_answer, width=10, font=("Roboto", 18)).place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        tk.Button(frame, text="Submit Answer", command=self._submit_answer, bg="#FF4397", fg="black", font=("Roboto", 14)).place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        tk.Label(frame, textvariable=self.score_text, bg="#000000", fg="white", font=("Roboto", 12)).place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        tk.Label(frame, textvariable=self.feedback_text, bg="#000000", fg="#FFF8DC", font=("Roboto", 10)).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        tk.Button(frame, text="Back to Menu", command=lambda: self._show_frame("menu"), bg="#444444", fg="white", font=("Roboto", 10)).place(relx=0.5, rely=0.9, anchor=tk.CENTER)

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
