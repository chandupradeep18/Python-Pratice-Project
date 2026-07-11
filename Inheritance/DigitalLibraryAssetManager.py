#04-07-2026
#Digital Library Asset Manager
from datetime import datetime,date,timedelta
import uuid
import random
class DigitalAsset:
    total_assets_in_network=0
    def __init__(self,title:str,author:str):
        title=title.upper().strip()
        author=author.upper().strip()
        self._asset_id=str(uuid.uuid4())[:8]
        self._title=title
        self._author=author
        self.__is_available=True
        self.__borrow_count=0
        DigitalAsset.total_assets_in_network+=1
    
    @property
    def available(self):
        return self.__is_available
    
    @property
    def borrow_count(self):
        return self.__borrow_count
    
    def get_details(self):
        status = "Available" if self.__is_available else "Checked Out"
        return f"[{self._asset_id}] {self._title} by {self._author} - {status}"
    
    def mark_as_borrowed(self):
        if not self.__is_available:
            return False
        self.__is_available=False
        self.__borrow_count+=1
        return True
    
    def mark_as_returned(self):
        if self.available:
            print('Not Borrowed') 
        else:
            self.__is_available=True
            print('Returned')

class EBook(DigitalAsset):
    def __init__(self, title:str, author:str,file_size_mb:float,format_type:str):
        format_type=format_type.lower()
        format_types=['.pdf','.html','.epub','.docx','.md','.odt','rtf','.txt']
        if format_type not in format_types:
            raise ValueError('Enter Valid File Format')
        super().__init__(title, author)
        self.file_size_mb=file_size_mb
        self.format_type=format_type
    
    def get_details(self):
        base_details=super().get_details()
        return f"{base_details} | E-Book ({self.file_size_mb}MB, {self.format_type})"

class AudioBook(DigitalAsset):
    def __init__(self, title, author,duration:float,narrator:str):
        narrator=narrator.lower()
        if duration<=0:
            raise ValueError('Duration is Not Valid')
        super().__init__(title, author)
        self.duration=duration
        self.narrator=narrator
    
    def get_details(self):
        base_details = super().get_details()
        return f"{base_details} | AudioBook ({self.duration} mins, Narrated by {self.narrator})"

class ResearchPaper(DigitalAsset):
    def __init__(self, title, author,university:str,is_restricted:bool=True):
        super().__init__(title, author)
        self.university=university.lower()
        self._is_restricted=is_restricted
    
    @property
    def is_restricted(self):
        return self._is_restricted

    def get_details(self):
        base_details = super().get_details()
        restriction="RESTRICTED" if self.is_restricted else "OPEN"
        return f"{base_details} | Paper ({self.university}) - [{restriction}]"

class LibraryUser:
    standard_borrow_days=10
    def __init__(self,name:str,email:str):
        name=name.lower()
        email=email.lower()
        if not self.__validate_email(email):
            raise ValueError('Email not Validly')
        self._user_id=str(random.randint(1111,9999))
        self._name=name
        self._email=email
        self._borrowed_items=[]
        self._max_borrows=1

    @staticmethod
    def __validate_email(email:str):
        if '@' in email and '.' in email:
            vaild_email=['gmail.com','outlook.com']
            mail=email.split('@')
            if  mail[1] in vaild_email:
                return True
        return False
    
    @classmethod
    def get_library_policy(cls):
        return f"Standard borrowing period is {cls.standard_borrow_days} days. Late fees apply."
    
    def can_borrow(self):
        return len(self._borrowed_items)<self._max_borrows
    
    def add_to_borrowed(self,asset_id):
        if asset_id not in self._borrowed_items:
            self._borrowed_items.append(asset_id)
            print('Asset Added to Borrowed Assets')
        else:
            print('The Asset Already Borrowed By User')
    
    def remove_from_borrowed(self,asset_id):
        if asset_id in self._borrowed_items:
            self._borrowed_items.remove(asset_id)
            print('Asset Returned')
        else:
            print('No asset Found')
    
    def get_user_type(self):
        return "Generic User"

class Student(LibraryUser):
    def __init__(self, name, email,grade_level):
        super().__init__(name, email)
        self.grade_level=grade_level
        self._max_borrows=3
    
    def get_user_type(self):
        return "Student"

class Teacher(LibraryUser):
    def __init__(self, name, email,department):
        super().__init__(name, email)
        self.department=department
        self._max_borrows=6
    
    def get_user_type(self):
        return "Teacher"

