import tkinter as tk 
from PIL import Image, ImageTk

# PLEASE NOTE ON AI ASSISTANCE:
# This program was written by me based on the module lecture notes.
# ChatGPT was only used to help debug small issues or help fix errors
# what was said: "what is the error"

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
        self.sort_buttons = []
        self.other_widgets = []     
        self.entry_widgets = []
        self.search_var = tk.StringVar() 

        self.make_menu_item("All student records", 170, 60, self.show_all_records)
        self.make_menu_item("Individual student record", 170, 128, self.show_individual)
        self.make_menu_item("Student with highest total score", 170, 196, self.show_highest)
        self.make_menu_item("Student with lowest total score", 170, 261, self.show_lowest)
        self.make_menu_item("Sort student records", 170, 318, self.sort_records)
        self.make_menu_item("Add a student record", 170, 383, self.add_record)
        self.make_menu_item("Delete a student record", 170, 452, self.delete_record)
        self.make_menu_item("Update a student record", 170, 520, self.update_record)


    def make_menu_item(self, text, x, y, command):
        item = self.canvas.create_text(
            x, y, text=text, anchor="center",
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

        for w in self.entry_widgets:
            w.destroy()
        self.entry_widgets = []

        for w in self.other_widgets:
            w.destroy()
        self.other_widgets = []

    def clear_sort_buttons(self):
        for btn in self.sort_buttons:
            btn.destroy()
        self.sort_buttons = []

        for w in self.entry_widgets:
            w.destroy()
        self.entry_widgets = []

        for w in self.master.place_slaves():    
            w.destroy()

#SHOW ALL RECORDSSS

    def show_all_records(self):  
        self.clear_data()
        self.clear_sort_buttons()    
        students = self.students

        x = 360
        y = 180
        gap = 26
        
        t = self.canvas.create_text(
            x, y - 30,
            text="All Student Records",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
            )
        self.data_items.append(t)

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

#show individuallllllllllll

    def show_individual(self):
        self.clear_data()
        self.clear_sort_buttons()
        x = 360
        y = 180
        t = self.canvas.create_text(
            x, y - 30,
            text="View Individual Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
            )
        self.data_items.append(t)
        l = self.canvas.create_text(
            x, y,
            text="Enter Student Name or ID:",
            anchor="w",
            font=("Georgia", 11, "bold"),
            fill="white"
            )
        self.data_items.append(l)
        
        e = tk.Entry(
            self.master,
            textvariable=self.search_var,
            font=("Courier New", 11),
            width=30,
            bg="#333333",
            fg="white",
            insertbackground="white"
            )
        e.place(x=x + 220, y=y - 12)
        self.entry_widgets.append(e)
        
        b = tk.Button(
            self.master,
            text="Search",
            command=self.search_and_display_record,
            bg="#f296aa",
            fg="white",
            font=("Georgia", 10, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0
            )
        b.place(x=x + 470, y=y - 12)
        self.other_widgets.append(b)
        e.bind("<Return>", lambda ev: self.search_and_display_record())


    def search_and_display_record(self):
        query = self.search_var.get().strip().lower()
        self.clear_data()
        self.clear_sort_buttons()

        x = 360
        y = 180

        h = self.canvas.create_text(
            x, y,
            text="Name                Number   CW   Exam   %     Grade",
            anchor="w",
            font=("Courier New", 12, "bold"),
            fill="white"
        )
        self.data_items.append(h)
        y += 30

        found = False

        for s in self.students:
            if query in s[0].lower() or query in s[1].lower():
                row = f"{s[1]:20} {s[0]:7}  {s[2]:3}   {s[3]:4}   {s[4]:6.2f}   {s[5]}"
                r = self.canvas.create_text(
                    x, y,
                    text=row,
                    anchor="w",
                    font=("Courier New", 11),
                    fill="white"
                )
                self.data_items.append(r)
                found = True
                break

        if not found:
            nf = self.canvas.create_text(
                x, y,
                text="No matching student found.",
                anchor="w",
                font=("Georgia", 12, "bold"),
                fill="white"
            )
            self.data_items.append(nf)

# SHOW HIGHESTTTTTTTTTTTTT

    def show_highest(self):  
        self.clear_data()
        self.clear_sort_buttons()

        top = max(self.students, key=lambda s: s[4])
        x = 360
        y = 180
        
        header = "Name                Number   CW   Exam   %     Grade"
        h = self.canvas.create_text(x, y, text=header, anchor="w",
                                font=("Courier New", 12, "bold"), fill="white")
        self.data_items.append(h)
        y += 30
        info = f"{top[1]:20} {top[0]:7}  {top[2]:3}   {top[3]:4}   {top[4]:6.2f}   {top[5]}"
        line = self.canvas.create_text(x, y, text=info, anchor="w",
                                   font=("Courier New", 11), fill="white")
        self.data_items.append(line)
        
        txt = self.canvas.create_text(
            x, y - 65,
        text="Highest overall scoring student",
        anchor="w",
        font=("Georgia", 13, "bold"),
        fill="white"
        )
        
        self.data_items.append(txt)
# SHOW LOWESTTTTTTTTTTTTTTT

    def show_lowest(self):  
        self.clear_data()
        self.clear_sort_buttons()
        low = min(self.students, key=lambda s: s[4])
        x = 360
        y = 180
        
        header = "Name                Number   CW   Exam   %     Grade"
        h = self.canvas.create_text(x, y, text=header, anchor="w",
                                font=("Courier New", 12, "bold"), fill="white")
        self.data_items.append(h)
        y += 30
        info = f"{low[1]:20} {low[0]:7}  {low[2]:3}   {low[3]:4}   {low[4]:6.2f}   {low[5]}"
        line = self.canvas.create_text(x, y, text=info, anchor="w",
                                   font=("Courier New", 11), fill="white")
        self.data_items.append(line)
        txt = self.canvas.create_text(
        x, y - 65,
        text="Lowest overall scoring student",
        anchor="w",
        font=("Georgia", 13, "bold"),
        fill="white"
        )
        self.data_items.append(txt)

#SORT RECORDDDDDDDDDDDDDDDDDD

    def sort_records(self): 
        self.clear_data()
        self.clear_sort_buttons()   

        for w in self.master.place_slaves():
            w.destroy()

        label = self.canvas.create_text(
            360, 150,
            text="Sort by overall percentage:",
            anchor="w",
            font=("Georgia", 14, "bold"),
            fill="white"
        )
        self.data_items.append(label)

        def show_sorted(order): 
            self.clear_data()

            if order == "asc":
                sorted_students = sorted(self.students, key=lambda s: s[4])
            else:
                sorted_students = sorted(self.students, key=lambda s: s[4], reverse=True)

            x = 360
            y = 180
            gap = 26

            header = "Name                Number   CW   Exam   %     Grade"
            h = self.canvas.create_text(
                x, y,
                text=header,
                anchor="w",
                font=("Courier New", 12, "bold"),
                fill="white"
            )
            self.data_items.append(h)

            y += gap

            for s in sorted_students:
                row = f"{s[1]:20} {s[0]:7}  {s[2]:3}   {s[3]:4}   {s[4]:6.2f}   {s[5]}"
                item = self.canvas.create_text(
                    x, y,
                    text=row,
                    anchor="w",
                    font=("Courier New", 11),
                    fill="white"
                )
                self.data_items.append(item)
                y += gap

        asc_btn = tk.Button(
            self.master,
            text="Ascending",
            command=lambda: show_sorted("asc"),
            bg= "#f296aa",
            fg="white",
            font=("Georgia", 11, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0
        )
        asc_btn.place(x=730, y=140)
        self.sort_buttons.append(asc_btn)
        
        desc_btn = tk.Button(
            self.master,
            text="Descending",
            command=lambda: show_sorted("desc"),
            bg= "#f296aa",
            fg="white",
            font=("Georgia", 11, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0
        )
        desc_btn.place(x=830, y=140)
        self.sort_buttons.append(desc_btn)

#ADDD RECORDDDDDDDDDDDDDDDD 

    def add_record(self):
        self.clear_data()
        self.clear_sort_buttons()

        x = 360
        y = 180

        title = self.canvas.create_text(
            x, y - 40,
            text="Add a New Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
        )
        self.data_items.append(title)

        labels = ["Student ID:", "Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam:"]
        vars_list = []

        for i, text in enumerate(labels):
            lbl = self.canvas.create_text(
                x, y + (i * 40),
                text=text,
                anchor="w",
                font=("Georgia", 11, "bold"),
                fill="white"
            )
            self.data_items.append(lbl)

            v = tk.StringVar()
            entry = tk.Entry(
                self.master,
                textvariable=v,
                font=("Courier New", 11),
                width=25,
                bg="#333333",
                fg="white",
                insertbackground="white"
            )
            entry.place(x=x + 200, y=y - 12 + (i * 40))
            self.entry_widgets.append(entry)
            vars_list.append(v)

        def save_record():
            sid = vars_list[0].get().strip()
            name = vars_list[1].get().strip()
            c1 = int(vars_list[2].get().strip())
            c2 = int(vars_list[3].get().strip())
            c3 = int(vars_list[4].get().strip())
            exam = int(vars_list[5].get().strip())

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

            self.students.append([sid, name, cw_total, exam, percent, grade])

            with open(MARKS, "a") as f:
                f.write(f"\n{sid},{name},{c1},{c2},{c3},{exam}")

            msg = self.canvas.create_text(
                x, y + 280,
                text="Record added successfully!",
                anchor="w",
                font=("Georgia", 12, "bold"),
                fill="white"
            )
            self.data_items.append(msg)

        btn = tk.Button(
            self.master,
            text="Add Record",
            command=save_record,
            bg="#f296aa",     
            fg="white",
            font=("Georgia", 11, "bold"),
            relief="flat",
            activebackground="#f296aa",
            activeforeground="white",
            border=0,
            highlightthickness=0,
            padx=10,
            pady=5
        )

        btn.place(x=x + 200, y=y + 240)
        self.other_widgets.append(btn)

#DELTE RECORDDD
    
    def delete_record(self):
        self.clear_data()
        self.clear_sort_buttons()

        x = 360
        y = 180

        t = self.canvas.create_text(
            x, y - 40,
            text="Delete a Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
        )
        self.data_items.append(t)

        lbl = self.canvas.create_text(
            x, y,
            text="Enter Student Name or ID:",
            anchor="w",
            font=("Georgia", 11, "bold"),
            fill="white"
        )
        self.data_items.append(lbl)

        delete_var = tk.StringVar()
        entry = tk.Entry(
            self.master,
            textvariable=delete_var,
            font=("Courier New", 11),
            width=30,
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        entry.place(x=x + 220, y=y - 12)
        self.entry_widgets.append(entry)

        def perform_delete():
            query = delete_var.get().strip().lower()
            found = None
            for s in self.students:
                if query in s[0].lower() or query in s[1].lower():
                    found = s
                    break

            if found:
                self.students.remove(found)

                with open(MARKS, "r") as f:
                    lines = f.readlines()

                with open(MARKS, "w") as f:
                    for line in lines:
                        if not (found[0] in line or found[1].lower() in line.lower()):
                            f.write(line)

                msg = self.canvas.create_text(
                    x, y + 90,
                    text="Record deleted successfully.",
                    anchor="w",
                    font=("Georgia", 12, "bold"),
                    fill="white"
                )
                self.data_items.append(msg)
            else:
                msg = self.canvas.create_text(
                    x, y + 80,
                    text="No matching student found.",
                    anchor="w",
                    font=("Georgia", 12, "bold"),
                    fill="white"
                )
                self.data_items.append(msg)

        btn = tk.Button(
            self.master,
            text="Delete Record",
            command=perform_delete,
            bg="#f296aa",
            fg="white",
            font=("Georgia", 11, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0,
            padx=10,
            pady=5
        )
        btn.place(x=x + 220, y=y + 40)
        self.other_widgets.append(btn)

        entry.bind("<Return>", lambda ev: perform_delete())

#update recorddd

    def update_record(self):
        self.clear_data()
        self.clear_sort_buttons()

        x = 360
        y = 180

        title = self.canvas.create_text(
            x, y - 40,
            text="Update a Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
        )
        self.data_items.append(title)

        search_var = tk.StringVar()

        lbl = self.canvas.create_text(
            x, y,
            text="Enter Student Name or ID:",
            anchor="w",
            font=("Georgia", 11, "bold"),
            fill="white"
        )
        self.data_items.append(lbl)

        entry = tk.Entry(
            self.master,
            textvariable=search_var,
            font=("Courier New", 11),
            width=30,
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        entry.place(x=x + 220, y=y - 12)
        self.entry_widgets.append(entry)

        form_vars = []

        def load_edit_fields(s):
            labels = ["Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam:"]
            values = [s[1], "", "", "", ""]

            for i, text in enumerate(labels):
                lbl2 = self.canvas.create_text(
                    x, y + 60 + (i * 40),
                    text=text,
                    anchor="w",
                    font=("Georgia", 11, "bold"),
                    fill="white"
                )
                self.data_items.append(lbl2)

                v = tk.StringVar()
                if i == 0:
                    v.set(s[1])
                form_vars.append(v)

                e = tk.Entry(
                    self.master,
                    textvariable=v,
                    font=("Courier New", 11),
                    width=25,
                    bg="#333333",
                    fg="white",
                    insertbackground="white"
                )
                e.place(x=x + 200, y=y + 48 + (i * 40))
                self.entry_widgets.append(e)

            def apply_update():
                new_name = form_vars[0].get().strip()
                c1 = int(form_vars[1].get().strip() or s[2] - (s[3] + s[4] if False else 0))
                c2 = int(form_vars[2].get().strip() or 0)
                c3 = int(form_vars[3].get().strip() or 0)
                exam = int(form_vars[4].get().strip() or s[3])

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

                s[1] = new_name
                s[2] = cw_total
                s[3] = exam
                s[4] = percent
                s[5] = grade

                with open(MARKS, "r") as f:
                    lines = f.readlines()

                with open(MARKS, "w") as f:
                    for line in lines:
                        if s[0] in line:
                            f.write(f"{s[0]},{new_name},{c1},{c2},{c3},{exam}\n")
                        else:
                            f.write(line)

                msg = self.canvas.create_text(
                    x, y + 300,
                    text="Record updated successfully!",
                    anchor="w",
                    font=("Georgia", 12, "bold"),
                    fill="white"
                )
                self.data_items.append(msg)

            btn2 = tk.Button(
                self.master,
                text="Save Changes",
                command=apply_update,
                bg="#f296aa",
                fg="white",
                font=("Georgia", 11, "bold"),
                relief="flat",
                border=0,
                highlightthickness=0,
                padx=10,
                pady=5
            )
            btn2.place(x=x + 200, y=y + 250)
            self.other_widgets.append(btn2)

        def search_student():
            q = search_var.get().strip().lower()
            for s in self.students:
                if q in s[0].lower() or q in s[1].lower():
                    load_edit_fields(s)
                    return

            msg = self.canvas.create_text(
                x, y + 60,
                text="No matching student found.",
                anchor="w",
                font=("Georgia", 12, "bold"),
                fill="white"
            )
            self.data_items.append(msg)

        search_btn = tk.Button(
            self.master,
            text="Search",
            command=search_student,
            bg="#f296aa",
            fg="white",
            font=("Georgia", 9, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0,
            padx=6,
            pady=2
        )
        search_btn.place(x=x + 470, y=y - 12)
        self.other_widgets.append(search_btn)

        entry.bind("<Return>", lambda ev: search_student())


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop() 
