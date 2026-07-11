#23-06-2026
import random
from datetime import datetime
class BankError(Exception):
    pass
class InvalidAmountError(BankError):
    pass
class InsufficientFundsError(BankError):
    pass
class InsufficientMinFundsError(BankError):
    pass
class AccountFrozenError(BankError):
    pass
class InvalidPinError(BankError):
    pass
class AccountNotFoundError(BankError):
    pass
class AccountTypeNotFoundError(BankError):
    pass
class AccountActivationError(BankError):
    pass

class BankAccount:
    acc_type={'saving':1000,'current':5000}
    def __init__(self,name,account_type):
        account_type=account_type.lower().strip()
        if account_type not in self.acc_type.keys():
            raise AccountTypeNotFoundError('Select a Vaild Account Type')
        self.account_id='Acc'+str(random.randint(111111111,999999999))
        self.name=name
        self.account_type=account_type
        self._status='InActive'
        self.__balance=0.0
        self.__pin=None
        self.__transaction=[]
        self.__logs=[]
        self.__log_account_activite(f'Account Created with Account No : {self.account_id}')
    
    @property
    def balance(self):
        return self.__balance
    
    def __log_account_activite(self,message):
        self.__logs.append({'Time Stamp':datetime.now(),'Log':message})
    
    def show_account_activite(self):
        if not self.__logs:
            print('No Log Found')
            return
        for logs in self.__logs:
            print(logs)
    def __record_account_transaction(self,transaction):
        self.__transaction.append(transaction)
    def __verify_pin(self,pin):
        return pin==self.__pin
    
    def activate_account(self,pin):
        if not self.vaildate_pin(pin):
            self.__log_account_activite('Try to Activite Account With Invaild Pin')
            raise InvalidPinError('Pin Must be 6 Number')
        if self._status!='InActive' and self.__pin!=None:
            self.__log_account_activite('Account is Already Active')
            raise AccountActivationError('Account is Already Active')
        self._status='Active'
        self.__pin=pin
        self.__log_account_activite('Account Activated')
        print('Account Activated With Pin')
    
    def deposit(self,amount,sender=None):
        if self._status!='Active':
            self.__log_account_activite('Account is Not Active to make Deposit')
            raise AccountActivationError('Account is Not Active')
        if not self.vaildate_amount(amount):
            raise InvalidAmountError('Invaild Amount')
        self.__balance+=amount
        transaction={'Date':datetime.now(),'Type':'Credit','Recevier':self,'Sender':sender,'Amount':amount,'Balance':self.__balance}
        self.__record_account_transaction(transaction)
        print(f'{amount} Deposited Balance {self.__balance}')
    
    def withdraw(self,amount,pin,reciver=None):
        if self._status!='Active':
            self.__log_account_activite('Account is Not Active to make Withdraw')
            raise AccountActivationError('Account is Not Active')
        if not self.vaildate_amount(amount):
            raise InvalidAmountError('Invaild Amount')
        if not self.__verify_pin(pin):
            raise InvalidPinError('Invalid Pin Entered')
        if amount >self.__balance:
            raise InsufficientFundsError('Insufficient Balance')
        min_balance=self.acc_type.get(self.account_type)
        if not self.__balance-amount >=min_balance:
            raise InsufficientMinFundsError(f'Min Balance of {min_balance} is Required')
        self.__balance-=amount
        transaction={'Date':datetime.now(),'Type':'Debit','Recevier':reciver,'Sender':self,'Amount':amount,'Balance':self.__balance}
        self.__record_account_transaction(transaction)
        print(f'{amount} Withdrawed Balance {self.__balance}')
    
    def transfer(self,amount,pin,receiver):
        if self._status!='Active':
            raise AccountActivationError('Account is Not Active')
        if not isinstance(receiver,BankAccount):
            raise AccountNotFoundError('Invaild Receiver Account')
        if receiver._status!='Active':
            raise AccountActivationError('Receiver Account is Not Active')
        self.withdraw(amount,pin,receiver)
        self.deposit(amount,self)
        print(f'{amount} have been Transfed to {receiver.name} from {self.name}')

    @staticmethod
    def vaildate_pin(pin):
        return isinstance(pin,str) and pin.isdigit() and len(pin)==6
    @staticmethod
    def vaildate_amount(amount):
        return isinstance(amount,(int,float)) and amount >0

