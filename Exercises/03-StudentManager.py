import tkinter as tk 
from PIL import Image, ImageTk 

IMAGE1 = r"Resources\images\StudentManager.png"
IMAGE2 = r"Resources\images\StudentManager2.png"

class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("03 - Student Manager")
        self.master.geometry("1000x580")
        self.master.resizable(False, False)

        img1 = Image.open(IMAGE1).resize((1000, 580))
        img2 = Image.open(IMAGE2).resize((1000, 580))

        self.bg_photo1 = ImageTk.PhotoImage(img1)
        self.bg_photo2 = ImageTk.PhotoImage(img2)

        self.canvas = tk.Canvas(self.master, width=1000, height=580, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo1)

        self.menu_items = []

        self.make_menu_item("All student records", 230, 255, self.open_page)
        self.make_menu_item("Individual student record", 230, 330, self.open_page)
        self.make_menu_item("Student with highest total score", 230, 400, self.open_page)
        self.make_menu_item("Student with lowest total score", 230, 460, self.open_page)
        self.make_menu_item("Sort student records", 520, 255, self.open_page)
        self.make_menu_item("Add a student record", 520, 330, self.open_page)
        self.make_menu_item("Delete a student record", 520, 400, self.open_page)
        self.make_menu_item("Update a student record", 520, 460, self.open_page)
        
    def make_menu_item(self, text, x, y, command):
        item = self.canvas.create_text(
            x, y, text=text, anchor="w",
            font=("Georgia", 12, "bold"),
            fill="#ffffff"
        )
        self.canvas.tag_bind(item, "<Button-1>", lambda e: command())
        self.menu_items.append(item)

    def open_page(self):
        self.canvas.itemconfig(self.canvas_bg, image=self.bg_photo2)

        new_positions = [  
            (70, 130),  
            (70, 180),  
            (70, 230),  
            (70, 280),  
            (70, 330),  
            (70, 380),  
            (70, 430),  
            (70, 480),  
        ]

        for item, (x, y) in zip(self.menu_items, new_positions):
            self.canvas.coords(item, x, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