class Transaction:
    def __init__(self,user:LibraryUser,asset:DigitalAsset):
        self.user_id=user._user_id
        self.asset_id=asset._asset_id
        self.borrow_date=date.today()
        self.due_date=self.borrow_date+timedelta(days=user.standard_borrow_days)
        self.return_date=None
        self.late_fee=0.0
    
    def close_transaction(self,return_date_override=None):
        self.return_date=return_date_override or date.today()
        if self.return_date>self.due_date:
            day_late=(self.return_date-self.due_date).days
            self.late_fee=day_late*1.50
        return self.late_fee

class LibraryManager:
    def __init__(self):
        self.assets={}
        self.users={}
        self.active_transaction={}
    
    def add_asset(self,asset:DigitalAsset):
        if asset._asset_id in self.assets:
            print('Asset Already Exist')
        else:
            self.assets[asset._asset_id]=asset
            print('Asset Added to Libray')
    
    def register_user(self,user:LibraryUser):
        if user._user_id in self.users:
            print('User Already Exist')
        else:
            self.users[user._user_id]=user
            print('User Added to Libray')

    def proccess_borrowing(self,user_id:str,asset_id:str):
        if user_id not in self.users:
            print("Error: Invalid User ID ")
            return False
        user=self.users[user_id]
        if asset_id not in self.assets:
            print("Error: Invalid Asset ID ")
            return False
        asset=self.assets[asset_id]
        if not user.can_borrow():
            print(f"Error: {user._name} has reached their borrowing limit of {user._max_borrows}.")
            return False
        if not asset.available:
            print(f"Error: Asset '{asset._title}' is currently checked out.")
            return False
        if isinstance(asset,ResearchPaper) and asset.is_restricted:
            if not isinstance(user,Teacher):
                print(f"Error: '{asset._title}' is restricted. Only Teachers can borrow this asset.")
                return False
        asset.mark_as_borrowed()
        user.add_to_borrowed(asset_id)
        new_transaction=Transaction(user,asset)
        self.active_transaction[asset_id] = new_transaction
        print(f"Success! '{asset._title}' borrowed by {user._name}. Due on: {new_transaction.due_date}")
        return True
    
    def process_return(self,asset_id,simulated_return_date=None):
        if asset_id not in self.active_transaction:
            print("Error: No active transaction found for this asset.")
            return False
        transaction:Transaction
        transaction=self.active_transaction[asset_id]
        user=self.users[transaction.user_id]
        asset=self.assets[asset_id]

        fee=transaction.close_transaction(simulated_return_date)
        asset.mark_as_returned()
        user.remove_from_borrowed(asset_id)

        del self.active_transaction[asset_id]
        print(f"Success! '{asset._title}' returned by {user._name}.")
        if fee > 0:
            print(f"WARNING: Item was returned late. Outstanding Fee: ${fee:.2f}")
        return True
    
    def show_inventory(self):
        print("\n=== Library Digital Inventory ===")
        for asset in self.assets.values():
            print(asset.get_details())
        print(f"Total Assets in Network: {DigitalAsset.total_assets_in_network}")

if __name__ == "__main__":
    # Initialize the Manager
    library = LibraryManager()

    # Print Class Method Policy
    print(LibraryUser.get_library_policy())

    # Create some Assets
    book1 = EBook("Learn Python", "Guido", 5.2, ".PDF")
    audio1 = AudioBook("Clean Code", "Uncle Bob", 450, "John Doe")
    paper1 = ResearchPaper("Advanced AI Models", "Dr. Smith", "MIT", is_restricted=True)

    # Add to Library
    library.add_asset(book1)
    library.add_asset(audio1)
    library.add_asset(paper1)

    # Create Users
    student1 = Student( "Alice", "alice@gmail.com", "Sophomore")
    teacher1 = Teacher( "Prof. Bob", "bob@gmail.com", "Computer Science")

    # Register Users
    library.register_user(student1)
    library.register_user(teacher1)

    # Show initial inventory
    library.show_inventory()

    # --- Test Business Logic Scenarios ---
    
    # Scenario 1: Normal borrow
    library.proccess_borrowing(student1._user_id, book1._asset_id)

    # Scenario 2: Trying to borrow an unavailable item
    library.proccess_borrowing(teacher1._user_id, book1._asset_id)

    # Scenario 3: Student trying to borrow a restricted item (Should Fail)
    library.proccess_borrowing(student1._user_id, paper1._asset_id)

    # Scenario 4: Teacher borrowing a restricted item (Should Succeed)
    library.proccess_borrowing(teacher1._user_id, paper1._asset_id)

    # Scenario 5: Returning an item Late (Simulating a return 20 days later)
    late_date = date.today() + timedelta(days=20)
    library.process_return(book1._asset_id, simulated_return_date=late_date)

    # Show final inventory
    library.show_inventory()
        