class Bank:
    def __init__(self, name):
        self.name        = name
        self.__accounts  = {}
    
    def open_account(self, owner, acc_type):
        try:
            account = BankAccount(owner,acc_type)
        except AccountTypeNotFoundError as e:
            print(f'Invaild Bank Account Type')
            return None
        else:
            self.__accounts[account.account_id] = account
            print(f"  [OPENED] {account.account_id} "
                  f"for {owner}")
            return account
        finally:
            print(f"  [LOG] Account opening attempt "
                  f"processed for {owner}.")
    
    def safe_deposit(self, account, amount):
        try:
            account.deposit(amount)
        except AccountActivationError as e:
            print(f"  [ERR] {e}")
            return False
        except (InvalidAmountError,
                AccountFrozenError) as e:
            print(f"  [ERR] Deposit failed: {e}")
            return False
        else:
            print(f"  [OK] New balance: "
                  f"₹{account.balance}")
            return True
    
    def safe_withdraw(self, account, amount, pin):
        try:
            new_balance = account.withdraw(amount, pin)
        except AccountActivationError as e:
            print(f"  [ERR] {e}")
            return False
        except InvalidAmountError as e:
            print(f"  [ERR] {e}")
            return False
        except InvalidPinError as e:
            print(f"  [ERR] Withdrawal blocked: {e}")
            return False
        except InsufficientFundsError as e:
            print(f"  [ERR] {e}")
            return False
        except InsufficientMinFundsError as e:
            print(f"  [ERR] {e}")
            return False
        except BankError as e:
            # Catches AccountFrozenError and any other
            # BankError subtype not explicitly handled above
            print(f"  [ERR] Banking error: {e}")
            return False
        else:
            print(f"  [OK] Withdrawn. New balance: "
                  f"₹{account.balance:,.2f}")
            return True
        finally:
            print(f"  [LOG] Withdrawal attempt "
                  f"logged for {account.account_id}.")
    
    def transfer(self, sender, recevier, amount, pin):
        try:
            sender.transfer(amount, pin,recevier)
        except AccountNotFoundError as e:
            print(f"  [ERR] {e}")
            return False
        except (InvalidPinError, InsufficientFundsError,
                InvalidAmountError,InvalidPinError,InsufficientMinFundsError) as e:
            print(f"  [ERR] Transfer failed: "
                  f"{e.__class__.__name__}: {e}")
            return False
        else:
            print(f"  [OK] ₹{amount:,.2f} transferred "
                  f"from {sender.name} to {recevier.name}")
            return True

bank = Bank("SBI Digital")
print("--- Opening Accounts ---")
acc1 = bank.open_account("Ravi Kumar",'saving')
acc2 = bank.open_account("Sneha Reddy",'current')
acc3 = bank.open_account("Bad User",'hi')
acc1.activate_account('901836')
acc2.activate_account('954216')

print("\n--- Deposits ---")
bank.safe_deposit(acc1, 2000)
bank.safe_deposit(acc1, -100)     # invalid
#bank.safe_deposit("ACC00000000", 500)  

print("\n--- Withdrawals ---")
bank.safe_withdraw(acc1, 300, "901836")  # ok
bank.safe_withdraw(acc1, 3000, "0000")  # wrong pin
bank.safe_withdraw(acc1, 50000, "1234") # insufficient
bank.safe_withdraw(acc1, -10, "1234")   # invalid amount
#bank.safe_withdraw("ACC99999999", 100, "1234") 

print("\n--- Transfer ---")
bank.transfer(acc1, acc2,
              1000, "901836")          # frozen receiver — sender still debited
bank.transfer(acc1, "ACC00000000",
              500, "1234")     