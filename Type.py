import threading
import random
import time
import math
import os
import string
from tkinter import *
import tkinter.font as tkFont

def get_dictionary(path):  # takes in a file path path and returns a list, content
    f = open("dictionary\\" + path, "r")

    content = f.readlines()
    f.close()

    return content

def get_mistakes():     # searches for letters where user made most mistakes
    nums = {}
    letters = []

    with open('res\\misspelt.txt', 'r') as file:     # stores all data in data file
        data = file.readlines()                 # in list to be changed

    for i in range(0, len(data)):
        nums[str(data[i][0])]= int(data[i][1:-1])

    letters = sorted(nums, key=nums.get, reverse=True)
    
    if nums[letters[0]] < 5:
        return None
    else:
        return letters[0:3]

def get_prompt(dictionary, length):  # takes in a list, 'dictionary', and returns a list, 'prompt'
    global total_char_count
    global improvement_text

    mistakes = get_mistakes()

    prompt = []
    current_length = 0

    if mistakes == None:
        improvement_text = "Play more games!"
        while current_length < length:
            word = dictionary[random.randrange(0, len(dictionary))]
            prompt.append(word)
            current_length += len(word)
    else:
        improvement_text = "Improve on: " + (", ".join(mistakes)).upper()
        while current_length < length:
            word = dictionary[random.randrange(0, len(dictionary))]
            if any(m in word for m in mistakes):
                prompt.append(word)
                current_length += len(word)

    return prompt

def change_prompt():  # changes the prompt in the gui
    global current_word_index
    global correct_characters
    global total_char_count
    global wpm
    global accuracy
    global prompt

    prompt = get_prompt(dictionary, prompt_length)
    input_field.delete(0, END)
    current_word_index = 0
    correct_characters = 0
    total_char_count = 0
    wpm = 0
    accuracy = 0

    start_game()

def scale_labels(value):  # runs when the slider is changed
    global dictionaryPath
    global dictionary
    length_scale.config(label=SCALE_LABELS[int(value)])

    # the below code swaps the dictionary the program is using
    if length_scale.get() == 0:
        dictionaryPath = "default.txt"
    elif length_scale.get() == 1:
        dictionaryPath = "short.txt"
    elif length_scale.get() == 2:
        dictionaryPath = "medium.txt"
    elif length_scale.get() == 3:
        dictionaryPath = "long.txt"

    dictionary = [word.strip() for word in get_dictionary(dictionaryPath)]


def input_updated(*args):  # When the user changes the input field
    global current_word_index
    global current_label
    global t0

    inputText = input_field.get()

    if current_word_index == 0:  # Check if this is the first letter in the prompt
        if len(inputText) == 1:
            start_game()

    if " " in inputText:  # Check if they typed a space (advance to next word)
        update_correct_characters(inputText[0: inputText.index(" ")])
        update_total_char_count()
        input_field.delete(0, inputText.index(" ") + 1)
        current_word_index += 1
        current_label.config(underline=0)
        update_prompt_frame()
        if current_word_index == len(prompt):
            stop_game()
    else:
        if not len(inputText) > len(prompt[current_word_index]):
            if inputText == prompt[current_word_index][0:len(inputText)]:
                current_label.config(fg="black", underline=len(inputText))
            else:
                current_label.config(fg="red", underline=len(inputText))
        else:
            current_label.config(fg="red", underline=len(inputText))

def update_prompt_frame() :
    previous_words = prompt[:current_word_index]
    try:
        next_words = prompt[current_word_index + 1:]
    except:
        next_words = ""
    previous_label.config(text=" ".join(previous_words))
    next_label.config(text=" ".join(next_words))
    try:
        current_label.config(text=str(prompt[current_word_index]))
    except:
        current_label.config(text="", relief="flat")

def update_correct_characters(word):  # changes the number of correct characters entered
    global correct_characters

    if len(word) <= len(prompt[current_word_index]):
        if word == prompt[current_word_index]:
            correct_characters += len(word)
        else:
            for i in range(0, len(word)):  # loops through every letter in user input
                if word[i] != (prompt[current_word_index])[i]:  # compares said letter to prompt letter
                    misspelt_letters((prompt[current_word_index])[i])   # sends letter to be added to misspelt data
                    break  # if incorrect stop counting letters(add accuracy checker here)

def update_total_char_count():  # finds all characters in the prompt and
    global total_char_count     # adds them to a global char prompt variable

    total_char_count += len(prompt[current_word_index])

def update_gui_stats():  # updates the gui labels for wpm and accuracy
    import time
    global accuracy
    global t1
    global wpm

    try:
        accuracy = math.ceil((correct_characters / total_char_count) * 1000) / 10.0
    except:
        accuracy = 0

    t1 = time.time()  # gets the current time
    time = (t1 - t0) / 60  # time is in seconds, divide by 60 to get mins

    try:
        wpm = math.ceil(correct_characters / 5 / time)  # calculate wpm
    except:
        wpm = 0

    try:
        wpm_label.config(text="WPM: " + str(wpm))
        accuracy_label.config(text="Accuracy: " + str(accuracy) + "%")
    except:
        pass

    if game_is_running:
        threading.Timer(1.0, update_gui_stats).start()

