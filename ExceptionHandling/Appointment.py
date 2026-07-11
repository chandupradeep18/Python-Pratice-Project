#24-06-2026
from datetime import datetime,date

class AppointmentError(Exception):
    pass
class DoctorUnavailableError(AppointmentError):
    pass
class PatientLimitExceededError(AppointmentError):
    pass
class PastDateError(AppointmentError):
    pass
class InvalidTimeSlotError(AppointmentError):
    pass
class SlotConflictError(AppointmentError):
    def __init__(self, conflicting_appointment):
        self.appointment=conflicting_appointment
        message=(f"Slot already booked by {conflicting_appointment.patient_name} at {conflicting_appointment.time}")
        super().__init__(message)

class Appointment:
    def __init__(self,patient,doctor,app_date,time_slot):
        self.patient_name = patient
        self.doctor_name  = doctor
        self.date         = app_date
        self.time         = time_slot
        self.status       = "Confirmed"
    
    def __str__(self):
        return (f"{self.patient_name} with "
                f"Dr. {self.doctor_name} on "
                f"{self.date} at {self.time}")

class Doctor:
    def __init__(self,name,specialization,max_per_day=8):
        self.name=name
        self.specialization=specialization
        self.is_available = True
        self.max_per_day=max_per_day
        self.__schedule={}
    
    def book_slot(self,patient_name,appt_date,time_slot):
        if not self.is_available:
            raise DoctorUnavailableError( f"Dr. {self.name} is currently unavailable.")
        day_appointments=self.__schedule.get(appt_date,[])
        if len(day_appointments)>=self.max_per_day:
            raise PatientLimitExceededError(f"Dr. {self.name} already has "
                f"{self.max_per_day} appointments on "
                f"{appt_date}.")
        for existing in day_appointments:
            if existing.time==time_slot:
                raise SlotConflictError(existing)
        appt=Appointment(patient_name,self.name,appt_date,time_slot)
        day_appointments.append(appt)
        self.__schedule[appt_date]=day_appointments
        return appt
    
    def get_schedule(self,appt_date):
        return self.__schedule.get(appt_date,[])

def parse_time_slot(raw_time):
        try:
            parsed = datetime.strptime(raw_time, "%I:%M %p")
        except ValueError as original_error:
            raise InvalidTimeSlotError(
            f"'{raw_time}' is not a valid time. "
            f"Use 'HH:MM AM/PM'.") from original_error
        return parsed.strftime("%I:%M %p")

def parse_appointment_date(raw_date):
    try:
        parsed = datetime.strptime(raw_date, "%d-%m-%Y").date()
    except ValueError as original_error:
        raise InvalidTimeSlotError(
            f"'{raw_date}' is not a valid date. "
            f"Use 'DD-MM-YYYY'."
        ) from original_error
    if parsed<date.today():
        raise PastDateError(
            f"'{raw_date}' is in the past.")
    return parsed

class Hospital:
    def __init__(self,name):
        self.name=name
        self.__doctors={}
    
    def add_doctor(self,doctor: Doctor):
        self.__doctors[doctor.name]=doctor
        print(f"  [ADDED] Dr. {doctor.name} "
              f"({doctor.specialization})")
        
    
    def book_appointment(self,patient_name,doctor : Doctor,raw_date,raw_time):
        try:
            appt_date=parse_appointment_date(raw_date)
            time_slot=parse_time_slot(raw_time)
            appt=doctor.book_slot(patient_name,appt_date,time_slot)
        except DoctorUnavailableError as e:
            print(f"  [ERR] {e}")
            return None
        except PastDateError as e:
            print(f"  [ERR] {e}")
            return None
        except InvalidTimeSlotError as e:
            print(f"  [ERR] {e}")
            if e.__cause__:
                print(f"        (caused by: "
                      f"{e.__cause__.__class__.__name__}"
                      f": {e.__cause__})")
            return None
        except PatientLimitExceededError as e:
            print(f"  [ERR] {e}")
            return None
        except SlotConflictError as e:
            print(f"  [CONFLICT] {patient_name} wants "
                  f"{raw_time} on {raw_date}, but that "
                  f"slot belongs to "
                  f"{e.appointment.patient_name}.")
            print(f"  [SUGGESTION] Try a different "
                  f"time slot.")
            return None
        else:
            print(f"  [BOOKED] {appt}")
            return appt
        finally:
            print(f"  [LOG] Booking attempt: "
                  f"{patient_name} → Dr. {doctor.name}")
    
    def doctor_schedule(self,doctor :  Doctor,raw_date):
        try:
            appt_date = parse_appointment_date(raw_date)
        except AppointmentError as e:
            print(f"  [ERR] {e}")
            return
        appointments =doctor.get_schedule(appt_date)
        print(f"\n  Schedule — Dr. {doctor.name} "
              f"on {appt_date}")
        if not appointments:
            print(f"  No appointments booked.")
            return
        for a in appointments:
            print(f"  {a.time}  {a.patient_name}")

hospital = Hospital("Apollo Hospitals")
doc1=Doctor("Arjun Rao", "Cardiology", max_per_day=3)
doct2=Doctor("Priya Sharma", "General Medicine")
hospital.add_doctor(doc1)
hospital.add_doctor(doct2)
hospital.book_appointment("Ravi Kumar", doc1,"25-12-2026", "10:30 AM")
hospital.book_appointment("Sneha Reddy", doct2,"25-12-2026", "10:30 AM")

hospital.book_appointment("Meena Iyer", doc1,"25-12-2026", "10:30 AM")

hospital.book_appointment("Vikram Singh", doc1,
                          "25-12-2026", "10:30 PM")

hospital.doctor_schedule(doc1, "25-12-2026")