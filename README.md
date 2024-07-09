# Requirements

  * Python 3.7
  * Transformers
  * Fuzzywuzzy

  * use pip install -r requirements.txt

# Sample Execution and Output

Run using
```
./ py chatbot.py
```

output varies depending on questions prompted by user.
```
sample question:
What is your name?

sample output:
CodyBot: My name is Cody Rabie!

```
# CodyChatBOT
CodyChatBOT is the first time I have attempted to make any type of chatbot. I do so using a .json file of data provided by myself to respond as Cody Rabie to preprocessed questions.  
The program preprocesses the data.json file in the directory to provide answers to certain questions as myself (Cody). If it does not recognize user input it will provide the user input  
to blenderbot and return the answer from so. Each user question is saved in conversation history as the user continues. 
