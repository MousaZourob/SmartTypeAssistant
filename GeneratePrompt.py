import random


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

prompt_length = 150  # Characters in the prompt
prompt = get_prompt(dictionary, prompt_length)  # Generates a random prompt
print(prompt)
