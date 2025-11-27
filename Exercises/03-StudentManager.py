import tkinter as tk #importing tkinkter 
from PIL import Image, ImageTk #for importing images

# PLEASE NOTE ON AI ASSISTANCE:
# This program was written by me based on the module lecture notes.
# ChatGPT was only used to help debug small issues or help fix errors
# what was said: "what is the error"

IMAGE2 = r"Resources\images\StudentManager2.png" #image2 is now the image in tht specific path
MARKS = r"Resources\studentMarks.txt" #marks is now the image in tht specific path

class StudentManagerApp: #class is being made 
    def __init__(self, master):
        self.master = master
        self.master.title("03 - Student Manager") #title of the window 
        self.master.geometry("1000x580") #size of the window
        self.master.resizable(False, False) #window is notr resizeable 

        img2 = Image.open(IMAGE2).resize((1000, 580)) #image opens and is rezied to fit window 
        self.bg_photo2 = ImageTk.PhotoImage(img2) #convert image for tkinter

        self.canvas = tk.Canvas(self.master, width=1000, height=580, bd=0, highlightthickness=0) #canvas used for background + all text elements
        self.canvas.pack(fill="both", expand=True)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo2) #place bg image

        self.menu_items = [] #lists to track widgets/text to delete when switching menu options
        self.data_items = []         
        self.students = self.load_students() #load students from file at start
        self.sort_buttons = []
        self.other_widgets = []     
        self.entry_widgets = []
        self.search_var = tk.StringVar() #for search box input

        self.make_menu_item("All student records", 170, 60, self.show_all_records) #the buttons on the left
        self.make_menu_item("Individual student record", 170, 128, self.show_individual) 
        self.make_menu_item("Student with highest total score", 170, 196, self.show_highest)
        self.make_menu_item("Student with lowest total score", 170, 261, self.show_lowest)
        self.make_menu_item("Sort student records", 170, 318, self.sort_records)
        self.make_menu_item("Add a student record", 170, 383, self.add_record)
        self.make_menu_item("Delete a student record", 170, 452, self.delete_record)
        self.make_menu_item("Update a student record", 170, 520, self.update_record)


    def make_menu_item(self, text, x, y, command): #creates each left menu button
        item = self.canvas.create_text(
            x, y, text=text, anchor="center",
            font=("Georgia", 12, "bold"),
            fill="#ffffff"
        )
        self.canvas.tag_bind(item, "<Button-1>", lambda e: command()) #makes text clickable
        self.menu_items.append(item)
     
    def load_students(self): #loads students from the text file
        students = []
        with open(MARKS, "r") as file:
            lines = file.readlines()#read every line

        for line in lines[1:]: #skip first line
            data = line.strip().split(",")
            sid = data[0]
            name = data[1]
            c1 = int(data[2])
            c2 = int(data[3])
            c3 = int(data[4])
            exam = int(data[5])

            cw_total = c1 + c2 + c3 #calculate coursework and percentage
            percent = ((cw_total + exam) / 160) * 100

            if percent >= 70: #calculates grade based on percentage
                grade = "A"
            elif percent >= 60:
                grade = "B"
            elif percent >= 50:
                grade = "C"
            elif percent >= 40:
                grade = "D"
            else:
                grade = "F"

            students.append([sid, name, cw_total, exam, percent, grade]) #append each student list

        return students #return full student list
    
    def clear_data(self): #clears all displayed records from canvas
        for item in self.data_items:
            self.canvas.delete(item)
        self.data_items = []

        for w in self.entry_widgets: #destroys entry widgets
            w.destroy()
        self.entry_widgets = []

        for w in self.other_widgets:#destroys other widgets 
            w.destroy()
        self.other_widgets = [] #destroys buttons from .place()

    def clear_sort_buttons(self): #clears sorting buttons + placed widgets
        for btn in self.sort_buttons:
            btn.destroy()
        self.sort_buttons = []

        for w in self.entry_widgets:
            w.destroy()
        self.entry_widgets = []

        for w in self.master.place_slaves(): #destroys buttons from .place()
            w.destroy()

