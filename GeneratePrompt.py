import random
import time
import math


def get_dictionary(file):  # takes in a file path path and returns a list, content
    f = open(file, "r")
    content = f.readlines()
    f.close()

    return content


def get_prompt(words, length):  # takes in a list, 'dictionary', and returns a list, 'prompt'
    prompt = []
    current_length = 0

    while current_length < length:
        word = words[random.randrange(0, len(words))]
        prompt.append(word[0:-1])
        current_length += len(word)

    return prompt


file = "default.txt"  # Initializes file name to be used, better as variable so user can pick later
dictionary = get_dictionary(file)  # Gets all words from text file

prompt_length = 40 # Characters in the prompt
prompt = get_prompt(dictionary, prompt_length)  # Generates a random prompt
print(prompt)

# firstLetter = (prompt[0])[0:1]
# if keyboard.is_pressed(firstLetter):
#     t0 = time.time()

char_counter = 0    # counter to count how many correct characters
t0 = time.time()    # start time for user to type prompt
for index in range(0, len(prompt)):     # loops through every word in the prompt list
    temp = input("Enter word: ")    # gets the current word

    for i in range(0, len(temp)):   # loops through every letter in user input
        if str(temp[i]).lower() == str((prompt[index])[i]):     # compares said letter to prompt letter
            char_counter += 1   # adds 1 to correct letter counter
        else:
            break   # if incorrect stop counting letters(add accuracy checker here)

t1 = time.time()    # gets time it took for them to finish prompt
time = (t1 - t0)/60     # time is in seconds, divide by 60 to get mins
wpm = char_counter/5/time   # calculate wpm
print(math.ceil(wpm))   # print wpm

