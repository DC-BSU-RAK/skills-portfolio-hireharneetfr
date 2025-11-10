import tkinter as tk 
import tkinter.messagebox as msgbox 
import sys 
EASY_RANGE = (1, 9) 
MODERATE_RANGE = (10, 99) 
ADVANCED_RANGE = (1000, 9999) 

class MathsQuizApp: 
    
    def __init__(self, master): 
        self.master = master 
        self.master.title("01- Maths Quiz!") 
        self.master.geometry("450x300") 
        self.master.resizable(False, False) 
        self.master.configure(bg="#000000") 

        self.difficulty_level = None 
        self.current_question = 0 
        self.score = 0 
        self.current_answer = None 
        self.chances_left = 2 
        self.current_num1 = 0 
        self.current_num2 = 0 
        self.current_operation = '' #
        
        self.question_text = tk.StringVar(master, value="Select Difficulty Level") 
        self.feedback_text = tk.StringVar(master, value="Welcome to the Maths Quiz!") 
        self.score_text = tk.StringVar(master, value="Score: 0") 
        self.user_answer = tk.StringVar() 

        
        self.frames = {} 
        self.frames["menu"] = self._create_menu_frame() 
        
        
        self._show_frame("menu") 

    def _show_frame(self, page_name): 
  
        frame = self.frames[page_name] 
        frame.tkraise() 

    
    def _create_menu_frame(self): #
        frame = tk.Frame(self.master, bg="#000000") 
        frame.place(x=0, y=0, relwidth=1, relheight=1) 

        tk.Label(frame, text="DIFFICULTY LEVEL", bg="#000000", fg="white", font=("Roboto", 16, "bold")).pack(pady=20) 
        
        tk.Button(frame, text="1. Easy (Single Digit)", command=lambda: print("Easy selected (Placeholder)"), bg="#FF4397", fg="black", font=("Roboto", 12)).pack(pady=5, ipadx=10) 
        tk.Button(frame, text="2. Moderate (Double Digit)", command=lambda: print("Moderate selected (Placeholder)"), bg="#FF0073", fg="black", font=("Roboto", 12)).pack(pady=5, ipadx=10) 
        tk.Button(frame, text="3. Advanced (4-Digit)", command=lambda: print("Advanced selected (Placeholder)"), bg="#F6197C", fg="black", font=("Roboto", 12)).pack(pady=5, ipadx=10) 
        
        return frame 

if __name__ == '__main__': 
    root = tk.Tk() 
    app = MathsQuizApp(root) 
    root.mainloop() 