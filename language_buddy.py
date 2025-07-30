import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random

USERS_DB = "gui_users.json"
languages_supported = {
    'Hindi': {
        'vocab': {'Pani': 'Water', 'Khana': 'Food', 'Namaste': 'Hello'},
        'quiz': [('What is the Hindi word for "Food"?', 'Khana')]
    },
    'Kannada': {
        'vocab': {'Neeru': 'Water', 'Oota': 'Food', 'Namaskara': 'Hello'},
        'quiz': [('What is the Kannada word for "Water"?', 'Neeru')]
    },
    'Tamil': {
        'vocab': {'Thanneer': 'Water', 'Sappadu': 'Food', 'Vanakkam': 'Hello'},
        'quiz': [('What is the Tamil word for "Hello"?', 'Vanakkam')]
    }
}


# ---------- User Management ----------
def load_users():
    if os.path.exists(USERS_DB):
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_DB, 'w') as f:
        json.dump(users, f)

users = load_users()


# ---------- GUI App ----------
class LanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Buddy - Learn Indian Languages")
        self.username = ""
        self.language = "Hindi"
        self.users = users

        self.login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Language Buddy", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Sign In", command=self.sign_in).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.sign_up).pack()

    def sign_in(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()
        if uname in self.users and self.users[uname]["password"] == pwd:
            self.username = uname
            self.language_selection()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def sign_up(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()
        if uname in self.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.users[uname] = {"password": pwd, "progress": {}}
            save_users(self.users)
            messagebox.showinfo("Success", "Account created.")
            self.login_screen()

    def language_selection(self):
        self.clear_screen()
        tk.Label(self.root, text="Choose a Language", font=("Arial", 16)).pack(pady=10)

        for lang in languages_supported:
            tk.Button(self.root, text=lang, command=lambda l=lang: self.main_menu(l)).pack(pady=5)

    def main_menu(self, lang):
        self.language = lang
        self.clear_screen()
        tk.Label(self.root, text=f"Hi {self.username}! Learning {lang}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="📚 Flashcards", command=self.show_flashcards).pack(pady=5)
        tk.Button(self.root, text="❓ Quiz", command=self.quiz).pack(pady=5)
        tk.Button(self.root, text="🧠 Grammar Tips", command=self.grammar).pack(pady=5)
        tk.Button(self.root, text="✍️ Writing Practice", command=self.writing).pack(pady=5)
        tk.Button(self.root, text="🗣️ Conversation Practice", command=self.conversation).pack(pady=5)
        tk.Button(self.root, text="📈 Track Progress", command=self.track_progress).pack(pady=5)
        tk.Button(self.root, text="🔒 Logout", command=self.login_screen).pack(pady=5)

    def show_flashcards(self):
        vocab = languages_supported[self.language]["vocab"]
        word, meaning = random.choice(list(vocab.items()))
        messagebox.showinfo("Flashcard", f"{word} means '{meaning}'")

    def quiz(self):
        question, answer = random.choice(languages_supported[self.language]["quiz"])
        user_answer = simpledialog.askstring("Quiz", question)
        if user_answer and user_answer.strip().lower() == answer.lower():
            messagebox.showinfo("Correct!", "✅ Well done!")
        else:
            messagebox.showinfo("Incorrect", f"❌ Correct Answer: {answer}")

    def grammar(self):
        tips = {
            "Hindi": "- Hindi uses Subject-Object-Verb.\n- Gender matters: Ladka/Ladki",
            "Kannada": "- Verb comes at the end.\n- Uses postpositions, not prepositions.",
            "Tamil": "- Subject-Object-Verb.\n- No gendered pronouns in general speech."
        }
        messagebox.showinfo("Grammar Tips", tips[self.language])

    def writing(self):
        sentence = simpledialog.askstring("Writing Practice", f"Write a sentence in {self.language}:")
        if sentence:
            messagebox.showinfo("Looks good!", f"✅ '{sentence}' recorded! (Correction coming soon)")

    def conversation(self):
        bot_q = {
            "Hindi": "Namaste! Aap kaise ho?",
            "Kannada": "Namaskara! Neenu hegiddiya?",
            "Tamil": "Vanakkam! Eppadi irukkenga?"
        }
        user_response = simpledialog.askstring("Conversation", f"Bot: {bot_q[self.language]}\nYou:")
        messagebox.showinfo("Bot", "Achha! Main bhi theek hoon. :)")

    def track_progress(self):
        progress = self.users[self.username]["progress"]
        lang_sessions = progress.get(self.language, 0) + 1
        self.users[self.username]["progress"][self.language] = lang_sessions
        save_users(self.users)
        messagebox.showinfo("Progress", f"You've completed {lang_sessions} session(s) in {self.language}!")

# ---------- Run App ----------
root = tk.Tk()
root.geometry("400x500")
app = LanguageApp(root)
root.mainloop()
