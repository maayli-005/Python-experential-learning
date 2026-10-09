# Student Marksheet Automation - High Volume
# Phase 2 Code Implementation

students = []

# Grade calculation function
def calculate_grade(percentage):
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
    elif percentage >= 40:
        return "E"
    else:
        return "F"


# Input number of students
n = int(input("Enter number of students: "))

# Enter student details
for i in range(n):

    print("\n-----------------------------")
    print("Enter details for Student", i + 1)
    print("-----------------------------")

    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")

    print("Enter marks out of 100:")

    subjects = {}

    subjects["Python"] = float(input("Python: "))
    subjects["Mathematics"] = float(input("Mathematics: "))
    subjects["Data Structures"] = float(input("Data Structures: "))
    subjects["Computer Networks"] = float(input("Computer Networks: "))
    subjects["Database"] = float(input("Database: "))

    # Calculate total and percentage
    total = sum(subjects.values())
    percentage = total / len(subjects)

    # Calculate grade
    grade = calculate_grade(percentage)

    # Store student record
    student = {
        "name": name,
        "roll_no": roll_no,
        "subjects": subjects,
        "total": total,
        "percentage": percentage,
        "grade": grade
    }

    students.append(student)


# Determine rank based on percentage
students.sort(key=lambda x: x["percentage"], reverse=True)

for i in range(len(students)):
    students[i]["rank"] = i + 1


# Display final marksheets
print("\n\n==============================================")
print("       STUDENT MARKSHEET AUTOMATION")
print("==============================================")

for student in students:

    print("\n----------------------------------------------")
    print("Name       :", student["name"])
    print("Roll No.   :", student["roll_no"])
    print("----------------------------------------------")

    for subject, marks in student["subjects"].items():
        print(f"{subject:<20}: {marks}")

    print("----------------------------------------------")
    print("Total      :", student["total"], "/ 500")
    print("Percentage :", round(student["percentage"], 2), "%")
    print("Grade      :", student["grade"])
    print("Rank       :", student["rank"])
    print("----------------------------------------------")


# Display ranking summary
print("\n\n==============================================")
print("             RANKING SUMMARY")
print("==============================================")

print(f"{'Rank':<8}{'Name':<20}{'Percentage':<15}{'Grade'}")
print("----------------------------------------------")

for student in students:
    print(
        f"{student['rank']:<8}"
        f"{student['name']:<20}"
        f"{student['percentage']:<15.2f}"
        f"{student['grade']}"
    )

print("==============================================")
print("       Marksheet Generated Successfully!")
print("==============================================")