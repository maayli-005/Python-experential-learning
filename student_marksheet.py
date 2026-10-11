# Student Marksheet Automation - High Volume
# Phase 2 Code Implementation

import csv

students = []

def get_marks(subject):
    while True:
        try:
            marks = float(input(f"{subject}: "))
            if 0 <= marks <= 100:
                return marks
            print("Invalid marks! Enter marks between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a number.")


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

    subjects["Python"] = get_marks("Python: ")
    subjects["Mathematics"] = get_marks("Mathematics: ")
    subjects["Data Structures"] = get_marks("Data Structures: ")
    subjects["Computer Networks"] = get_marks("Computer Networks: ")
    subjects["Database"] = get_marks("Database: ")

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


# Save student records without deleting old records
import os

file_exists = os.path.exists("marksheets.csv")
file_is_empty = not file_exists or os.path.getsize("marksheets.csv") == 0

with open("marksheets.csv", "a", newline="") as file:
    writer = csv.writer(file)

    if file_is_empty:
        writer.writerow([
            "Rank", "Name", "Roll No", "Python",
            "Mathematics", "Data Structures",
            "Computer Networks", "Database",
            "Total", "Percentage", "Grade", "Result"
        ])

    for student in students:
        writer.writerow([
            student["rank"],
            student["name"],
            student["roll_no"],
            student["subjects"]["Python"],
            student["subjects"]["Mathematics"],
            student["subjects"]["Data Structures"],
            student["subjects"]["Computer Networks"],
            student["subjects"]["Database"],
            student["total"],
            round(student["percentage"], 2),
            student["grade"],
            student.get("result", "N/A")
        ])

print("Student records saved successfully!")


print("==============================================")
print("       Marksheet Generated Successfully!")
print("==============================================")

# Search student by roll number
search_roll = input("\nEnter roll number to search: ")

found = False

for student in students:
    if str(student["roll_no"]) == search_roll:
        print("\nStudent Found!")
        print("Name       :", student["name"])
        print("Roll No.   :", student["roll_no"])
        print("Total      :", student["total"])
        print("Percentage :", round(student["percentage"], 2), "%")
        print("Grade      :", student["grade"])
        print("Rank       :", student["rank"])
        found = True
        break

if not found:
    print("Student not found!")

# Search previously saved student records from CSV
print("\n--- SEARCH SAVED CSV RECORDS ---")
csv_roll = input("Enter roll number to search in CSV: ").strip()

found_in_csv = False

try:
    with open("marksheets.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for record in reader:
            if record["Roll No"].strip() == csv_roll:
                print("\nSaved Record Found!")
                print("Name       :", record["Name"])
                print("Roll No    :", record["Roll No"])
                print("Total      :", record["Total"])
                print("Percentage :", record["Percentage"], "%")
                print("Grade      :", record["Grade"])
                print("Rank       :", record["Rank"])
                found_in_csv = True
                break

    if not found_in_csv:
        print("No saved record found for this roll number.")

except FileNotFoundError:
    print("CSV file not found. Generate a marksheet first.")
