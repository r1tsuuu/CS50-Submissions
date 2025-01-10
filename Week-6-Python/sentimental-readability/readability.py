text = input("Text: ")

w = 1
s = 0
l = 0

for c in text:
    if c in [".", "?", "!"]:
        s += 1
    elif c == " ":
        w += 1
    elif c.isalpha():
        l += 1

L = (l / w) * 100
S = (s / w) * 100

C = 0.0588 * L - 0.296 * S - 15.8
level = round(C)

if level < 1:
    print("Before Grade 1")
elif level > 16:
    print("Grade 16+")
else:
    print(f"Grade {level}")