#BELOW IS FOR THE BUTTON "SHOW ALL RECORDS"

    def show_all_records(self): #shows all student records on screen 
        self.clear_data() # Remove any previously displayed records
        self.clear_sort_buttons() # Remove sort buttons from previous views
        students = self.students # Loads all student records stored in memory

        x = 360 #starting x-position for writing data
        y = 180 #y postion for writing data
        gap = 26 #line spacing
        
        t = self.canvas.create_text( #the tile 
            x, y - 30,
            text="All Student Records",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
            )
        self.data_items.append(t) # Load all student records stored in memory

        header = "Name                Number   CW   Exam   %     Grade"#Column names 
        h = self.canvas.create_text(x, y, text=header, anchor="w",
                                    font=("Courier New", 12, "bold"), fill="white")
        self.data_items.append(h) #Stores it to clear later

        y += gap #moved cursor down for next row

        total = 0 #variable to calculate average percentage later

        for s in students: #loop through every student in the list
            row = f"{s[1]:20} {s[0]:7}  {s[2]:3}   {s[3]:4}   {s[4]:6.2f}   {s[5]}" #format one students data into neatly spaced columns
            item = self.canvas.create_text(x, y, text=row, anchor="w",
                                           font=("Courier New", 11), fill="white")
            self.data_items.append(item) #stores so it can be cleared later
            y += gap #move down for the next student
            total += s[4] #add this student's percentage to total for avg calculation

        avg = total / len(students)  #calculate class average percentage

        s1 = self.canvas.create_text(x, y + 20, #text showing total number of students
                                     text=f"Total students: {len(students)}", #postion, display total
                                     anchor="w", font=("Georgia", 12, "bold"), #aligns left, font size 
                                     fill="white") #text color
        s2 = self.canvas.create_text(x, y + 50, #text showing average percentage
                                     text=f"Average percentage: {avg:.2f}%", #display average (2 decimals)
                                     anchor="w", font=("Georgia", 12, "bold"),
                                     fill="white")
        self.data_items.extend([s1, s2]) #store both summary items for clearing later

