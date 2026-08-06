roll = [1, 2, 3, 5, 6]

roll.sort()

for i in range(len(roll)):
    if roll[i] == i + 1:
        continue
    else:
        print("Missing roll number is:", i + 1)
        break