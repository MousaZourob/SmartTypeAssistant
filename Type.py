import random
import time
import math
from tkinter import *
import tkinter.font as tkFont


def get_dictionary(path):  # takes in a file path path and returns a list, content
    f = open(path, "r")

    content = f.readlines()
    f.close()

    return content


def get_prompt(dictionary, length):  # takes in a list, 'dictionary', and returns a list, 'prompt'
    global total_char_count

    prompt = []
    current_length = 0

    while current_length < length:
        word = dictionary[random.randrange(0, len(dictionary))]
        prompt.append(word)
        current_length += len(word)

    return prompt


def change_prompt():  # changes the prompt in the gui
    global current_word_index
    global correct_characters
    global wpm
    global accuracy
    global prompt

    prompt = get_prompt(dictionary, prompt_length)
    prompt_label.config(text=" ".join(prompt))
    input_field.delete(0, END)
    current_word_index = 0
    correct_characters = 0
    total_char_count = 0
    wpm = 0
    accuracy = 0

    update_gui_stats()


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
    global t0

    inputText = input_field.get()

    if current_word_index == 0:  # Check if this is the first letter in the prompt
        if len(inputText) == 1:
            t0 = time.time()

    if " " in inputText:  # Check if they typed a space (advance to next word)
        update_correct_characters(inputText[0: inputText.index(" ")])
        update_total_char_count()
        update_wpm()
        update_accuracy()
        update_gui_stats()
        input_field.delete(0, inputText.index(" ") + 1)
        current_word_index += 1


def update_correct_characters(word):  # changes the number of correct characters entered
    global correct_characters

    if len(word) == len(prompt[current_word_index]):
        if word == prompt[current_word_index]:
            correct_characters += len(word)
        else:
            for i in range(0, len(word)):  # loops through every letter in user input
                if word[i] != (prompt[current_word_index])[i]:  # compares said letter to prompt letter
                    misspelt_letters((prompt[current_word_index])[i])   # sends letter to be added to misspelt data
                    break  # if incorrect stop counting letters(add accuracy checker here)


def update_total_char_count():
    global total_char_count

    total_char_count += len(prompt[current_word_index])


def update_gui_stats():  # updates the gui labels for wpm and accuracy
    wpm_label.config(text="WPM: " + str(wpm))
    accuracy_label.config(text="Accuracy: " + str(accuracy) + "%")


def update_accuracy():  # updates the global accuracy variable
    global accuracy

    accuracy = math.ceil((correct_characters / total_char_count) * 1000) / 10.0


def update_wpm():  # updates the global wpm variable
    import time
    global t1
    global wpm

    t1 = time.time()  # gets the current time
    time = (t1 - t0) / 60  # time is in seconds, divide by 60 to get mins
    wpm = correct_characters / 5 / time  # calculate wpm
    wpm = math.ceil(wpm)  # round up wpm


def misspelt_letters(mis_char):
    mis_read = open("misspelt.txt", "r")    # initializes data file
    seek_counter = 0    # counter to seek current location in file

    with open('misspelt.txt', 'r') as file:     # stores all data in data file
        data = file.readlines()                 # in list to be changed

    for letter in mis_read.readlines():     # loops through data file from starting letter to end
        if letter[0] == mis_char:   # checks if letter equals misspelt character
            counter_mis = int(letter[len(letter) - 2]) + 1  # if it does adds 1 to misspelt character score
            data[seek_counter] = letter[0] + str(counter_mis) + "\n"    # stores misspelt character in data list
        seek_counter += 1   # added 1 to seek as it goes to next line

    with open('misspelt.txt', 'w') as file:     # stores new data list
        file.writelines(data)                   # in data file

    mis_read.close()


######################## backend stuff ####################

t0 = 0
t1 = 0
correct_characters = 0
total_char_count = 0
wpm = 0
accuracy = 0
current_word_index = 0
prompt_length = 190
dictionaryPath = "default.txt"
dictionary = [word.strip() for word in get_dictionary(dictionaryPath)]
prompt = get_prompt(dictionary, prompt_length)

######################## gui stuff ########################

window = Tk()
window.geometry("710x200")
window.title("Type Faster")

statistics_font = tkFont.Font(family="Arial", size=16, weight="bold")
prompt_font = tkFont.Font(family="Arial", size=14)
scale_font = tkFont.Font(family="Arial", size=14)

wpm_label = Label(window, text="WPM: 0", justify="left", font=statistics_font)
accuracy_label = Label(window, text="Accuracy: 0%", justify="left", font=statistics_font)
prompt_label = Label(window, text=prompt, wraplength=700, justify="left",
                     relief="sunken", borderwidth=3, padx=5, pady=5, font=prompt_font)
change_prompt_button = Button(window, text="New Prompt", bg="white",
                              activebackground="white", relief="groove", width="20",
                              command=lambda: change_prompt())

SCALE_LABELS = {
    0: "All",
    1: "Short",
    2: "Medium",
    3: "Long"
}

sv = StringVar()
sv.trace("w", input_updated)

input_field = Entry(window, width="50", relief="solid", textvariable=sv)
length_scale = Scale(window, from_=min(SCALE_LABELS), to=max(SCALE_LABELS),
                     length=300, orient=HORIZONTAL, showvalue=False,
                     command=scale_labels, font=scale_font)

wpm_label.grid(row=0, column=0)
accuracy_label.grid(row=0, column=1)
prompt_label.grid(row=1, column=0, columnspan=2)
input_field.grid(row=2, column=0)
change_prompt_button.grid(row=2, column=1)
length_scale.grid(row=3, column=0)

length_scale.set(0)
length_scale.config(label="All")

window.mainloop()