#BELOW IS FOR THE BUTTON "SHOW INDIVIDUALS"

    def show_individual(self): #function to show one student's record
        self.clear_data() #function to show one student's record
        self.clear_sort_buttons() #clear sorting buttons if they were displayed
        x = 360 #starting x-position for drawing text on right side
        y = 180 #starting y-position for drawing text
        t = self.canvas.create_text( #title of this section
            x, y - 30,
            text="View Individual Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
            )
        self.data_items.append(t) #store title so it can be deleted later
        l = self.canvas.create_text( #label asking user to enter name or ID
            x, y,
            text="Enter Student Name or ID:",
            anchor="w",
            font=("Georgia", 11, "bold"),
            fill="white"
            )
        self.data_items.append(l) #store label
        
        e = tk.Entry( #entry box where user types the name or ID
            self.master, #entry inside main window
            textvariable=self.search_var, #binds input to a variable
            font=("Courier New", 11),
            width=30,
            bg="#333333",
            fg="white",
            insertbackground="white"
            )
        e.place(x=x + 220, y=y - 12) #place entry box beside the label
        self.entry_widgets.append(e) #store entry widget for clearing later
        
        b = tk.Button( #search button to trigger searching
            self.master,
            text="Search",
            command=self.search_and_display_record,  #calls search function
            bg="#f296aa",
            fg="white",
            font=("Georgia", 10, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0
            )
        b.place(x=x + 470, y=y - 12) #place button next to entry
        self.other_widgets.append(b) #store so it can be deleted later
        e.bind("<Return>", lambda ev: self.search_and_display_record()) #allows pressing ENTER to trigger search

    def search_and_display_record(self): #function to search and show ONE student
        query = self.search_var.get().strip().lower() #get search text, clean spaces, lowercase
        self.clear_data() #clear old displayed info
        self.clear_sort_buttons() #clear sort buttons too

        x = 360 #starting x-position for display
        y = 180 #starting y-position

        h = self.canvas.create_text( #header row for results
            x, y,
            text="Name                Number   CW   Exam   %     Grade",
            anchor="w",
            font=("Courier New", 12, "bold"),
            fill="white"
        )
        self.data_items.append(h) #store header
        y += 30 #move down for the results

        found = False #flag to track if a match is found

        for s in self.students:  #loop through all students
            if query in s[0].lower() or query in s[1].lower(): #checks if search matches ID or Name (both converted to lowercase)
                row = f"{s[1]:20} {s[0]:7}  {s[2]:3}   {s[3]:4}   {s[4]:6.2f}   {s[5]}" #format the result row cleanly
                r = self.canvas.create_text( #draws the found student's info
                    x, y,
                    text=row,
                    anchor="w",
                    font=("Courier New", 11),
                    fill="white"
                )
                self.data_items.append(r) #store row
                found = True #match was found
                break #stop looping cuz we found the student

        if not found: #if NO student matched the search
            nf = self.canvas.create_text(
                x, y,
                text="No matching student found.",
                anchor="w",
                font=("Georgia", 12, "bold"),
                fill="white"
            )
            self.data_items.append(nf) #store the message

#BELOW IS FOR THE BUTTON "SHOW HIGHEST"

    def show_highest(self): #function to show the student with the highest score
        self.clear_data() #clearS any old displayed records from the right side  
        self.clear_sort_buttons() #remove sorting buttons if they were showing  

        top = max(self.students, key=lambda s: s[4]) #find student with the highest percentage  
        x = 360 #starting x-position for drawing text  
        y = 180 #startnig y postion
        
        header = "Name                Number   CW   Exam   %     Grade"  #header row displayed above the student details  
        h = self.canvas.create_text(x, y, text=header, anchor="w",
                                font=("Courier New", 12, "bold"), fill="white")
        self.data_items.append(h) #store so it can be cleared later  
        y += 30  #move down to draw the student's info  
        info = f"{top[1]:20} {top[0]:7}  {top[2]:3}   {top[3]:4}   {top[4]:6.2f}   {top[5]}" #format the row for the highest scoring student 
        line = self.canvas.create_text(x, y, text=info, anchor="w", #draw the student's information  
                                   font=("Courier New", 11), fill="white")
        self.data_items.append(line) #store for clearing later  
        
        txt = self.canvas.create_text( #title label displayed above the header  
            x, y - 65,
        text="Highest overall scoring student",
        anchor="w",
        font=("Georgia", 13, "bold"),
        fill="white"
        )
        
        self.data_items.append(txt)  #store so it can be deleted later

#BELOW IS FOR THE BUTTON "SHOW LOWEST"

    def show_lowest(self): #function to show the student with the lowest percentage 
        self.clear_data() #clear previously displayed data from the right sid
        self.clear_sort_buttons() #clear sorting buttons if any were visible  

        low = min(self.students, key=lambda s: s[4]) #find the student with the lowest percentage
        x = 360 #starting x-position for drawing text  
        y = 180 #starting y-position
        
        header = "Name                Number   CW   Exam   %     Grade" #header row showing column titles  
        h = self.canvas.create_text(x, y, text=header, anchor="w",
                                font=("Courier New", 12, "bold"), fill="white")
        self.data_items.append(h) #store header for clearing later 
        y += 30 #move down for student data  
        info = f"{low[1]:20} {low[0]:7}  {low[2]:3}   {low[3]:4}   {low[4]:6.2f}   {low[5]}"#formats the lowest scoring student's data into neat columns  
        line = self.canvas.create_text(x, y, text=info, anchor="w", #draw the student's row  
                                   font=("Courier New", 11), fill="white") 
        self.data_items.append(line)#store row so it can be removed later 
        txt = self.canvas.create_text( #section title displayed above the header  
        x, y - 65,
        text="Lowest overall scoring student",
        anchor="w",
        font=("Georgia", 13, "bold"),
        fill="white"
        )
        self.data_items.append(txt)  #store title for clearing 

#BELOW IS FOR THE BUTTON "SHOW RECORDS"

    def sort_records(self):  #function to sort all student records by percentage 
        self.clear_data()#remove any existing displayed data 
        self.clear_sort_buttons() #remove sort buttons if previously shown   

        for w in self.master.place_slaves(): #clear all widgets placed using .place() to avoid overlapping  
            w.destroy()

        label = self.canvas.create_text( #title label for this sorting section
            360, 150,
            text="Sort by overall percentage:",
            anchor="w",
            font=("Georgia", 14, "bold"),
            fill="white"
        ) 
        self.data_items.append(label) #track so it can be cleared later 

        def show_sorted(order):  #function to actually display sorted results  
            self.clear_data() #clear data before drawing new sorted list  

            if order == "asc": #sort list ascending 
                sorted_students = sorted(self.students, key=lambda s: s[4])
            else: 
                sorted_students = sorted(self.students, key=lambda s: s[4], reverse=True)  #sort list descending

            x = 360 #starting x-position  
            y = 180 #starting y-position 
            gap = 26 #line spacing

            header = "Name                Number   CW   Exam   %     Grade" #header row  
            h = self.canvas.create_text(
                x, y,
                text=header,
                anchor="w",
                font=("Courier New", 12, "bold"),
                fill="white"
            )
            self.data_items.append(h) #store header

            y += gap #move down 

            for s in sorted_students: #loop through sorted students and display each row  
                row = f"{s[1]:20} {s[0]:7}  {s[2]:3}   {s[3]:4}   {s[4]:6.2f}   {s[5]}"
                item = self.canvas.create_text(
                    x, y,
                    text=row,
                    anchor="w",
                    font=("Courier New", 11),
                    fill="white"
                )
                self.data_items.append(item)  #store text for later clearing  
                y += gap #move down for next student  

        asc_btn = tk.Button( #button for ascending sort  
            self.master,
            text="Ascending",
            command=lambda: show_sorted("asc"),  #call sorting function  
            bg= "#f296aa",
            fg="white",
            font=("Georgia", 11, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0
        )
        asc_btn.place(x=730, y=140) #place button on screen  
        self.sort_buttons.append(asc_btn)  #store button  
        
        desc_btn = tk.Button( #button for descending sort  
            self.master,
            text="Descending",
            command=lambda: show_sorted("desc"), #call sorting function  
            bg= "#f296aa",
            fg="white",
            font=("Georgia", 11, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0
        )
        desc_btn.place(x=830, y=140) #place button  
        self.sort_buttons.append(desc_btn)  #store button  

#BELOW IS FOR THE BUTTON "ADD RECORD"

    def add_record(self): #function to add a new student into the records
        self.clear_data() #clear any previous displayed text from the right side
        self.clear_sort_buttons() #remove sorting buttons if they were shown earlier

        x = 360 #starting x-position for text and labels
        y = 180 #starting y-position

        title = self.canvas.create_text( #title of the add record section
            x, y - 40,
            text="Add a New Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
        )
        self.data_items.append(title)  #store title for future clearing

        labels = ["Student ID:", "Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam:"] #labels for each data field the user needs to enter
        vars_list = [] #list to store StringVar for each entry field

        for i, text in enumerate(labels): #loop through each label and create entry boxes for them
            lbl = self.canvas.create_text( #draw label text on canvas
                x, y + (i * 40),
                text=text,
                anchor="w",
                font=("Georgia", 11, "bold"),
                fill="white"
            )
            self.data_items.append(lbl) #store label so it can be removed later

            v = tk.StringVar()  #create variable to store user input
            entry = tk.Entry(
                self.master, #entry inside main window (not canvas)
                textvariable=v,
                font=("Courier New", 11),
                width=25,
                bg="#333333",
                fg="white",
                insertbackground="white"
            )
            entry.place(x=x + 200, y=y - 12 + (i * 40))#place entry aligned with label
            self.entry_widgets.append(entry) #store entry so it can be cleared later
            vars_list.append(v) #store variable reference

        def save_record(): #function that saves the student record into the list + file
            sid = vars_list[0].get().strip() #all the functions 
            name = vars_list[1].get().strip()
            c1 = int(vars_list[2].get().strip())
            c2 = int(vars_list[3].get().strip())
            c3 = int(vars_list[4].get().strip())
            exam = int(vars_list[5].get().strip())

            cw_total = c1 + c2 + c3 #total coursework marks out of 60
            percent = ((cw_total + exam) / 160) * 100  #calculate overall percentage

            if percent >= 70: #Checks grade based on percentage
                grade = "A"
            elif percent >= 60:
                grade = "B"
            elif percent >= 50:
                grade = "C"
            elif percent >= 40:
                grade = "D"
            else:
                grade = "F"

            self.students.append([sid, name, cw_total, exam, percent, grade]) #add new student to the in-memory list

            with open(MARKS, "a") as f:  #appends to the studentMarks.txt file
                f.write(f"\n{sid},{name},{c1},{c2},{c3},{exam}")

            msg = self.canvas.create_text( #confirmation message on canvas
                x, y + 280,
                text="Record added successfully!",
                anchor="w",
                font=("Georgia", 12, "bold"),
                fill="white"
            )
            self.data_items.append(msg) #store for clearing later

        btn = tk.Button( #button to save the new student record
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
            padx=10, #internal padding (left-right)
            pady=5 #internal padding (top-bottom)
        )

        btn.place(x=x + 200, y=y + 240) #place button under the entries
        self.other_widgets.append(btn) #store button so it can be deleted later

#BELOW IS FOR THE BUTTON "DELETE RECORD"
    
    def delete_record(self): #function to delete a student record
        self.clear_data() #clear the canvas of previous data
        self.clear_sort_buttons() #remove any sorting buttons

        x = 360  #starting x-position for text
        y = 180 #starting y-position

        t = self.canvas.create_text( #title of this delete section
            x, y - 40,
            text="Delete a Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
        )
        self.data_items.append(t) #store for clearing later

        lbl = self.canvas.create_text(  #label prompting user for ID or name to delete
            x, y,
            text="Enter Student Name or ID:",
            anchor="w",
            font=("Georgia", 11, "bold"),
            fill="white"
        )
        self.data_items.append(lbl) #store label

        delete_var = tk.StringVar() #variable for user input
        entry = tk.Entry( #entry box for entering student ID or name    
            self.master,
            textvariable=delete_var,
            font=("Courier New", 11),
            width=30,
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        entry.place(x=x + 220, y=y - 12) #place beside label
        self.entry_widgets.append(entry)  #store entry

        def perform_delete(): #this inner function performs the actual deletion
            query = delete_var.get().strip().lower() #get input, clean, lowercase
            found = None #variable to store matching student
            for s in self.students:
                if query in s[0].lower() or query in s[1].lower(): #get input, clean, lowercase
                    found = s 
                    break  #student found

            if found:
                self.students.remove(found) #remove from memory list

                with open(MARKS, "r") as f:  #read all lines in file
                    lines = f.readlines()

                with open(MARKS, "w") as f:  #rewrite file except the deleted student
                    for line in lines:
                        if not (found[0] in line or found[1].lower() in line.lower()):
                            f.write(line)

                msg = self.canvas.create_text( #success message
                    x, y + 90,
                    text="Record deleted successfully.",
                    anchor="w",
                    font=("Georgia", 12, "bold"),
                    fill="white"
                )
                self.data_items.append(msg)
            else: 
                msg = self.canvas.create_text( #message when no student matches the query
                    x, y + 80,
                    text="No matching student found.",
                    anchor="w",
                    font=("Georgia", 12, "bold"),
                    fill="white"
                )
                self.data_items.append(msg)

        btn = tk.Button( #button to delete the student
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
        btn.place(x=x + 220, y=y + 40) #place button under entry box
        self.other_widgets.append(btn) #store button

        entry.bind("<Return>", lambda ev: perform_delete()) #press enter to delete

#BELOW IS FOR THE BUTTON "UPDATE RECORD "

    def update_record(self): #function to update an existing student record
        self.clear_data() #clear all displayed items from the canvas
        self.clear_sort_buttons() #remove sorting buttons if they were displayed

        x = 360 #starting x-position for drawing text
        y = 180 #starting y-position

        title = self.canvas.create_text( #title for this section
            x, y - 40,
            text="Update a Student Record",
            anchor="w",
            font=("Georgia", 13, "bold"),
            fill="white"
        )
        self.data_items.append(title)  #store for clearing later

        search_var = tk.StringVar() #variable to store search input

        lbl = self.canvas.create_text( #label instructing the user what to enter
            x, y,
            text="Enter Student Name or ID:",
            anchor="w",
            font=("Georgia", 11, "bold"),
            fill="white"
        )
        self.data_items.append(lbl) #store label

        entry = tk.Entry( #entry box for entering the search query
            self.master,
            textvariable=search_var,
            font=("Courier New", 11),
            width=30,
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        entry.place(x=x + 220, y=y - 12) #place next to label
        self.entry_widgets.append(entry) #store entry box

        form_vars = [] #this will store variables for editing fields
 
        def load_edit_fields(s):
            labels = ["Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam:"] #labels for editing
            values = [s[1], "", "", "", ""]  #default prefilled values (only name is prefilled)

            for i, text in enumerate(labels): #create labels + entries for each editable field
                lbl2 = self.canvas.create_text(
                    x, y + 60 + (i * 40),
                    text=text,
                    anchor="w",
                    font=("Georgia", 11, "bold"),
                    fill="white"
                )
                self.data_items.append(lbl2) #store label

                v = tk.StringVar() #variable for editing field
                if i == 0:
                    v.set(s[1]) #prefill name field
                form_vars.append(v) #store variable

                e = tk.Entry(
                    self.master,
                    textvariable=v,
                    font=("Courier New", 11),
                    width=25,
                    bg="#333333",
                    fg="white",
                    insertbackground="white"
                )
                e.place(x=x + 200, y=y + 48 + (i * 40)) #position entry next to label
                self.entry_widgets.append(e)  #store entry

            def apply_update():
                new_name = form_vars[0].get().strip() #updated name input
                c1 = int(form_vars[1].get().strip() or s[2] - (s[3] + s[4] if False else 0))   #updated coursework marks 
                c2 = int(form_vars[2].get().strip() or 0)
                c3 = int(form_vars[3].get().strip() or 0)
                exam = int(form_vars[4].get().strip() or s[3]) #updated exam marks

                cw_total = c1 + c2 + c3 #recalculate coursework total
                percent = ((cw_total + exam) / 160) * 100 #recalculate percentage

                if percent >= 70: #recalculate grade using same logic as load_students
                    grade = "A"
                elif percent >= 60:
                    grade = "B"
                elif percent >= 50:
                    grade = "C"
                elif percent >= 40:
                    grade = "D"
                else:
                    grade = "F"

                s[1] = new_name #update VALUES inside the student data list stored in memory
                s[2] = cw_total 
                s[3] = exam
                s[4] = percent
                s[5] = grade

                with open(MARKS, "r") as f:
                    lines = f.readlines() #read all lines

                with open(MARKS, "w") as f:
                    for line in lines:
                        if s[0] in line: #if this is the student we updated
                            f.write(f"{s[0]},{new_name},{c1},{c2},{c3},{exam}\n") #write updated version
                        else:
                            f.write(line) #write the original line

                msg = self.canvas.create_text( #success message
                    x, y + 300,
                    text="Record updated successfully!",
                    anchor="w",
                    font=("Georgia", 12, "bold"),
                    fill="white"
                )
                self.data_items.append(msg) #store message

            btn2 = tk.Button(#button to save updated info
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
            btn2.place(x=x + 200, y=y + 250) #place save button
            self.other_widgets.append(btn2) #store button for clearing

        def search_student():
            q = search_var.get().strip().lower() #user input cleaned + lowered
            for s in self.students: 
                if q in s[0].lower() or q in s[1].lower(): #match by name or ID
                    load_edit_fields(s) #load fields for editing
                    return  #stop after match

            msg = self.canvas.create_text( #if student not found, show message
                x, y + 60,
                text="No matching student found.",
                anchor="w",
                font=("Georgia", 12, "bold"),
                fill="white"
            )
            self.data_items.append(msg) #store message

        search_btn = tk.Button(  #button to trigger searching   
            self.master,
            text="Search",
            command=search_student,  #function to search student
            bg="#f296aa",
            fg="white",
            font=("Georgia", 9, "bold"),
            relief="flat",
            border=0,
            highlightthickness=0,
            padx=6,
            pady=2
        )
        search_btn.place(x=x + 470, y=y - 12)  #place button next to entry
        self.other_widgets.append(search_btn) #store button

        entry.bind("<Return>", lambda ev: search_student())  #pressing ENTER also triggers search

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)  #creates an instance of the class
    root.mainloop() #keeps the window opened
