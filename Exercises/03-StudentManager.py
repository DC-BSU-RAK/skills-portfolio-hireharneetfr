import tkinter as tk  
from tkinter import messagebox 


STUDENT_FILE = r"Resources\studentMarks.txt"

class StudentManagerApp:  
    def __init__(self, master):
        self.master = master
        self.master.title("03 - Student Manager")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        self.master.configure(bg="#FCE2E6") 
        self.students = []

        self.build_main_menu()

    def build_main_menu(self):
        title_label = tk.Label(
            self.master,
            text="Student Manager",
            font=("Roboto", 22, "bold"),
            bg="#FCE2E6"
        )
        title_label.pack(pady=20)

        info_label = tk.Label(
            self.master,
            text="Student Records",
            font=("Roboto", 10),
            bg="#FCE2E6"
        )
        info_label.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
