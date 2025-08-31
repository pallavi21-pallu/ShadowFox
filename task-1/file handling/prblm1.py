import csv

# 1. Open the file in read mode
with open("student_marks.csv", "r") as file:
    reader = csv.DictReader(file)  # Reads CSV into a list of dictionaries

    # 2. Create a list of dictionaries from the given data
    students = list(reader)

# 3 & 4. Add 'total_marks' and 'Average' fields
for student in students:
    # Convert all subject marks to integers
    marks = [int(student[subj]) for subj in student if subj not in ["Name", "RollNo"]]
    total = sum(marks)
    average = total / len(marks)

    student["total_marks"] = total
    student["Average"] = round(average, 2)  # round to 2 decimal places

# 5. Create a new file and write updated data
fieldnames = list(students[0].keys())  # All columns including new ones

with open("student_marks_updated.csv", "w", newline="") as new_file:
    writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    writer.writeheader()  # Write the first row (column names)
    writer.writerows(students)  # Write all student data

print("✅ New file 'student_marks_updated.csv' created successfully!")
