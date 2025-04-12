import random

# Options to choose from
options = ["rock", "paper", "scissors"]

# Rules for who wins
win_conditions = {
    "rock": "scissors",  # rock beats scissors
    "paper": "rock",  # paper beats rock
    "scissors": "paper"  # scissors beats paper
}


def play_game():
    print("🎮 Welcome to Rock, Paper, Scissors!")

    while True:
        user = input("Choose rock, paper or scissors (or 'q' to quit): ").lower()

        if user == 'q':
            print("👋 Thanks for playing! Goodbye!")
            break

        if user not in options:
            print("❌ Invalid choice. Please try again.")
            continue

        computer = random.choice(options)

        print(f"\nYou chose: {user}")
        print(f"Computer chose: {computer}")

        if user == computer:
            print("🤝 It's a tie!\n")
        elif win_conditions[user] == computer:
            print("✅ You win!\n")
        else:
            print("💻 Computer wins!\n")


# Run the game
play_game()
