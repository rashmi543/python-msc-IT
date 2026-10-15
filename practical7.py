class Course:
    def __init__(self, code, day, start, end):
        self.code = code
        self.day = day
        self.start = start
        self.end = end


class Student:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def __str__(self):
        return self.sid + " " + self.name


n = int(input("Enter number of students: "))

students = []

for i in range(n):

    print("\nStudent", i + 1)

    sid = input("Enter Student ID: ")
    name = input("Enter Student Name: ")

    s = Student(sid, name)

    m = int(input("Enter number of courses: "))

    for j in range(m):

        print("\nCourse", j + 1)

        code = input("Course Code: ")
        day = input("Day: ")
        start = int(input("Start Time: "))
        end = int(input("End Time: "))

        c = Course(code, day, start, end)

        s.add_course(c)

    students.append(s)


print("\n RESULT")

for s in students:

    print("\nStudent:", s.name)
    print("ID:", s.sid)

    conflict = False

    for i in range(len(s.courses)):

        for j in range(i + 1, len(s.courses)):

            c1 = s.courses[i]
            c2 = s.courses[j]

            if c1.day == c2.day:
                if c1.start < c2.end and c2.start < c1.end:

                    print("Conflict:", c1.code, "and", c2.code)
                    conflict = True

    if conflict == False:
        print("No Conflict")

    print("Total Courses:", len(s.courses))

    print("Timetable:")

    for c in s.courses:
        print(c.code, c.day, c.start, "-", c.end)