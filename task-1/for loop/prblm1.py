import random

# Variables to keep track of counts
count_6 = 0
count_1 = 0
count_two_6s_row = 0

previous_roll = 0  # To track the last roll

# Roll the die at least 20 times 
for i in range(20):
    roll = random.randint(1, 6)  # Simulate dice roll
    print(f"Roll {i+1}: {roll}")

    # Count how many times you rolled a 6
    if roll == 6:
        count_6 += 1

    # Count how many times you rolled a 1
    if roll == 1:
        count_1 += 1

    # Count how many times you rolled two 6s in a row
    if roll == 6 and previous_roll == 6:
        count_two_6s_row += 1

    # Update previous roll
    previous_roll = roll

# Print statistics
print("\n--- Statistics ---")
print(f"Number of times rolled a 6: {count_6}")
print(f"Number of times rolled a 1: {count_1}")
print(f"Number of times rolled two 6s in a row: {count_two_6s_row}")
