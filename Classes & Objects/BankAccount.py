#07-04-2026
#Bank Account Creation
import random
class BankAccount:
    bank_name = "ABC Bank Ltd"
    branch_name = "Main Branch"
    total_accounts = 0
    def __init__(self,name,phone,acc_type):
        self.acc_no = str(random.randint(1111111111,9999999999))
        self.name = name
        self.phone = phone
        self.acc_type = acc_type
        self.balance = 0
        self.transactions = []
        BankAccount.total_accounts += 1
    
    def __str__(self):
        return f"""Bank Account Details:
Bank Name: {BankAccount.bank_name}
Branch Name: {BankAccount.branch_name}
Account No: {self.acc_no}
Name: {self.name}
Phone: {self.phone}
Account Type: {self.acc_type}
Balance: {self.balance}"""

    def deposit(self,amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(
                {"type": "deposit", "amount": amount,"balance": self.balance})
            print(f"Deposited {amount}. New Balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")
    
    def withdraw(self,amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.transactions.append(
                    {"type": "withdrawal", "amount": amount,"balance": self.balance}
                )
                print(f"Withdrew {amount}. New Balance: {self.balance}")
            else:
                print("Insufficient balance for withdrawal.")
        else:
            print("Withdrawal amount must be positive.")
    
    def check_balance(self):
        print(f"Current Balance: {self.balance}")
    
    def display_transactions(self):
        print("Transaction History:")
        for txn in self.transactions:
            print(f"Type : {txn['type']} Amount : {txn['amount']} Balance : {txn['balance']}")

pradeep=BankAccount("Pradeep Kumar","9876543210","SA")
print(pradeep)
pradeep.deposit(10000)
pradeep.withdraw(2500)
pradeep.check_balance()
pradeep.display_transactions()