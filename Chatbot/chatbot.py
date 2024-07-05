import json
from fuzzywuzzy import fuzz
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

class CodyBot:
    def __init__(self):
        self.tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
        self.model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
        self.personal_data = self.load_personal_data('data.json')
        self.context = {}
        self.conversation_history = []
        self.known_questions = {
            "What is your name?": ["whats your name", "tell me your name", "Whats your name?", "Your name is?", "Hey, what is your name?"],
            "Tell me about your education.": ["What is your education", "what is your education", "Where did you go to school?", "Where did you go to school", "Where did you go to college?", "Where did you go to college"],
            "What projects have you worked on?": ["what are your projects", "tell me about your projects"],
            "How old are you?": ["how old are you", "old are you", "old you are", "How old are you", "What is your age", "your age is?", "What is your age"],
            "What is your height?": ["how tall are you", "what is your height", "What is your height?", "Your height is?","Tell me your height"],
            "When is your birthday?": ["What is your day of birth", "When were you born", "What is your birth date", "when were you born", "when is your birthday?", "When was your birthday"],
            "Do you have any pets?": ["What pets do you have?", "do you have pets", "Do you like cats", "do you like dogs", "what pets do you have"],
            "What is the best video game?": ["Do you like video games?", "Whats your favorite video game", "whats your favorite game", "what video games do you enjoy"]
        }

    def load_personal_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def match_known_question(self, user_input):
        for key, variations in self.known_questions.items():
            if fuzz.partial_ratio(user_input.lower(), key.lower()) > 85:
                return key
            for variation in variations:
                if fuzz.partial_ratio(user_input.lower(), variation.lower()) > 85:
                    return key
        return None

    def get_personal_response(self, user_input):
        if 'follow_up' in self.context:
            follow_up = self.context.pop('follow_up')
            if user_input.lower() in follow_up['responses']:
                return follow_up['responses'][user_input.lower()]
            else:
                return "I didn't understand your response. Can you please clarify?"

        matched_question = self.match_known_question(user_input)
        if matched_question:
            for item in self.personal_data:
                if matched_question == item['question']:
                    response = item['answer']
                    if 'follow_up_responses' in item:
                        self.context['follow_up'] = {
                            'responses': item['follow_up_responses']
                        }
                    self.conversation_history.append((user_input, response))
                    return response

        for item in self.personal_data:
            if fuzz.partial_ratio(user_input.lower(), item['question'].lower()) > 70:
                response = item['answer']
                if 'follow_up_responses' in item:
                    self.context['follow_up'] = {
                        'responses': item['follow_up_responses']
                    }
                self.conversation_history.append((user_input, response))
                return response
        return None

    def get_response(self, user_input):
        personal_response = self.get_personal_response(user_input)
        if personal_response:
            return personal_response

        # If no personal response is found, fall back to BlenderBot
        inputs = self.tokenizer([user_input], return_tensors='pt')
        reply_ids = self.model.generate(**inputs)
        response = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        return response

if __name__ == "__main__":
    bot = CodyBot()
    print("CodyBot: Hi! How can I help you today?")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit", "done"]:
            print("CodyBot: Goodbye!")
            break

        response = bot.get_response(user_input)
        print(f"CodyBot: {response}")
