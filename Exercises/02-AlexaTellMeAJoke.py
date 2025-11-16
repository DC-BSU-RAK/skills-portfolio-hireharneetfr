import tkinter as tk
from PIL import Image, ImageTk
import random

BG_IMAGE = r"Resources\images\PHONE.png"
BG2_IMAGE = r"Resources\images\PHONE2.png"
RANDOM_JOKES = r"Resources\randomJokes.txt"

root = tk.Tk()
root.title("02 AlexaTellMeAJoke")
root.geometry("430x800")
root.resizable(False, False)

img = Image.open(BG_IMAGE)
img = img.resize((430, 800))
bg_photo = ImageTk.PhotoImage(img)

bg = tk.Label(root, image=bg_photo)
bg.place(x=0, y=0, relwidth=1, relheight=1)

jokes = []
current_joke = None 

with open(RANDOM_JOKES, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        q_index = line.find("?")
        if q_index != -1:
            setup = line[:q_index + 1].strip()
            punch = line[q_index + 1 :].strip()
        else:
            setup = line
            punch = ""
        jokes.append((setup, punch))

#For the below wrap joke code i asked assistance from chatgpt to make sure that the joke fits inside the notification UI.
#What was asked: I want the text to fit inside the notification bar which is in the background, how can i do tht? here is my code for your reference

def wrap_joke(text, max_chars=34):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > max_chars:
            lines.append(current_line)
            current_line = word
        else: 
            if current_line == "":
                current_line = word
            else: 
                current_line += " " + word 
    
    if current_line:
        lines.append(current_line)

    return "/n".join(lines)

question_label = tk.Label(
    root,
    text="Wanna hear something funny?",
    bg="#ebeae8",
    fg="#484848",
    font=("Roboto", 11),
    wraplength=248
)
question_label.place(x=110, y=348)

yes_button = tk.Label(
    root,
    text="Yes",
    bg="#ebeae8",
    fg="#007AFF",
    font=("Roboto", 11),
    cursor="hand2"
)
yes_button.place(x=110, y=374)

punchline_label = tk.Label(root,
    text="",
    bg="#ebeae8",
    fg="#484848",
    font=("Roboto", 11),
    wraplength=248,
    justify="left")

quit_label = tk.Label(
    root,
    text="Quit",
    bg="#ebeae8",
    fg="#FF3B30",        
    font=("Roboto", 11),
    cursor="hand2"
)

quit_label.bind("<Button-1>", lambda e: root.destroy())

def expand_notification():
    global bg_photo
    img = Image.open(BG2_IMAGE)
    img = img.resize((430,800))
    bg_photo = ImageTk.PhotoImage(img)
    bg.config(image=bg_photo)
    question_label.place(x=110, y=360)
    yes_button.place(x=110, y=430)
    punchline_label.place(x=110, y=470)

def show_new_joke(event=None):
    expand_notification()
    global current_joke
    current_joke = random.choice(jokes)
    setup, _ = current_joke
    question_label.config(text=setup)
    punchline_label.config(text="")
    punchline_label.place(x=110, y=400)
    quit_label.place_forget()             
    yes_button.config(text="Show punchline")
    yes_button.bind("<Button-1>", show_punchline)

def show_punchline(event=None):
    if not current_joke:
        return
    _, punch = current_joke
    punchline_label.config(text=wrap_joke(punch))

    yes_button.config(text="Another joke")
    yes_button.bind("<Button-1>", show_new_joke)
    quit_label.place(x=250, y=400)

yes_button.bind("<Button-1>", show_new_joke)

root.mainloop()

