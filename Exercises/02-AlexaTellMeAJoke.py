import tkinter as tk #importing tkinter
from PIL import Image, ImageTk #to import images
import random #choosing random jokes
# PLEASE NOTE ON AI ASSISTANCE:

# This program was written by me based on the module lecture notes.
# ChatGPT was only used to help debug small issues or help fix errors
# what was said: "what is the error"

BG_IMAGE = r"Resources\images\PHONE.png" #small notification image
BG2_IMAGE = r"Resources\images\PHONE2.png" #a little bigger notification image
RANDOM_JOKES = r"Resources\randomJokes.txt" #text file of jokes

root = tk.Tk() #making the main vwindow
root.title("02 AlexaTellMeAJoke") #window title
root.geometry("430x800") #size of the window 
root.resizable(False, False) #window is not resizable

img = Image.open(BG_IMAGE) #opening the background
img = img.resize((430, 800)) #making sure the size fits window
bg_photo = ImageTk.PhotoImage(img) #converting image 

bg = tk.Label(root, image=bg_photo) #to display the image
bg.place(x=0, y=0, relwidth=1, relheight=1) #placing the background

jokes = [] #to store all the jokes
current_joke = None #holds the current joke

with open(RANDOM_JOKES, "r", encoding="utf-8") as f: #opens the joke file
    for line in f: #loops through each line 
        line = line.strip() #removes the spaces
        if not line: #skips empty lines
            continue
        q_index = line.find("?") #checks where the question mark is
        if q_index != -1: #if the joke has ?
            setup = line[:q_index + 1].strip() #everything until the ? is the setup joke
            punch = line[q_index + 1 :].strip() #everything after the? is the punchline
        else: #if the joke doesnt have a?
            setup = line #entire line is a setup
            punch = "" #with no punchline
        jokes.append((setup, punch)) #saves joke as a typle

#For the below wrap joke code i asked assistance from chatgpt to make sure that the joke fits inside the notification UI.
#What was asked: I want the text to fit inside the notification bar which is in the background, how can i do tht? here is my code for your reference

def wrap_joke(text, max_chars=34): #function to wrap text so it fits inside bubble
    words = text.split() #splits joke into words
    lines = [] #stores lines
    current_line = "" #building each line

    for word in words: #loops through all words
        if len(current_line) + len(word) + 1 > max_chars: #if adding word makes it too long
            lines.append(current_line)  #save current line
            current_line = word #starts new line
        else: 
            if current_line == "": #if its the first word
                current_line = word #it just adds it
            else: 
                current_line += " " + word #adds space and thn the word
    
    if current_line: #adds the last line
        lines.append(current_line) 

    return "\n".join(lines) #joins lines with the new line

question_label = tk.Label(  #main text above the yes button
    root,
    text="Wanna hear something funny?", #the default text
    bg="#ebeae8", #the background 
    fg="#484848", #text color
    font=("Roboto", 11), #font
    wraplength=245, #limits the line width from expanding the notification ui
    justify="left" #the alignment
)
question_label.place(x=110, y=348) #placement of the text

yes_button = tk.Label( #yes button
    root,
    text="Yes", #the text
    bg="#ebeae8", #background
    fg="#007AFF", #text color
    font=("Roboto", 11), #font and size
    cursor="hand2"#the pointer cursor changing to hand
)
yes_button.place(x=110, y=374) #placement of the button

punchline_label = tk.Label(root, #punchline label
    text="", #its empty until clicked 
    bg="#ebeae8", 
    fg="#484848",
    font=("Roboto", 11),
    wraplength=245,
    justify="left")

quit_label = tk.Label( #quit button
    root,
    text="Quit", #the text
    bg="#ebeae8", #the background colour
    fg="#FF3B30", #the text colour
    font=("Roboto", 11), #font and size
    cursor="hand2" #the pointer cursor changing to hand
)

quit_label.bind("<Button-1>", lambda e: root.destroy()) #clicking quit closes the window

def expand_notification(): #function to expand the ui so the joke fits inside the notification ui
    global bg_photo 
    img = Image.open(BG2_IMAGE) #the image with bigger notification ui
    img = img.resize((430,800)) #resizing the image to fit the window
    bg_photo = ImageTk.PhotoImage(img) 
    bg.config(image=bg_photo)
    question_label.place(x=110, y=348) #reposition of the text
    yes_button.place(x=110, y=430) #reposition of the button
    
def show_new_joke(event=None): #when user clicks yes or another joke
    expand_notification() #it switched to the other image
    global current_joke
    current_joke = random.choice(jokes) #picks a random joke
    setup, _ = current_joke #gets the setup part
    question_label.config(text=wrap_joke(setup, max_chars=28)) #shows wrapped setup
    punchline_label.config(text="") #clears the old punchline
    punchline_label.place(x=110, y=390) #shows the punchline area
    quit_label.place_forget()  #hides the quit button
    yes_button.config(text="Show punchline") #changes the button text
    yes_button.bind("<Button-1>", show_punchline) #when clicked it shows the punchline

def show_punchline(event=None): #shows the punchline
    if not current_joke: 
        return
    _, punch = current_joke 
    punchline_label.config(text=wrap_joke(punch, max_chars=28)) #shows punchline
    yes_button.config(text="Another joke") #changes the button 
    yes_button.bind("<Button-1>", show_new_joke) #clicking the button starts a new joke
    quit_label.place(x=250, y=430) #shows the button

yes_button.bind("<Button-1>", show_new_joke) #the first time user clicks yes

root.mainloop() #runs the window