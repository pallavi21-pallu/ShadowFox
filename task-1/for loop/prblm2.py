total_jumping_jacks = 100
done_jumping_jacks = 0
set_size = 10

while done_jumping_jacks < total_jumping_jacks:
    # Perform 10 jumping jacks
    done_jumping_jacks += set_size
    print(f"You have completed {done_jumping_jacks} jumping jacks.")

    # If all are done
    if done_jumping_jacks >= total_jumping_jacks:
        print("Congratulations! You completed the workout!")
        break

    # Ask if tired
    tired = input("Are you tired? (yes/y or no/n): ")

    if tired in ("yes", "y"):
        skip = input("Do you want to skip the remaining sets? (yes/y or no/n): ")
        if skip in ("yes", "y"):
            print(f"You completed a total of {done_jumping_jacks} jumping jacks.")
            break
        else:
            remaining = total_jumping_jacks - done_jumping_jacks
            print(f"{remaining} jumping jacks remaining.")
    elif tired in ("no", "n"):
        remaining = total_jumping_jacks - done_jumping_jacks
        print(f"{remaining} jumping jacks remaining.")
    else:
        print("Invalid input! Continuing...")

