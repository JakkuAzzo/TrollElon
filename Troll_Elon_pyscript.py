from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

print("use pip3 to install selenium and transformers")

twitStandard = " include them in your response, use less than 60 characters"
defaultText = "\n Convert this into a joke about "

# Download the model and the tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')

print(" - - - - - - - - - - - -")
print(" Trollscript using GPT2 ")
print(" - - - - - - - - - - - -")
#fail = 0
#Lets @Elon from the start
person = "Elon Musk"

#Include twitter to make it more specific
choiceT = input("Incude Twitter in diss? (y/n)")
if choiceT == "y":
    person = person + ", twitter "
else: 
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    
#Read and learn from Diss Script
trainData = "pickDiss.txt"
def learnBot(a):
    with open(trainData, 'r') as f:
        lines = f.readlines()
        return lines
learnBot(trainData)

def ask_for_names():
    names = ""
    # Keep asking for names until the user says they are done
    while True:
        # Ask the user for a name
        name = input("Enter a name: ")
        # Add the name to the list
        names = names + name
        # Ask the user if they want to add more names
        more_names = input("Do you want to add more names? (Y/N) ")
        # If the user does not want to add more names, break out of the loop
        if more_names.lower() != 'y':
            break
    return names

#Main Title
choice = int(input("1. Mock Elon Musk > \n" + "Not working: 2. Mock Someone else > \n" +"3. enter location of your own Diss script > \n"+ "4. Enter your own diss line > \n"))

if choice == 1:
    line = random.choice(learnBot(trainData)) + defaultText + person + twitStandard
    
if choice == 2:
    person = ask_for_names()
    line = learnBot(trainData) + defaultText+ person +twitStandard
    
if choice == 3:
    print("This will probably only work if you've downloaded your code to your device")
    trainData = input("Enter the name / location of your Diss Script > ")
    addOthers = input("Would you like to draw out other mandem ? (y/n) >")
    if addOthers == "y":
        person = ask_for_names()
    else:
        person = person
    line = learnBot(trainData) +defaultText+ person + twitStandard
        
if choice == 4:
    lines = input("Enter diss > ")
    line = lines + defaultText + person +twitStandard

#else:
#    print("Use it properly man, stop messing around \n")
#    fail = fail + 1
#     #call main loop
#    if fail >= 6:
#        print("Just leave. just get out. ")

    
# Encode the input and generate text
input_ids = tokenizer.encode(line, return_tensors='pt')
output = model.generate(input_ids, max_length=128, top_k=5, top_p=0.9, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)

# Decode the generated text and print it to the console
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
print()
print("The next two features dont work")
print()
PostToTwitter = input("Would you like to post this to Twitter? (y/n) >")
if PostToTwitter == "y":
    print("This will probably only work if you dont have 2fa on your twitter account and have chrome installed")
    # Set up ChromeDriver
    driver = webdriver.Chrome()
    # Go to Twitter
    driver.get('https://twitter.com')

    # Log in to Twitter
    username_field = driver.find_element(By.NAME,'session[username_or_email]')
    username = input("Enter your twitter username > ")
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME,'session[password]')
    password = input("Enter your twitter password > ")
    password_field.send_keys(password)
    login_button = driver.find_element_by_css_selector('button[type="submit"]')
    login_button.click()

    # Post a tweet
    tweet_box = driver.find_element_by_css_selector('div[data-testid="tweetTextarea_0"]')
    tweet_box.send_keys(generated_text)
    tweet_button = driver.find_element_by_css_selector('div[data-testid="tweetButton"]')
    tweet_button.click()
    
else:
    save = input("Would you like to save this to Generated Disses? (y/n)>")
    if save == "y":
        filename = 'Generated_Disses.txt'
        filepath = '/Troll_Elon/'  # Replace this with the actual path to the folder where you want to save the file

        # Check if the file already exists
        if os.path.exists(filepath + filename):
            # If the file exists, open it in append mode
            with open(filepath + filename, 'a') as f:
                # Append the output of your script to the file
                f.write(generated_text)
        else:
            # If the file does not exist, create it
            with open(filepath + filename, 'w') as f:
                # Write the output of your script to the file
                f.write(generated_text)
    
    else:
        "Peace bro"