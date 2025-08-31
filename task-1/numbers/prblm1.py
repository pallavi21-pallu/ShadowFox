def format_numbers(num, char):
    result = "{0:{1}}".format(num, char)
    print(result)

format_numbers(145, 'o')  # This uses 'o' for octal representation
