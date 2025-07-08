import random
import os
import json
from datetime import datetime

DIFFICULTIES = {
    "easy": {"tries": 10, "range": 100},
    "medium": {"tries": 7, "range": 100},
    "hard": {"tries": 5, "range": 100},
}
HIGH_SCORES_FILE = "high_scores.json"


def clear_screen():
    """Clears the console screen."""

    if os.name == 'nt':
        _ = os.system('cls')

    else:
        _ = os.system('clear')

def get_player_name():
    """Prompts the user for their name."""
    name = input("Enter your name (optional, press Enter to be Anonymous): ").strip()
    return name if name else "Anonymous"

def get_difficulty_choice():
    """Prompts the user to choose a difficulty level."""
    while True:
        print("\n--- Choose Difficulty ---")
        for level, settings in DIFFICULTIES.items():
            print(f"  {level.capitalize()}: {settings['tries']} tries (1 - {settings['range']})")
        choice = input("Enter difficulty (Easy/Medium/Hard): ").lower()
        if choice in DIFFICULTIES:
            return choice
        else:
            print("Invalid choice. Please choose Easy, Medium, or Hard.")

def generate_secret_number(difficulty_level):
    """Generates a random secret number based on difficulty."""
    max_range = DIFFICULTIES[difficulty_level]["range"]
    return random.randint(1, max_range)

def get_user_guess(max_range):
    """Prompts the user for a guess and validates it."""
    while True:
        try:
            guess = int(input(f"Enter your guess (1 - {max_range}): "))
            if 1 <= guess <= max_range:
                return guess
            else:
                print(f"Please enter a number within the range (1 - {max_range}).")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def generate_hint(secret_number, attempts_made, last_guess=None):
    """Generates a hint based on the secret number and game state."""
    hints = []


    if secret_number % 2 == 0:
        hints.append("The number is even.")
    else:
        hints.append("The number is odd.")


    if secret_number > 10:
        if secret_number % 3 == 0:
            hints.append("It is divisible by 3.")
        elif secret_number % 5 == 0:
            hints.append("It is divisible by 5.")
        elif secret_number % 7 == 0:
            hints.append("It is divisible by 7.")

    
    if last_guess is not None:
        if last_guess < secret_number:
            hints.append(f"It's greater than {last_guess}.")
        elif last_guess > secret_number:
            hints.append(f"It's less than {last_guess}.")

    
    random.shuffle(hints)
    return " ".join(hints[:2]) 

def load_high_scores():
    """Loads high scores from a JSON file."""
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, 'r') as f:
                scores = json.load(f)
                
                return sorted(scores, key=lambda x: x['attempts'])
        except json.JSONDecodeError:
            print(f"Warning: Could not read {HIGH_SCORES_FILE}. Starting with empty scores.")
            return []
    return []

def save_high_score(score):
    """Saves a new score to the JSON file."""
    scores = load_high_scores()
    scores.append(score)
    
    scores.sort(key=lambda x: x['attempts'])
    try:
        with open(HIGH_SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=4)
    except IOError as e:
        print(f"Error saving high score: {e}")

def display_leaderboard(scores):
    """Displays the sorted high scores."""
    clear_screen()
    print("\n" + "="*30)
    print("      🏆 HIGH SCORES 🏆")
    print("="*30)

    if not scores:
        print("\nNo scores recorded yet. Be the first to play!")
    else:
        print(f"\n{'Rank':<5} {'Player':<15} {'Difficulty':<10} {'Attempts':<10} {'Date':<12}")
        print("-" * 60)
        for i, score in enumerate(scores[:10]): 
            print(f"{i+1:<5} {score['name']:<15} {score['difficulty'].capitalize():<10} {score['attempts']:<10} {score['date']:<12}")
    print("\n" + "="*30)
    input("Press Enter to continue...")



def play_game():
    """Manages the flow of a single game session."""
    clear_screen()
    print("="*40)
    print("    Welcome to the Number Guessing Game!")
    print("="*40)

    player_name = get_player_name()
    difficulty_choice = get_difficulty_choice()
    
    settings = DIFFICULTIES[difficulty_choice]
    secret_number = generate_secret_number(difficulty_choice)
    max_attempts = settings["tries"]
    max_range = settings["range"]
    
    attempts_made = 0
    last_guess = None

    print(f"\nOkay {player_name}, I'm thinking of a number between 1 and {max_range}.")
    print(f"You have {max_attempts} attempts to guess it.")

    game_won = False
    while attempts_made < max_attempts:
        print(f"\nAttempts left: {max_attempts - attempts_made}")
        guess = get_user_guess(max_range)
        last_guess = guess 
        attempts_made += 1

        if guess == secret_number:
            print(f"\n🎉 Congratulations, {player_name}! You guessed the number {secret_number} in {attempts_made} attempts!")
            game_won = True
            break
        elif guess < secret_number:
            print("Too Low! Try again.")
        else:
            print("Too High! Try again.")
        
    
        if attempts_made >= 3 and not game_won and (attempts_made == 3 or (attempts_made > 3 and attempts_made % 2 == 1)):
            print(f"Hint: {generate_hint(secret_number, attempts_made, last_guess)}")

    if not game_won:
        print(f"\nGame Over! You ran out of attempts. The secret number was {secret_number}.")

    
    if game_won:
        score = {
            "name": player_name,
            "difficulty": difficulty_choice,
            "attempts": attempts_made,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        save_high_score(score)
        print("Your score has been saved to the leaderboard!")

    input("\nPress Enter to continue...")

def main_menu():
    """Displays the main menu and handles user choices."""
    high_scores = load_high_scores()

    while True:
        clear_screen()
        print("\n--- Main Menu ---")
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            play_game()
        elif choice == '2':
            display_leaderboard(high_scores)
            high_scores = load_high_scores() 
        elif choice == '3':
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to try again...")


if __name__ == "__main__":
    main_menu()