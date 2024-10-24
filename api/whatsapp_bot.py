import json
import random
from collections import defaultdict
import re
import os
from datetime import datetime
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleAIBot:
    def __init__(self, training_file):
        self.intents = self.load_training_data(training_file)
        self.vectorizer = TfidfVectorizer()
        self.train_model()

    def load_training_data(self, training_file):
        with open(training_file, 'r') as file:
            return json.load(file)['intents']

    def train_model(self):
        patterns = []
        self.tags = []
        for intent in self.intents:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                self.tags.append(intent['tag'])
        self.tfidf_matrix = self.vectorizer.fit_transform(patterns)

    def get_response(self, message):
        message_vector = self.vectorizer.transform([message])
        similarities = cosine_similarity(message_vector, self.tfidf_matrix)
        best_match = similarities.argmax()

        tag = self.tags[best_match]
        responses = next(
            intent['responses']
            for intent in self.intents
            if intent['tag'] == tag
        )
        return random.choice(responses)

    def process_message(self, sender, message):
        response = self.get_response(message)
        self.log_message(sender, message, response)
        return json.dumps({
            'type': 'response',
            'recipient': sender,
            'content': response
        })

    def log_message(self, sender, message, response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message} -> Bot: {response}\n"
        with open("chat_logs.txt", "a") as log_file:
            log_file.write(log_entry)

# Initialize bot
bot = SimpleAIBot('chatbot_intents.json')

# Process stdin messages from Node.js
while True:
    try:
        message = input()
        data = json.loads(message)
        if data['type'] == 'message':
            print(bot.process_message(data['sender'], data['content']))
    except EOFError:
        break
    except Exception as e:
        print(json.dumps({'type': 'error', 'message': str(e)}))
