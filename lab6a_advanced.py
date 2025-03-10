#!/usr/bin/env python3
# Author ID: [seneca_id]

import threading
import weakref
import logging
import asyncio
import traceback
from collections import OrderedDict
from functools import lru_cache
from typing import Dict, List, Union, Generator


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# 📌 Custom Exceptions for Data Validation
class StudentException(Exception):
    """Base Exception for Student Class"""
    pass


class InvalidGradeError(StudentException):
    """Raised when an invalid grade is entered."""
    pass


class InvalidCourseError(StudentException):
    """Raised when an invalid course name is entered."""
    pass


# 📌 Metaclass for Tracking Instances
class StudentMeta(type):
    """Metaclass to track live Student instances and memory management."""
    _instances = []

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        cls._instances.append(weakref.finalize(instance, cls._instances.remove, instance))
        logging.info(f"Student {instance.name} created.")
        return instance

    @classmethod
    def count_instances(cls) -> int:
        """Returns the number of active Student instances."""
        return len(cls._instances)


# 📌 Base Student Class
class Student(metaclass=StudentMeta):
    """Ultra-Advanced Student Class with Extreme Features"""

    __slots__ = ("_name", "_number", "_courses", "_lock")

    def __init__(self, name: str, number: Union[int, str]):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(number, (int, str)):
            raise TypeError("Student number must be an integer or string")

        self._name = name
        self._number = str(number)  # Ensure student number is a string
        self._courses = OrderedDict()  # Maintain insertion order of courses
        self._lock = threading.Lock()  # Thread-safety lock

    def __repr__(self) -> str:
        return f"Student({self._name}, {self._number})"

    @property
    def name(self) -> str:
        """Getter for name"""
        return self._name

    @property
    def number(self) -> str:
        """Getter for number"""
        return self._number

    def addGrade(self, course: str, grade: float) -> None:
        """Adds a grade to the student with error handling."""
        if not isinstance(course, str) or len(course) < 3:
            raise InvalidCourseError("Course name must be a valid string with at least 3 characters.")
        if not isinstance(grade, (int, float)) or not (0.0 <= grade <= 4.0):
            raise InvalidGradeError("Grade must be between 0.0 and 4.0.")

        with self._lock:
            self._courses[course] = grade
            logging.info(f"Added grade {grade} for {course} to {self._name}")

    @lru_cache(maxsize=10)
    def displayGPA(self) -> str:
        """Calculates and returns the GPA using caching."""
        if not self._courses:
            return f"GPA of student {self._name} is 0.0"

        gpa = sum(self._courses.values()) / len(self._courses)
        return f"GPA of student {self._name} is {gpa:.2f}"

    def displayCourses(self) -> List[str]:
        """Returns a sorted list of passed courses."""
        return sorted([course for course, grade in self._courses.items() if grade > 0.0], key=lambda x: -self._courses[x])

    def __iter__(self) -> Generator[str, None, None]:
        """Allows iteration over courses."""
        for course in self._courses:
            yield course

    def __contains__(self, course: str) -> bool:
        """Checks if a course exists in the student's records."""
        return course in self._courses

    def __lt__(self, other: "Student") -> bool:
        """Compare students based on GPA."""
        return float(self.displayGPA().split()[-1]) < float(other.displayGPA().split()[-1])

    def __eq__(self, other: "Student") -> bool:
        """Compare students based on name and number."""
        return self._name == other._name and self._number == other._number

    @classmethod
    def totalStudents(cls) -> int:
        """Returns the total number of Student instances."""
        return StudentMeta.count_instances()


# 📌 Advanced Inheritance - ScholarshipStudent
class ScholarshipStudent(Student):
    """Specialized Student with Scholarship Eligibility"""
    def __init__(self, name: str, number: Union[int, str], scholarship_amount: float):
        super().__init__(name, number)
        if scholarship_amount < 0:
            raise ValueError("Scholarship amount cannot be negative")
        self.scholarship_amount = scholarship_amount

    def isEligible(self) -> bool:
        """Checks if student is eligible for a scholarship (GPA > 3.5)"""
        return float(self.displayGPA().split()[-1]) > 3.5

    def __repr__(self) -> str:
        return f"ScholarshipStudent({self.name}, {self.number}, Scholarship: ${self.scholarship_amount})"


# 📌 Multi-threaded GPA Calculation
async def async_gpa_calculation(student: Student):
    """Simulate GPA calculation asynchronously."""
    await asyncio.sleep(1)
    print(f"[ASYNC] {student.name}'s GPA is {student.displayGPA()}")


# 📌 Main Execution
if __name__ == "__main__":
    student1 = Student("John", "013454900")
    student1.addGrade("ops445", 3.0)
    student1.addGrade("ops245", 2.0)
    student1.addGrade("uli101", 1.0)

    student2 = ScholarshipStudent("Jessica", 123456, 5000)
    student2.addGrade("ipc144", 4.0)
    student2.addGrade("cpp244", 3.5)

    print(student1.displayGPA())
    print(student2.displayGPA())

    # Run async GPA calculation
    asyncio.run(async_gpa_calculation(student1))

    # Demonstrate Operator Overloading
    print(f"Is {student2.name} eligible for a scholarship? {student2.isEligible()}")
    print(f"Is {student1} better than {student2}? {'Yes' if student1 < student2 else 'No'}")
    print(f"Total students created: {Student.totalStudents()}")

