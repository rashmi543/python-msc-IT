def generate_ranks(students):

    students.sort(key=lambda x: x["total"], reverse=True)

    for i in range(len(students)):

        if i > 0 and students[i]["total"] == students[i - 1]["total"]:
            students[i]["rank"] = students[i - 1]["rank"]
        else:
            students[i]["rank"] = i + 1

    return students