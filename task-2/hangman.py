import random

# --- Step 1: ASCII Art for Stickman ---
HANGMAN_PICS = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]


def hangman():
    # --- Step 2: Choose a category and word ---
    categories = {
        "Fruits": ["apple", "banana", "grape", "mango", "orange"],
        "Animals": ["elephant", "tiger", "lion", "giraffe", "zebra"],
        "Programming": ["python", "java", "variable", "function", "computer"]
    }
    category = random.choice(list(categories.keys()))
    word = random.choice(categories[category])

    # --- Step 3: Initialize game state ---
    word_letters = set(word)        # letters still to guess
    guessed_letters = set()         # correct guesses
    wrong_guesses = set()           # incorrect guesses
    attempts = len(HANGMAN_PICS) - 1

    # --- Step 4: Display welcome message and rules ---
    print("🎮 Welcome to Hangman!")
    print(f"💡 Hint: The word is from the category **{category}**")
    print(f"🔤 The word has {len(word)} letters.")
    print("👉 You can type '*' to reveal one random letter (costs 1 attempt).\n")

    # --- Step 5: Main Game Loop ---
    while attempts > 0 and len(word_letters) > 0:
        # Display current hangman stage
        print(HANGMAN_PICS[len(HANGMAN_PICS) - 1 - attempts])
        print("Word so far:", " ".join([letter if letter in guessed_letters else "_" for letter in word]))
        print("Wrong guesses:", " ".join(sorted(wrong_guesses)))
        print(f"Attempts left: {attempts}\n")

        # --- Step 6: Take user input ---
        guess = input("Guess a letter: ").lower()

        # --- Step 7: If user asks for hint ---
        if guess == "*":
            if word_letters:
                revealed = random.choice(list(word_letters))
                guessed_letters.add(revealed)
                word_letters.remove(revealed)
                attempts -= 1
                print(f"💡 Hint used! The letter '{revealed}' is revealed. (-1 attempt)\n")
            else:
                print("⚠️ No letters left to reveal.\n")
            continue

        # --- Step 8: Validate input ---
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter a single letter.\n")
            continue

        if guess in guessed_letters or guess in wrong_guesses:
            print("⚠️ You already guessed that letter.\n")
            continue

        # --- Step 9: Check guess ---
        if guess in word_letters:
            guessed_letters.add(guess)
            word_letters.remove(guess)
            print("✅ Good guess!\n")
        else:
            wrong_guesses.add(guess)
            attempts -= 1
            print("❌ Wrong guess!\n")

    # --- Step 10: Win/Loss ---
    if not word_letters:
        print("\n🎉 Congratulations! You guessed the word:", word)
    else:
        print(HANGMAN_PICS[-1])
        print("\n💀 Game Over! The word was:", word)

    # --- Step 11: Play Again ---
    again = input("\nDo you want to play again? (yes/no): ").lower()
    if again == "yes":
        hangman()


# --- Step 12: Run the Game ---
hangman()
