#02-07-2026
#Banking Transaction Processor with Fraud Check
from datetime import datetime
import random
import uuid
class Transaction:
    def __init__(self,type,amount,location="Local",sender=None,receiver=None):
        self.transaction_id = str(uuid.uuid4())
        self.type = type
        self.amount = amount
        self.location = location
        self.sender = sender
        self.receiver = receiver
        self.timestamp = datetime.now()
        self.status="Pending"
    
    def complete_transaction(self):
        self.status="Completed"
    
    def flag_transaction(self):
        self.status="Flagged for Review"
    
    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, Type: {self.type}, Amount: {self.amount}, Location: {self.location}, Status: {self.status}, Timestamp: {self.timestamp}"

class BankAccount:
    bank_name = "Python Secure Trust"
    total_bank_reserves = 10000000.00
    total_flagged_accounts = 0
    def __init__(self,name,account_tier="Standard"):
        self.__account_number = self.__generate_account_number()
        self.name = name
        self.__balance = 0.0
        self._account_tier = account_tier
        self.__transaction_history = []
        self.__pin = None
        self.is_flagged = False
        self.__status="Inactive"
        self.__is_locked = False
        self.__failed_pin_attempts = 0
        self.__created_at = datetime.now()
    
    def __generate_account_number(self):
        return str(random.randint(1000000000, 9999999999))
    
    def activate_account_set_pin(self, pin):
        if not self.__validate_pin(pin):
            raise ValueError("PIN must be a string of 4 to 6 digits.")
        if self.__status == "Active":
            raise Exception("Account is already active.")
        if self.__is_locked:
            raise Exception("Account is locked. Cannot activate.")
        self.__pin = pin
        self.__status = "Active"
        print(f"Account {self.__account_number} activated successfully.")
    
    def __verify_pin(self, pin):
        if self.__is_locked:
            print("Account is locked. Cannot verify PIN.")
            return False
        if self.__status != "Active":
            print("Account is not active. Cannot verify PIN.")
            return False
        if self.__pin == pin:
            return True
        else:
            self.__failed_pin_attempts += 1
            if self.__failed_pin_attempts>=3:
                self.__is_locked = True
                print("Account is locked due to multiple failed PIN attempts.")
                return False
            return False

    @staticmethod
    def __validate_pin(pin):
        return isinstance(pin, str) and 4<=len(pin) <= 6 and pin.isdigit() 
    
    def __run_fraud_checks(self,new_transaction):
        recent_transactions = 0
        current_time=datetime.now()

        for t in reversed(self.__transaction_history):
            time_diff=(current_time-t.timestamp).total_seconds()
            if time_diff<60:
                recent_transactions+=1
            else:
                break
        if recent_transactions>=3:
            return False
        if len(self.__transaction_history)>=3:
            total_amounts=sum(t.amount for t in self.__transaction_history)
            average=total_amounts/len(self.__transaction_history)
            if new_transaction.amount > (average * 10) and new_transaction.amount > 1000:
                return False
        
        if len(self.__transaction_history)>0:
            last_location = self.__transaction_history[-1].location
            # If location changes instantly to a high-risk area
            if last_location != new_transaction.location and new_transaction.location == "High-Risk-IP":
                return False # Fraud flagged: Location anomaly
        return True
    
    def deposit(self,amount,location="Local Branch"):
        if self.__is_locked:
            return "Account is locked. Please contact support."
        if self.__status!="Active":
            return "Account is Not Active"
        if amount<=0:
            return "Deposit amount must be positive."
        new_transaction=Transaction('Credit',amount,location,None,self)
        self.__balance+=amount
        new_transaction.complete_transaction
        self.__transaction_history.append(new_transaction)
        return f"Successfully deposited ${amount:.2f}. New Balance: ${self.__balance:.2f}"
    
    def withdraw(self,amount,pin,location="ATM"):
        if self.__is_locked:
            return "Account is locked. Please contact support."
        if self.__status!="Active":
            return "Account is Not Active"
        if amount<=0:
            return "Deposit amount must be positive."
        if not self.__validate_pin(pin):
            return "Invaild Pin"
        if not self.__verify_pin(pin):
            return "Incorrect Pin"
        if amount>self.__balance:
            return "Insufficient funds."
        new_transaction=Transaction('Debit',amount,location,self,None)
        # Check global static rules first
        if not self.is_standard_business_hours() and amount > 5000:
             new_transaction.flag_transaction()
             self.__transaction_history.append(new_transaction)
             return "SYSTEM HALT: Large transfers outside business hours require manual review."

        # Run the internal private fraud engine
        is_safe = self.__run_fraud_checks(new_transaction)
        
        if not is_safe:
            self.__is_locked = True
            new_transaction.flag_transaction()
            self.__transaction_history.append(new_transaction)
            BankAccount.total_flagged_accounts += 1
            return f"FRAUD ALERT: Suspicious activity detected. Account {self.__account_number} is now LOCKED."

        # If we made it here, the transaction is legitimate
        self.__balance -= amount
        BankAccount.total_bank_reserves -= amount
        new_transaction.complete_transaction()
        self.__transaction_history.append(new_transaction)
        
        return f"Successfully withdrew ${amount:.2f}. Remaining Balance: ${self.__balance:.2f}"
    
    def get_balance(self,pin):
        if not self.__validate_pin(pin):
            return "Invaild Pin"
        if not self.__verify_pin(pin):
            return "Incorrect Pin"
        return f"Current Balance: ${self.__balance:.2f}"
    
    def print_statement(self,pin):
        if not self.__validate_pin(pin):
            return "Invaild Pin"
        if not self.__verify_pin(pin):
            return "Incorrect Pin"
        if not self.__transaction_history:
            return "No Transaction Found"
        for t in self.__transaction_history:
            print(t)
        print(f"Total Available Balance: ${self.__balance:.2f}\n" + "-"*50)
        return "Statement printed successfully."
    
    @classmethod
    def create_from_string(cls,data):
        name, tier = data.split(',')
        # Return a new instance of the class
        return cls(name, tier)
    
    @classmethod
    def get_bank_info(cls):
        """Accesses class variables."""
        return f"{cls.bank_name} has ${cls.total_bank_reserves:.2f} in reserves and {cls.total_flagged_accounts} locked accounts."

    # ==========================================
    # TOPIC: Static Methods
    # Uses the @staticmethod decorator.
    # Belongs to the class but doesn't need 'self' or 'cls'. 
    # Used for utility functions related to the domain.
    # ==========================================
    @staticmethod
    def is_standard_business_hours():
        """Checks if current time is within normal banking hours (9 AM to 5 PM)."""
        current_hour = datetime.datetime.now().hour
        # Returns True if between 9 AM and 5 PM
        return 9 <= current_hour < 17

