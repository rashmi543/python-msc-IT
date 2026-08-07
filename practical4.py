text = input("Enter paragraph: ")
words = text.split()

result = [
    ["Total words:", len(words), words],  
    ["Total unique words:", len(set(words)), list(set(words))],
    ["Longest word:", max(words, key=len)],
    ["Shortest word:", min(words, key=len)]
]

# Repeate words
repeated = []
for w in words:
    if words.count(w) > 1 and w not in repeated:
        repeated.append(w)

result.append(["Repeated words:", repeated])

for item in result:
    print(item)