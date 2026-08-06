password = input("Enter password: ") 
f = []
special = "!@#$%^&*(),.?\":{}|<>"

if not any(i.isupper() for i in password):
    f.append("uppercase")

if not any(i.islower() for i in password):
    f.append("lowercase")

if not any(i.isdigit() for i in password):
    f.append("digit")

if not any(i in special for i in password):
    f.append("special character")

for i in range(len(password)-1):
    if password[i] == password[i+1]:
        f.append("repeated characters")
        break

if not f:
    print("Strong Password")
else:
    print("Weak Password")
    print("Failed:", f)