import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import threading
import pygame

# --- INIT PYGAME FOR SOUND ---
pygame.mixer.init()

# --- SOUND PLAYER FUNCTION ---
def play_sound(path):
    threading.Thread(target=lambda: pygame.mixer.Sound(path).play(), daemon=True).start()

# --- ANIMATED GIF FUNCTION ---
from PIL import Image, ImageTk, ImageSequence

def animate_gif(label, path, size=(100, 100)):
    img = Image.open(path)

    # Use LANCZOS resampling for high-quality resizing
    frames = [
        ImageTk.PhotoImage(frame.copy().resize(size, Image.Resampling.LANCZOS))
        for frame in ImageSequence.Iterator(img)
    ]

    def update(index):
        label.configure(image=frames[index])
        label.image = frames[index]  # prevent garbage collection
        root.after(100, update, (index + 1) % len(frames))

    update(0)

# --- GAME CONFIG ---
CHOICES = ["Rock", "Paper", "Scissors"]
EMOJIS = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}
WINS_AGAINST = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}

user_score = 0
comp_score = 0
round_number = 1

# --- GAME LOGIC ---
def play(choice):
    global user_score, comp_score, round_number

    comp_choice = random.choice(CHOICES)
    user_choice_label.config(text=f"You chose: {choice} {EMOJIS[choice]}")
    comp_choice_label.config(text=f"Computer chose: {comp_choice} {EMOJIS[comp_choice]}")

    if choice == comp_choice:
        result = "😂 It's a Tie!"
        result_color = "#F1C40F"
        play_sound("laugh.mp3")
    elif WINS_AGAINST[choice] == comp_choice:
        user_score += 1
        result = "🏆 You Win!"
        result_color = "#2ECC71"
        play_sound("win.mp3")
    else:
        comp_score += 1
        result = "😤 Computer Wins!"
        result_color = "#E74C3C"
        play_sound("boo.mp3")

    result_label.config(text=result, fg=result_color)
    update_scores()
    history.insert(tk.END, f"🎲 Round {round_number}: You - {choice}, Comp - {comp_choice} ➜ {result}")
    round_number += 1

def reset_game():
    global user_score, comp_score, round_number
    user_score = 0
    comp_score = 0
    round_number = 1
    user_choice_label.config(text="You chose: ")
    comp_choice_label.config(text="Computer chose: ")
    result_label.config(text="")
    history.delete(0, tk.END)
    update_scores()

def update_scores():
    user_score_label.config(text=f"🧑 You: {user_score}")
    comp_score_label.config(text=f"🤖 Comp: {comp_score}")

# --- GUI SETUP ---
root = tk.Tk()
root.title("🎮 Rock, Paper, Scissors - Animated & Sound Edition")
root.geometry("600x900")
root.config(bg="#FFFBEA")
root.resizable(False, False)

# Title
tk.Label(root, text="🌟 Rock, Paper, Scissors 🌟", font=("Comic Sans MS", 24, "bold"), bg="#FFFBEA", fg="#FF3CAC").pack(pady=10)

# Avatar Frame
avatar_frame = tk.Frame(root, bg="#FFFBEA")
avatar_frame.pack()

user_avatar_label = tk.Label(avatar_frame, bg="#FFFBEA")
user_avatar_label.grid(row=0, column=0, padx=40)

vs_label = tk.Label(avatar_frame, text="⚔️", font=("Comic Sans MS", 22), bg="#FFFBEA")
vs_label.grid(row=0, column=1)

comp_avatar_label = tk.Label(avatar_frame, bg="#FFFBEA")
comp_avatar_label.grid(row=0, column=2, padx=40)

# Animate the avatars
animate_gif(user_avatar_label, "player.gif", size=(200, 200))
animate_gif(comp_avatar_label, "computer.gif", size=(200, 200))

# Labels
user_choice_label = tk.Label(root, text="You chose: ", font=("Comic Sans MS", 14), bg="#FFFBEA", fg="#0066FF")
user_choice_label.pack()
comp_choice_label = tk.Label(root, text="Computer chose: ", font=("Comic Sans MS", 14), bg="#FFFBEA", fg="#FF6600")
comp_choice_label.pack()

# Result Label
result_label = tk.Label(root, text="", font=("Comic Sans MS", 18, "bold"), bg="#FFFBEA")
result_label.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#FFFBEA")
button_frame.pack(pady=10)

tk.Button(button_frame, text="🪨 ROCK", font=("Comic Sans MS", 14, "bold"), bg="#00C4FF", fg="white", width=12, command=lambda: play("Rock")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="📄 PAPER", font=("Comic Sans MS", 14, "bold"), bg="#FF9F1C", fg="white", width=12, command=lambda: play("Paper")).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="✂️SCISSORS", font=("Comic Sans MS", 14, "bold"), bg="#8E44AD", fg="white", width=14, command=lambda: play("Scissors")).grid(row=0, column=2, padx=10)

# Scoreboard
score_frame = tk.Frame(root, bg="#FFFBEA")
score_frame.pack(pady=10)
user_score_label = tk.Label(score_frame, text="🧑 You: 0", font=("Comic Sans MS", 16, "bold"), bg="#FFFBEA", fg="#0066FF")
user_score_label.grid(row=0, column=0, padx=30)
comp_score_label = tk.Label(score_frame, text="🤖 Comp: 0", font=("Comic Sans MS", 16, "bold"), bg="#FFFBEA", fg="#FF6600")
comp_score_label.grid(row=0, column=1, padx=30)

# Game History
tk.Label(root, text="📜 Game History", font=("Comic Sans MS", 16, "bold"), bg="#FFFBEA", fg="#FF3CAC").pack(pady=(10, 5))
history = tk.Listbox(root, width=60, height=6, font=("Comic Sans MS", 10))
history.pack()

# Footer
footer = tk.Frame(root, bg="#FFFBEA")
footer.pack(pady=20)
tk.Button(footer, text="🔄 Reset", font=("Comic Sans MS", 12, "bold"), bg="#2ECC71", fg="white", width=12, command=reset_game).grid(row=0, column=0, padx=10)
tk.Button(footer, text="🚪 Quit", font=("Comic Sans MS", 12, "bold"), bg="#E74C3C", fg="white", width=12, command=root.quit).grid(row=0, column=1, padx=10)

# Run app
root.mainloop()
