import random
import tweepy
import tkinter as tk
from tkinter import messagebox
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Download the model and the tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')

# Constants
TWITTER_STANDARD = " include them in your response, use less than 60 characters"
DEFAULT_TEXT = "\n Convert this into a joke about "
line = random.choice("pickDiss.txt")
person = ""

# Main window
window = tk.Tk()
window.title("Trollscript using GPT2")

def post_to_twitter(generated_text):
    # Replace these with your own Twitter API credentials
    consumer_key = input("YOUR_CONSUMER_KEY >")
    consumer_secret = input("YOUR_CONSUMER_SECRET >")
    access_token = input("YOUR_ACCESS_TOKEN >")
    access_token_secret = input("YOUR_ACCESS_TOKEN_SECRET >")

    # Authenticate with the Twitter API
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    # Post the generated text as a tweet
    api.update_status(generated_text)


# Functions
def learn_bot(a):
    with open(a, 'r') as f:
        lines = f.readlines()
        return lines
    
def save_to_file(generated_text):
    with open("Generated_Disses.txt", "a") as f:
        f.write(generated_text + "\n")


def ask_for_names():
    names = ""
    # Keep asking for names until the user says they are done
    while True:
        # Ask the user for a name
        name = tk.simpledialog.askstring("Enter a name", "Enter a name:")
        # Add the name to the list
        names = names + name
        # Ask the user if they want to add more names
        more_names = tk.messagebox.askyesno("Add more names?", "Do you want to add more names?")
        # If the user does not want to add more names, break out of the loop
        if not more_names:
            break
    return names

def generate_text(event=None):
    global line
    global person
    # Create a frame to hold the radio buttons
    frame = tk.Frame(window)
    frame.pack()
    # Create a variable to hold the selected option
    choice_var = tk.IntVar()
    # Create a radio button for each option
    option1 = tk.Radiobutton(frame, text="Option 1", variable=choice_var, value=1)
    option1.pack(anchor=tk.W)
    option2 = tk.Radiobutton(frame, text="Option 2", variable=choice_var, value=2)
    option2.pack(anchor=tk.W)
    option3 = tk.Radiobutton(frame, text="Option 3", variable=choice_var, value=3)
    option3.pack(anchor=tk.W)
    option4 = tk.Radiobutton(frame, text="Option 4", variable=choice_var, value=4)
    option4.pack(anchor=tk.W)

    # Create a button to generate the text
    generate_button = tk.Button(window, text="Generate", command=generate_text)
    generate_button.pack()

    # Get the selected option
    choice = choice_var.get()
    if choice == 1:
        line = random.choice(learn_bot("pickDiss.txt")) + DEFAULT_TEXT + person + TWITTER_STANDARD
    elif choice == 2:
        person = ask_for_names()
        line = learn_bot("pickDiss.txt") + DEFAULT_TEXT + person + TWITTER_STANDARD
    elif choice == 3:
        train_data = tk.filedialog.askopenfilename()
        add_others = tk.messagebox.askyesno("Add more names?", "Would you like to draw out other mandem?")
        if add_others:
            person = ask_for_names()
        else:
            person = person
        line = learn_bot(train_data) + DEFAULT_TEXT + person + TWITTER_STANDARD
    elif choice == 4:
        lines = tk.simpledialog.askstring("Enter diss", "Enter diss:")
        line = lines + DEFAULT_TEXT + person + TWITTER_STANDARD
    # Encode the input and generate text
    input_ids = tokenizer.encode(line, return_tensors='pt')
    output = model.generate(input_ids, max_length=128, top_k=5, top_p=0.9, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)

    # Decode the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Print the generated text
    print(generated_text)
    
    # Create the "Save to file" button
    save_button = tk.Button(window, text="Save to file", command=save_to_file(generated_text))
    save_button.pack()

    # Create the "Post to Twitter" button
    twitter_button = tk.Button(window, text="Post to Twitter", command=post_to_twitter(generated_text))
    twitter_button.pack()
    
window.mainloop(generate_text())