if __name__ == "__main__":
    print(BankAccount.get_bank_info())
    print("\n" + "="*50)
    
    # 1. Create accounts using standard initialization and Class Method
    account1 = BankAccount("Alice Smith")
    account2 = BankAccount.create_from_string("Bob Jones,Premium")
    account1.activate_account_set_pin("901836")
    account2.activate_account_set_pin("901836")

    print(account1.deposit(500))
    print(account1.get_balance("901836")) # Wrong PIN, should fail
    print(account2.get_balance("901836"))

    print("\n--- Testing Security Lockout ---")
    print(account2.withdraw(50, "901836")) # Attempt 1
    print(account2.withdraw(50, "901836")) # Attempt 2
    print(account2.withdraw(50, "901836")) # Attempt 3 (Locks account)
    print(account2.withdraw(50, "901836")) # Correct PIN, but account is already locked
    
    # 4. Testing the Fraud Engine: Volume Check
    print("\n--- Testing Fraud: Volume Anomaly ---")
    account3 = BankAccount("Charlie")
    account3.activate_account_set_pin("901836")
    # Establish a pattern of small transactions
    account3.withdraw(10, "901836")
    account3.withdraw(15, "901836")
    account3.withdraw(12, "901836")
    # Suddenly try to withdraw a massive amount (10x average)
    print(account3.withdraw(15000, "901836")) 
    
    # 5. Testing the Fraud Engine: Velocity Check (Fast transactions)
    print("\n--- Testing Fraud: Velocity Anomaly ---")
    account4 = BankAccount("Diana")
    account4.activate_account_set_pin("901836")
    print(account4.withdraw(100, "901836"))
    print(account4.withdraw(100, "901836"))
    print(account4.withdraw(100, "901836")) # 3rd transaction in less than 60 seconds
    
    # 6. Testing the Fraud Engine: Location Anomaly
    print("\n--- Testing Fraud: Location Anomaly ---")
    account5 = BankAccount("Eve")
    account5.activate_account_set_pin("901836")
    account5.withdraw(100, "0000", location="New York ATM")
    # Immediate transaction from a flagged high-risk location
    print(account5.withdraw(100, "901836", location="High-Risk-IP"))
    
    # 7. Print Final Statement to see all private transaction logs
    account1.print_statement("901836")
    
    # 8. Check global class variables to see impact
    print("\n" + "="*50)
    print("END OF DAY BANK REPORT:")
    print(BankAccount.get_bank_info())