import tkinter as tk
from tkinter import simpledialog
from collections import deque
from datetime import datetime
import json
import os
import threading
import time
import random

# Linked list node class for storing messages
class Node:
    def __init__(self, username, message, timestamp):
        self.username = username
        self.message = message
        self.timestamp = timestamp
        self.next = None

# Linked list class for chat history
class ChatHistory:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_message(self, username, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_node = Node(username, message, timestamp)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def get_messages(self):
        messages = []
        current = self.head
        while current is not None:
            messages.append(f"[{current.timestamp}] {current.username}: {current.message}")
            current = current.next
        return messages

    def delete_last_message(self):
        if self.head is None:
            return
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current

    def clear_chat(self):
        self.head = self.tail = None

    def save_history(self, filename):
        messages = self.get_messages()
        with open(filename, 'w') as f:
            json.dump(messages, f)

    def load_history(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                messages = json.load(f)
                for message in messages:
                    timestamp, username_message = message.split("] ", 1)
                    username, message = username_message.split(": ", 1)
                    self.add_message(username, message)

# Main chat application class
class ChatApp:
    def __init__(self, root):
        self.chat_history = ChatHistory()
        self.message_queue = deque()
        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.chat_history.load_history("chat_history.json")

        # Setup Tkinter interface
        self.root = root
        self.root.title("ChatCast")
        self.root.geometry("400x600")  # Setting a fixed window size
        self.root.config(bg="#f0f0f0")  # Background color

        # Chat display (with scrollbar)
        self.chat_display_frame = tk.Frame(root)
        self.chat_display_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_display = tk.Text(self.chat_display_frame, state="disabled", width=50, height=20, bg="light yellow", font=("Arial", 12), wrap=tk.WORD)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.chat_display.yview)
        self.chat_display.config(yscrollcommand=self.scrollbar.set)

        # Entry for new message
        self.message_entry = tk.Entry(root, width=40, font=("Arial", 12), bd=2, relief="solid")
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())  # Enter to send
        
        # Buttons for functionality
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=5)

        send_button = tk.Button(button_frame, text="Send Message", command=self.send_message, width=15, height=2, bg="#4CAF50", fg="white", font=("Arial", 12), relief="solid", bd=1, activebackground="#45a049")
        send_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Last Message", command=self.delete_message, width=15, height=2, bg="#FF5733", fg="white", font=("Arial", 12), relief="solid", bd=1, activebackground="#ff5733")
        delete_button.grid(row=0, column=1, padx=5)

        clear_button = tk.Button(button_frame, text="Clear Chat", command=self.clear_chat, width=15, height=2, bg="#F1C40F", fg="white", font=("Arial", 12), relief="solid", bd=1, activebackground="#f1c40f")
        clear_button.grid(row=1, column=0, pady=5)

        save_button = tk.Button(button_frame, text="Save Chat History", command=self.save_chat, width=15, height=2, bg="#3498DB", fg="white", font=("Arial", 12), relief="solid", bd=1, activebackground="#2980b9")
        save_button.grid(row=1, column=1, pady=5)

        self.update_chat_display()
        self.bot_intro()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_queue.append((self.username, message))
            self.process_message_queue()
            self.message_entry.delete(0, tk.END)
            self.bot_response(message)

    def process_message_queue(self):
        while self.message_queue:
            username, message = self.message_queue.popleft()
            self.chat_history.add_message(username, message)
            self.update_chat_display()

    def update_chat_display(self):
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        messages = self.chat_history.get_messages()

        if messages:
            for msg in messages:
                # Display user and bot messages with different styles
                if msg.startswith(f"[{self.username}]:"):
                    self.chat_display.insert(tk.END, f"{msg}\n", "user_message")
                else:
                    self.chat_display.insert(tk.END, f"{msg}\n", "bot_message")

        else:
            self.chat_display.insert(tk.END, "No chat history.\n")

        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def delete_message(self):
        self.chat_history.delete_last_message()
        self.update_chat_display()

    def clear_chat(self):
        self.chat_history.clear_chat()
        self.update_chat_display()

    def save_chat(self):
        self.chat_history.save_history("chat_history.json")

    def bot_intro(self):
        intro_message = "Hello! I'm Matrix, your chat assistant. Feel free to ask me anything or just chat with me!"
        self.message_queue.append(("Matrix", intro_message))
        self.process_message_queue()

    def bot_response(self, user_message):
        responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What's up?",
            "hey": "Hey! What's going on?",
            "how are you": "I'm just a bot, but I'm here to help you!",
            "good morning": "Good morning! Hope you have a wonderful day ahead!",
            "good night": "Good night! Sleep well!",
            "bye": "Goodbye! Have a great day!",
            "thanks": "You're welcome!",
            "tell me a joke": "Why don’t scientists trust atoms? Because they make up everything!",
            "another joke": "Why did the math book look sad? Because it had too many problems!",
            "your name": "I am Matrix, your friendly chatbot.",
            "what's your name": "I am Matrix, your chatbot. Nice to meet you!",
            "what can you do": "I can chat with you, tell jokes, answer questions, and much more!",
            "what's up": "Not much! Just here to chat with you.",
            "how's it going": "It's going great! Thanks for asking.",
            "tell me something interesting": "Did you know? The human nose can distinguish at least 1 trillion different scents!",
            "what's the weather like": "Sorry, I don't have live weather updates, but you can check your local forecast online!",
            "how tall is mount everest": "Mount Everest is 8,848.86 meters tall (29,031.7 feet).",
            "who is the president of the usa": "The current president is Joe Biden.",
            "what's the capital of france": "The capital of France is Paris.",
            "who won the world series": "I don’t have real-time data, but the most recent winner of the World Series was the Houston Astros in 2022.",
            "how to make pasta": "To make pasta, boil water, add salt, cook the pasta according to the package instructions, and drain. Enjoy with your favorite sauce!",
            "what is machine learning": "Machine learning is a field of AI that uses algorithms to learn patterns from data and make decisions without explicit programming.",
            "define python": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's used for web development, data analysis, and more.",
            "what's an ai": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
            "who discovered electricity": "Electricity wasn't discovered by one person, but Benjamin Franklin's experiments in the 18th century contributed significantly to our understanding of it.",
            "what is the internet": "The internet is a global network of computers that are connected to each other, allowing the sharing of information and communication.",
            "what is the meaning of life": "The meaning of life is a philosophical question that has been debated for centuries, often answered with personal or spiritual perspectives.",
            "tell me a fact": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
            # New responses
            "what's your favorite color": "I don't have preferences, but blue is a calming color, don't you think?",
            "who are you": "I'm Matrix, your friendly chatbot. Here to assist you!",
            "what is your favorite food": "I don't eat food, but I hear pizza is quite popular!",
            "can you help me with coding": "Of course! I can help with coding. What language are you working with?",
            "do you like music": "I don't have ears, but I know music is a universal language!",
            "what's 2 + 2": "2 + 2 equals 4.",
            "what is your favorite movie": "I don't watch movies, but I know many people love classics like 'The Shawshank Redemption.'",
            "who invented the telephone": "The telephone was invented by Alexander Graham Bell.",
            "tell me a story": "Once upon a time, there was a curious robot who wanted to understand humans. It asked questions, learned, and made great friends along the way!",
            "can you play games": "I can help with trivia and puzzles! Want to play?"
        }

        def respond():
            time.sleep(1)
            for keyword, response in responses.items():
                if keyword in user_message.lower():
                    self.message_queue.append(("Matrix", response))
                    self.process_message_queue()
                    return

            # If no response matches, give a random response
            random_responses = [
                "Interesting!", "Can you tell me more?", "I'm here to chat!",
                "That sounds cool!", "I'm listening.", "Let's talk more about it!",
                "What else can you tell me?", "That’s amazing!",
            ]
            self.message_queue.append(("Matrix", random.choice(random_responses)))
            self.process_message_queue()

        threading.Thread(target=respond).start()

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
