def read_student():
    students = []

    n = int(input("Enter number of students: "))

    for i in range(n):
        print(f"\nEnter details of Student {i + 1}")

        roll = int(input("Roll No: "))
        name = input("Name: ")

        marks = []

        for j in range(5):
            mark = float(input(f"Subject {j + 1} Marks: "))
            marks.append(mark)

        total = calculate_total(marks)
        percentage = calculate_percentage(total)
        grade = assign_grade(percentage)

        student = {
            "roll": roll,
            "name": name,
            "marks": marks,
            "total": total,
            "percentage": percentage,
            "grade": grade
        }

        students.append(student)

    return students


def calculate_total(marks):
    return sum(marks)


def calculate_percentage(total):
    return total / 5


def assign_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"