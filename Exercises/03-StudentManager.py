import tkinter as tk 
from PIL import Image, ImageTk 

IMAGE2 = r"Resources\images\StudentManager2.png"
MARKS = r"Resources\studentMarks.txt"

class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("03 - Student Manager")
        self.master.geometry("1000x580")
        self.master.resizable(False, False)

        img2 = Image.open(IMAGE2).resize((1000, 580))
        self.bg_photo2 = ImageTk.PhotoImage(img2)

        self.canvas = tk.Canvas(self.master, width=1000, height=580, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo2)

        self.menu_items = []
        self.data_items = []         
        self.students = self.load_students()  

        self.make_menu_item("All student records", 70, 60, self.show_all_records)
        self.make_menu_item("Individual student record", 70, 130, self.update_record)
        self.make_menu_item("Student with highest total score", 70, 200, self.update_record)
        self.make_menu_item("Student with lowest total score", 70, 260, self.update_record)
        self.make_menu_item("Sort student records", 70, 320, self.update_record)
        self.make_menu_item("Add a student record", 70, 380, self.update_record)
        self.make_menu_item("Delete a student record", 70, 450, self.update_record)
        self.make_menu_item("Update a student record", 70, 520, self.update_record)
        
    def make_menu_item(self, text, x, y, command):
        item = self.canvas.create_text(
            x, y, text=text, anchor="w",
            font=("Georgia", 12, "bold"),
            fill="#ffffff"
        )
        self.canvas.tag_bind(item, "<Button-1>", lambda e: command())
        self.menu_items.append(item)
     
    def load_students(self): 
        students = []
        with open(MARKS, "r") as file:
            lines = file.readlines()

        for line in lines[1:]:
            data = line.strip().split(",")
            sid = data[0]
            name = data[1]
            c1 = int(data[2])
            c2 = int(data[3])
            c3 = int(data[4])
            exam = int(data[5])

            cw_total = c1 + c2 + c3
            percent = ((cw_total + exam) / 160) * 100

            if percent >= 70:
                grade = "A"
            elif percent >= 60:
                grade = "B"
            elif percent >= 50:
                grade = "C"
            elif percent >= 40:
                grade = "D"
            else:
                grade = "F"

            students.append([sid, name, cw_total, exam, percent, grade])

        return students
    
    def clear_data(self): 
        for item in self.data_items:
            self.canvas.delete(item)
        self.data_items = []
        
    def show_all_records(self):     
        self.clear_data()

        students = self.students

        x = 360
        y = 180
        gap = 26

        header = "Name                Number   CW   Exam   %     Grade"
        h = self.canvas.create_text(x, y, text=header, anchor="w",
                                    font=("Courier New", 12, "bold"), fill="white")
        self.data_items.append(h)

        y += gap

        total = 0

        for s in students:
            row = f"{s[1]:20} {s[0]:7}  {s[2]:3}   {s[3]:4}   {s[4]:6.2f}   {s[5]}"
            item = self.canvas.create_text(x, y, text=row, anchor="w",
                                           font=("Courier New", 11), fill="white")
            self.data_items.append(item)
            y += gap
            total += s[4]

        avg = total / len(students)

        s1 = self.canvas.create_text(x, y + 20,
                                     text=f"Total students: {len(students)}",
                                     anchor="w", font=("Georgia", 12, "bold"),
                                     fill="white")
        s2 = self.canvas.create_text(x, y + 50,
                                     text=f"Average percentage: {avg:.2f}%",
                                     anchor="w", font=("Georgia", 12, "bold"),
                                     fill="white")
        self.data_items.extend([s1, s2])

    def show_individual(self): pass
    def show_highest(self): pass
    def show_lowest(self): pass
    def sort_records(self): pass
    def add_record(self): pass
    def delete_record(self): pass
    def update_record(self): pass
    
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