def misspelt_letters(mis_char):
    mis_read = open("res\\misspelt.txt", "r")    # initializes data file
    seek_counter = 0    # counter to seek current location in file

    with open('res\\misspelt.txt', 'r') as file:     # stores all data in data file
        data = file.readlines()                 # in list to be changed

    for letter in mis_read.readlines():     # loops through data file from starting letter to end
        if letter[0] == mis_char:   # checks if letter equals misspelt character
            counter_mis = int(letter[len(letter) - 2]) + 1  # if it does adds 1 to misspelt character score
            data[seek_counter] = letter[0] + str(counter_mis) + "\n"    # stores misspelt character in data list
        seek_counter += 1   # added 1 to seek as it goes to next line

    with open('res\\misspelt.txt', 'w') as file:     # stores new data list
        file.writelines(data)                   # in data file

    mis_read.close()

def start_game():
    global t0
    global game_is_running

    wpm_label.config(fg="black")
    accuracy_label.config(fg="black")
    current_label.config(relief="solid", borderwidth=3)
    improvement_label.config(text=improvement_text)
    game_is_running = True
    input_field.config(state="normal")
    t0 = time.time()
    update_gui_stats()
    update_prompt_frame()

def stop_game():
    global game_is_running

    game_is_running = False
    input_field.config(state="disabled")
    wpm_label.config(fg="green")
    accuracy_label.config(fg="green")

def clear_misspelt():
    path = "res\\misspelt.txt"
    file = open(path, "w+")

    if os.path.isfile(path):
        file.truncate(0)
    
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    
    for i in range(0, len(alphabet_list)):
        file.write(alphabet_list[i] + "0\n")

    file.close()

######################## backend stuff ####################

improvement_text = ""
game_is_running = False
t0 = 0
t1 = 0
correct_characters = 0
total_char_count = 0
wpm = 0
accuracy = 0
current_word_index = 0
prompt_length = 180
dictionaryPath = "default.txt"
dictionary = [word.strip() for word in get_dictionary(dictionaryPath)]
prompt = get_prompt(dictionary, prompt_length)
previous_words = prompt[:current_word_index]
next_words = prompt[current_word_index + 1:]
WINDOW_WIDTH = 1000
WINDOW_HEIGHT= 380

######################## gui stuff ########################

window = Tk()
window.geometry(str(WINDOW_WIDTH + 80) + "x" + str(WINDOW_HEIGHT))
window.resizable(False, False)
window.title("Type Faster")
window.iconbitmap('res\\icon.ico')

statistics_font = tkFont.Font(family="Consolas", size=24, weight="bold")
prompt_font = tkFont.Font(family="Consolas", size=16)
button_font = tkFont.Font(family="Consolas", size=16, weight="bold")

wpm_label = Label(window, text="WPM: 0", font=statistics_font)
accuracy_label = Label(window, text="Accuracy: 0%", font=statistics_font)
prompt_frame = Frame(window, relief="solid", borderwidth=5, padx=10, pady=10)
previous_label = Label(prompt_frame, text=" ".join(previous_words), wraplength=WINDOW_WIDTH,
                        borderwidth=3, padx=5, pady=5, font=prompt_font)
next_label = Label(prompt_frame, text=" ".join(next_words), wraplength=WINDOW_WIDTH,
                        borderwidth=3, padx=5, pady=5, font=prompt_font)
current_label = Label(prompt_frame, text=prompt[current_word_index], wraplength=WINDOW_WIDTH,
                        relief="solid", borderwidth=3, padx=5, pady=5, font=prompt_font)
improvement_label = Label(window, text="", justify="left", bg='white', fg="#6464c8",
                        relief="ridge", borderwidth=3, padx=10, pady=10, font=prompt_font)
change_prompt_button = Button(window, text="New Prompt", bg="white", fg="#64c864",
                        activebackground="white", width="16", borderwidth=5,
                        command=lambda: change_prompt(), font=button_font)
delete_misspell_button = Button(window, text="Clear Typing Data", bg="white", fg="#c86464",
                        activebackground="white", width="22", borderwidth=5,
                        command=lambda: clear_misspelt(), font=button_font)

SCALE_LABELS = {
    0: "All",
    1: "Short",
    2: "Medium",
    3: "Long"
}

sv = StringVar()
sv.trace("w", input_updated)

input_field = Entry(window, width=36, relief="sunken", borderwidth=8,
                    textvariable=sv, font=prompt_font)
length_scale = Scale(window, from_=min(SCALE_LABELS), to=max(SCALE_LABELS),
                    length=round(WINDOW_WIDTH / 4), orient=HORIZONTAL, 
                    showvalue=False, command=scale_labels, font=button_font)

wpm_label.grid(row=0, column=0)
accuracy_label.grid(row=0, column=1)
improvement_label.grid(row=0, column=2, columnspan=2, pady=20, padx=20)
delete_misspell_button.grid(row=0, column=4, padx=10)

prompt_frame.grid(row=1, column=0, columnspan=5, padx=10)
previous_label.grid(row=0, column=0)
current_label.grid(row=1, column=0)
next_label.grid(row=2, column=0)

input_field.grid(row=2, column=0, columnspan=3, pady=20, padx=20)
change_prompt_button.grid(row=2, column=3, padx=10)
length_scale.grid(row=2, column=4, columnspan=2)

length_scale.set(0)
length_scale.config(label="All")

improvement_label.config(text=improvement_text)
window.mainloop()