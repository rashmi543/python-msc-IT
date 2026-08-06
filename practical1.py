mylist = [1, 2, 3, 4, 4, 4, 5]

result = []

for num in mylist:
    if mylist.count(num) > 1 and num not in result:
        result.append(num)

print(result)