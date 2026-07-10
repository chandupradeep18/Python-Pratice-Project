#07-06-2026
# Hospital Patient Registration System
class Patient:
    hospital_name = "City Hospital"
    id=1
    def __init__(self,name,age,gender,blood_group,phone):
        self.patient_id = Patient.id
        self.name = name
        self.age = age
        self.gender = gender
        self.blood_group = blood_group
        self.phone = phone
        Patient.id += 1
    
    def __str__(self):
        return f"""--- Patient Details ---
Hospital: {Patient.hospital_name}
Patient ID: {self.patient_id}
Name: {self.name}
Age: {self.age}
Gender: {self.gender}
Blood Group: {self.blood_group}
Phone: {self.phone}"""
    
    @classmethod
    def HospitalInfo(cls):
        return f"""Welcome to {cls.hospital_name}
Total Patients Registered: {cls.id - 1}"""

p1=Patient("John Doe", 30, "Male", "O+", "123-456-7890")
p2=Patient("Jane Smith", 25, "Female", "A-", "987-654-3210")
print(p1)
print(p2)
print(Patient.HospitalInfo())