#!/usr/bin/env python3
# Author ID: sdelgado

from collections import OrderedDict  # Import OrderedDict to maintain order

class Student:
    # Initialize student with name, student number, and an empty ordered dictionary for courses
    def __init__(self, name, number):
        self.name = name  # Store student name
        self.number = str(number)  # Convert number to string to avoid TypeError
        self.courses = OrderedDict()  # Use OrderedDict to maintain insertion order

    # Return student name and number
    def displayStudent(self):
        return f"Student Name: {self.name}\nStudent Number: {self.number}"

    # Add a new course and grade to the student's record
    def addGrade(self, course, grade):
        self.courses[course] = grade  # Keep the order in which courses were added

    # Calculate and return the GPA of the student
    def displayGPA(self):
        if len(self.courses) == 0:  # Check to prevent ZeroDivisionError
            return f"GPA of student {self.name} is 0.0"
        
        gpa = sum(self.courses.values()) / len(self.courses)  # Compute GPA
        return f"GPA of student {self.name} is {gpa:.1f}"  # Format to 1 decimal place

    # Return a list of courses where the student received a grade greater than 0.0 (Maintaining order)
    def displayCourses(self):
        return [course for course, grade in self.courses.items() if grade > 0.0]


# Main script execution for testing
if __name__ == "__main__":
    # Create first student and add courses
    student1 = Student("John", "013454900")
    student1.addGrade("ops445", 3.0)
    student1.addGrade("ops245", 2.0)
    student1.addGrade("uli101", 1.0)

    # Create second student and add courses (with integer student number to test fix)
    student2 = Student("Jessica", 123456)  
    student2.addGrade("ipc144", 4.0)
    student2.addGrade("cpp244", 3.5)
    student2.addGrade("cpp344", 0.0)  # Failed course

    # Display student information and GPA
    print(student1.displayStudent())
    print(student1.displayGPA())
    print(student1.displayCourses())  # Expected: ['ops445', 'ops245', 'uli101']

    print(student2.displayStudent())
    print(student2.displayGPA())
    print(student2.displayCourses())  # Expected: ['cpp244', 'ipc144']
