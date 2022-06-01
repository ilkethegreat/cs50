from cs50 import get_string


text = get_string("Text: ")

letters = 0
for i in range(len(text)):
    if text[i] >= 'a' and text[i] <= 'z' or text[i] >= 'A' and text[i] <= 'Z':
        letters += 1

words = 1
for i in range(len(text)):
    if text[i] == ' ':
        words += 1

sentences = 0
for i in range(len(text)):
    if text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1

CLI = (0.0588 * letters / words * 100) - (0.296 * sentences / words * 100) - 15.8
CLIr = round(CLI)

if CLIr < 1:
    print("Before Grade 1")
if CLIr >= 16:
    print("Grade 16+")
else:
    print(f"Grade {CLIr}")
