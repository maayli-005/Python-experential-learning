# Student Marksheet Automation - High Volume
# Phase 2 - 75% Complete

students = []

# Function to calculate result
def calculate_result(marks):
    total = sum(marks)
    percentage = total / len(marks)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    if percentage >= 40:
        result = "PASS"
    else:
        result = "FAIL"

    return total, percentage, grade, result


# Function to enter valid marks
def get_marks(subject):
    while True:
        try:
            marks = float(input(f"Enter marks for {subject} (0-100): "))

            if 0 <= marks <= 100:
                return marks
            else:
                print("Invalid marks! Enter marks between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# Number of students
n = int(input("Enter number of students: "))

# Input student records
for i in range(n):

    print("\n" + "=" * 45)
    print(f"ENTER DETAILS OF STUDENT {i + 1}")
    print("=" * 45)

    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")

    print("\nEnter Subject Marks:")

    mathematics = get_marks("Mathematics")
    python = get_marks("Python Programming")
    data_structures = get_marks("Data Structures")
    dbms = get_marks("DBMS")
    communication = get_marks("Communication")

    marks = [
        mathematics,
        python,
        data_structures,
        dbms,
        communication
    ]

    total, percentage, grade, result = calculate_result(marks)

    student = {
        "name": name,
        "roll_no": roll_no,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "result": result
    }

    students.append(student)


# Ranking students according to percentage
students.sort(
    key=lambda x: x["percentage"],
    reverse=True
)


# Display final marksheets
print("\n\n")
print("=" * 60)
print("             STUDENT MARKSHEET SYSTEM")
print("=" * 60)

for rank, student in enumerate(students, start=1):

    print("\n" + "-" * 60)
    print(f"Rank       : {rank}")
    print(f"Name       : {student['name']}")
    print(f"Roll No.   : {student['roll_no']}")
    print("-" * 60)

    print(f"Mathematics        : {student['marks'][0]:.0f}")
    print(f"Python Programming : {student['marks'][1]:.0f}")
    print(f"Data Structures    : {student['marks'][2]:.0f}")
    print(f"DBMS               : {student['marks'][3]:.0f}")
    print(f"Communication      : {student['marks'][4]:.0f}")

    print("-" * 60)

    print(f"Total      : {student['total']:.0f} / 500")
    print(f"Percentage : {student['percentage']:.2f}%")
    print(f"Grade      : {student['grade']}")
    print(f"Result     : {student['result']}")

    print("-" * 60)


# Overall summary
print("\n")
print("=" * 60)
print("                 CLASS SUMMARY")
print("=" * 60)

print(f"Total Students Processed : {len(students)}")

passed = sum(1 for s in students if s["result"] == "PASS")
failed = len(students) - passed

print(f"Students Passed          : {passed}")
print(f"Students Failed          : {failed}")

if students:
    print(f"Highest Percentage       : {students[0]['percentage']:.2f}%")
    print(f"Top Student              : {students[0]['name']}")
