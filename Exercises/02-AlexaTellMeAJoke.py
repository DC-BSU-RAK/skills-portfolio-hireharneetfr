import tkinter as tk
from PIL import Image, ImageTk   

BG_IMAGE = r"Resources\images\PHONE.png"   

root = tk.Tk()
root.title("02 AlexaTellMeAJoke")
root.geometry("430x800")
root.resizable(False, False)

# --- Background image ---
img = Image.open(BG_IMAGE)
img = img.resize((430, 800))
bg_photo = ImageTk.PhotoImage(img)

bg = tk.Label(root, image=bg_photo)
bg.place(x=0, y=0, relwidth=1, relheight=1)

# --- Question text ---
question_label = tk.Label(
    root,
    text="Wanna hear something funny?",
    bg="#ebeae8",
    fg="#484848",
    font=("Roboto", 11)
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

def on_yes(event=None):
    question_label.config(text="BlehBleh!")

yes_button.bind("<Button-1>", on_yes)

root.mainloop()
