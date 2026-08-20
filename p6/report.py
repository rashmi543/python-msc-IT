def display_students(students):

    print("\n")
    print("=" * 75)
    print("                    STUDENT RESULT")
    print("=" * 75)

    print(
        "Rank\tRoll No\tName\tTotal\tPercentage\tGrade"
    )

    print("-" * 75)

    for student in students:

        print(
            f"{student['rank']}\t"
            f"{student['roll']}\t"
            f"{student['name']}\t"
            f"{student['total']}\t"
            f"{student['percentage']:.2f}%\t\t"
            f"{student['grade']}"
        )

    print("=" * 75)