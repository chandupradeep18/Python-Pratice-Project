#25-06-2026
#Student result processor
class InvalidMarksError(Exception):
    def __init__(self, subject,marks):
        self.subject=subject
        self.marks=marks
        super().__init__(f"Invalid marks for '{subject}': {marks}. Must be between 0 and 100.")

class SubjectNotFoundError(Exception):
    def __init__(self, subject):
        self.subject=subject
        super().__init__(f"Subject '{subject}' not found.")

class InsufficientDataError(Exception):
    def __init__(self, count,minimum):
        self.count=count
        self.minimum=minimum
        super().__init__(f"Only {count} subject(s) recorded. Minimum {minimum} required.")

class Student:
    SUBJECTS={'Telugu','Hindi','Sankrit'}
    def __init__(self,name,roll_number):
        self.name=name
        self.roll_number=roll_number
        self.marks = {}
    

    def add_marks(self,subject,marks):
        try:
            
