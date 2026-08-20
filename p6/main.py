from student import read_student
from ranking import generate_ranks
from report import display_students


def main():

    print("=" * 50)
    print("       STUDENT RANK PROCESSING ENGINE")
    print("=" * 50)

    # Read student records
    students = read_student()

    # Generate ranks
    students = generate_ranks(students)

    # Display final result
    display_students(students)


if __name__ == "__main__":
    main()
