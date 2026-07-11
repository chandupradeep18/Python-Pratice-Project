#02-07-2026
#Medical Health Records Vault
import uuid
from datetime import datetime,timedelta

class AuditLogger:
    total_logs_recorded=0
    def __init__(self):
        self.logs=[]
    def logger(self,user_role,action,status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ROLE: {user_role.upper()} | ACTION: {action} | STATUS: {status}"
        self.logs.append(log_entry)
        AuditLogger.total_logs_recorded += 1

class MedicalVisit:
    def __init__(self,doctor,diagnosis,prescription,notes):
        self.date=datetime.today().isoformat()
        self.doctor=doctor
        self.diagnosis=diagnosis
        self.prescription=prescription
        self.notes=notes

class Patient:
    hospital_network = "Global Health Alliance"
    supported_insurance_tiers = ['Basic', 'Premium', 'Platinum']
    def __init__(self, name, dob,ssn, insurance_tier):
        self.patient_id = str(uuid.uuid4())[:8]
        self.name = name
        self.dob = dob
        if insurance_tier not in Patient.supported_insurance_tiers:
            self.__insurance_tier="Basic"
        else:
            self.__insurance_tier = insurance_tier
        if not Patient.validate_ssn_format(ssn):
            raise ValueError("Invalid SSN Format. Must be XXX-XX-XXXX")
        self.__ssn=ssn
        self.__medical_history=[]
        self.__account_balance=0.0
    
    @staticmethod
    def validate_ssn_format(ssn):
        if not isinstance(ssn,str) or len(ssn)!=11:
            return False
        parts=ssn.split('-')
        if len(parts)==3 and all(part.isdigit() for part in parts):
            return True
        return False
    
    @classmethod
    def get_supported_insurance(cls):
        return cls.supported_insurance_tiers
    
    def __mark_ssn(self):
        return f"***-**-{self.__ssn[-4:]}"
    
    def __calculate_visit_cost(self):
        base_cost = 100.0
        if self.__insurance_tier == 'Premium':
            return base_cost * 0.8
        elif self.__insurance_tier == 'Platinum':
            return base_cost * 0.5
        else:
            return base_cost
    
    def _bill_patient(self,amount):
        self.__account_balance += amount
    
    def add_medical_visit(self,doctor,diagnosis,prescription,user_role):
        if user_role.lower() not in ['doctor','admin']:
            return False, "Unauthorized role for adding medical visit."
        visit=MedicalVisit(doctor,diagnosis,prescription,"")
        self.__medical_history.append(visit)
        cost=self.__calculate_visit_cost()
        self._bill_patient(cost)
        return True, f"Medical visit added. Patient billed ${cost:.2f}."
    
    def get_medical_history(self,user_role):
        if user_role.lower() not in ['doctor','admin']:
            return False, "Unauthorized role for adding medical visit."
        if not self.__medical_history:
            return True, "No medical history available."
        history_report = f"\n--- Medical History for {self.name} ---\n"
        for visit in self.__medical_history:
            history_report += f"Date: {visit.date}, Doctor: {visit.doctor}, Diagnosis: {visit.diagnosis}, Prescription: {visit.prescription}\n"
            history_report += f"Notes: {visit.notes}\n"
        return True, history_report
    
    def get_patient_summary(self,user_role):
        summary = f"Patient: {self.name} (ID: {self.patient_id})\n"
        summary += f"Hospital: {Patient.hospital_network}\n"
        if user_role.lower() in ['admin', 'billing', 'doctor']:
            summary+=f"SSN: {self.__mark_ssn()}\n"
            summary += f"Insurance Tier: {self.__insurance_tier}\n"
        if user_role.lower() in ['admin', 'billing']:
            summary += f"Account Balance: ${self.__account_balance:.2f}\n"
        return summary

class RecordsVault:
    def __init__(self):
        self.patients={}
        self.logger=AuditLogger()
    
    def register_patient(self,patient : Patient,user_role):
        if user_role.lower() not in ['admin']:
            self.logger.logger(user_role,"Add Patient","Failed - Unauthorized")
            return "Unauthorized role for adding patient."
        if patient.patient_id in self.patients:
            self.logger.logger(user_role,"Add Patient","Failed - Duplicate ID")
            return  "Patient with this ID already exists."
        self.patients[patient.patient_id]= patient
        self.logger.logger(user_role,'Add Patient',"Success")
        return f"Patient {patient.name} registered successfully."
    
    def access_patient_records(self,patient_id,user_role):
        if patient_id not in self.patients:
            self.logger.logger(user_role,"Access Patient Records","Failed - Not Found")
            return "Patient not found."
        patient=self.patients[patient_id]
        status,records =patient.get_medical_history(user_role)
        if status:
            self.logger.logger(user_role,"Access Patient Records","Success")
        else:
            self.logger.logger(user_role,"Access Patient Records","Failed - Unauthorized")
        return records

if __name__ == "__main__":
    # Initialize the Vault
    vault = RecordsVault()
    
    print(f"--- Welcome to {Patient.hospital_network} Vault ---\n")

    # 1. Create a Patient Object
    # Notice we pass a valid SSN because of our Static Method validation
    p1 = Patient(name="Alice Smith", dob="1985-04-12", 
                 ssn="123-45-6789", insurance_tier="Platinum")
    print(vault.register_patient(p1,"admin"))
    status, msg = p1.add_medical_visit(
        "Gregory House", 
        "Lupus (wait, it's never Lupus) - Severe Migraine", 
        "Sumatriptan 50mg", 
        "doctor"
    )
    print(msg)

    print("\n--- Receptionist requesting Patient Summary ---")
    print(p1.get_patient_summary(user_role="receptionist"))

    print("\n--- Billing Dept requesting Patient Summary ---")
    print(p1.get_patient_summary(user_role="billing"))

    print("\n--- Unauthorized User Requesting Medical Records ---")
    print(vault.access_patient_records(p1.patient_id, "billing"))

    print("\n--- Doctor Requesting Medical Records ---")
    print(vault.access_patient_records(p1.patient_id, "doctor"))

    # 6. Audit Log Check
    print("\n--- System Audit Log ---")
    for log in vault.logger.logs:
        print(log)
    print(f"Total system logs recorded: {AuditLogger.total_logs_recorded}")