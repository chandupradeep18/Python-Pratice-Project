#06-07-2026
#Cloud Storage Provider API Simulator
import time
from datetime import datetime
import uuid
import random
from abc import ABC,abstractmethod

class CloudFile:
    allowed_extensions = ['.txt', '.pdf', '.png', '.jpg', '.csv', '.json','.docx']
    def __init__(self,filename,size_mb):
        if not self.validate_extension(filename):
            raise ValueError('Invalid File Extension')
        self.filename=filename
        self.size_mb=size_mb
        self.file_id=self._generate_file_id()
        self._is_encrypted=False
        self.upload_date=None
    
    @staticmethod
    def validate_extension(filename:str):
        return any(filename.endswith(ext) for ext in CloudFile.allowed_extensions)
    
    def _generate_file_id(self):
        return f"{uuid.uuid4().hex[:8].upper()}"
    
    def __str__(self):
        return f"'{self.filename}' ({self.size_mb} MB) [ID: {self.file_id}]"

class UserAccount:
    total_active_users=0
    def __init__(self,username,storage_limit_mb):
        self.username=username
        self._storage_limit_mb=storage_limit_mb
        self._used_storage=0.0
        self.__api_key=self._generate_api_key()
        self.owned_files=[]
        UserAccount.total_active_users+=1
    
    def _generate_api_key(self):
        return f"AKIA-{uuid.uuid4().hex.upper()}"
    
    @property
    def get_api_key(self):
        return self.__api_key
    
    def has_sufficient_space(self,file_size):
        return (self._used_storage+file_size)<=self._storage_limit_mb
    
    def consume_quota(self,file_size):
        self._used_storage+=file_size
    
    def free_quote(self,file_size):
        self._used_storage-=file_size
    
    def display_quota(self):
        print(f"[{self.username} Quota] Used: {self._used_storage:.2f} MB / {self._storage_limit_mb} MB")
    
    @classmethod
    def get_active_user_count(cls):
        return f"System currently has {cls.total_active_users} active users."

class CloudProvider(ABC):
    def __init__(self,region):
        self.region=region
        self._server_status="Online"
    
    @abstractmethod
    def upload_file(self,user:UserAccount,file_obj:CloudFile):
        pass

    @abstractmethod
    def download_file(self,user:UserAccount,file_id:str):
        pass

    @abstractmethod
    def delete_file(self,user:UserAccount,file_id:str):
        pass

    def ping_server(self):
        print(f"Pinging {self.region} server... Status: {self._server_status}")

class StandardStorage(CloudProvider):
    def __init__(self, region="US-EAST-1"):
        super().__init__(region)
        self.storage_bucket={}
    
    def upload_file(self, user: UserAccount, file_obj: CloudFile):
        if not CloudFile.validate_extension(file_obj.filename):
            print(f'Invalid File Extension Allowed Only {CloudFile.allowed_extensions}')
            return False
        if not user.has_sufficient_space(file_obj.size_mb):
            print(f"ERROR: Insufficient quota for {user.username}. Need {file_obj.size_mb} MB.")
            return False
        print("Uploading data blocks")
        time.sleep(0.5)
        file_obj._is_encrypted=True
        file_obj.upload_date=datetime.now()
        user.consume_quota(file_obj.size_mb)
        user.owned_files.append(file_obj)
        self.storage_bucket[file_obj.file_id]=file_obj
    
    def download_file(self, user: UserAccount, file_id: str):
        if file_id in self.storage_bucket:
            file=self.storage_bucket[file_id]
            print(f"Decrypting and downloading '{file.filename}'... (Fast speed)")
            time.sleep(0.3)
            print("SUCCESS: Download complete.")
            return file
        print("ERROR: File not found on server.")
        return None
    
    def delete_file(self, user: UserAccount, file_id: str):
        if file_id in self.storage_bucket:
            file:CloudFile=None
            file=self.storage_bucket.pop(file_id)
            user.free_quote(file.size_mb)
            user.owned_files.remove(file)
            print(f"DELETED: '{file.filename}' removed. Quota restored.")
        else:
            print("ERROR: File not found.")

class ArchiveStorage(CloudProvider):
    def __init__(self, region="EU-West-2"):
        super().__init__(region)
        self.cold_vault={}
        self.compression_rate=0.5
    
    def upload_file(self, user: UserAccount, file_obj: CloudFile):
        if not CloudFile.validate_extension(file_obj.filename):
            print(f'Invalid File Extension Allowed Only {CloudFile.allowed_extensions}')
            return False
        com_rate=file_obj.size_mb*self.compression_rate
        if not user.has_sufficient_space(com_rate):
            print(f"ERROR: Insufficient quota for {user.username}. Need {file_obj.com_rate} MB.")
            return False
        print("Compressing data...")
        time.sleep(1.0)
        print("Moving to deep archive storage...")
        time.sleep(1.5)
        file_obj._is_encrypted=True
        file_obj.size_mb=com_rate
        file_obj.upload_date=datetime.now()
        user.consume_quota(com_rate)
        user.owned_files.append(file_obj)
        self.cold_vault[file_obj.file_id]=file_obj
        print(f"SUCCESS: '{file_obj.filename}' archived in {self.region}. (Compressed to {com_rate} MB)")
        return True

    def download_file(self, user: UserAccount, file_id: str):
        if file_id in self.cold_vault:
            file=self.cold_vault[file_id]
            print(f"Waking up cold servers... this will take a moment.")
            time.sleep(1.0)
            print(f"Decompressing '{file.filename}'...")
            time.sleep(1.0)
            print("SUCCESS: Download complete.")
            return file
        print("ERROR: File not found in archive.")
        return None        

    def delete_file(self, user: UserAccount, file_id: str):
        if file_id in self.cold_vault:
            file=self.cold_vault.pop(file_id)
            user.free_quote(file.size_mb)
            user.owned_files.remove(file)
            print(f"DELETED: '{file.filename}' wiped from deep archive.")
        else:
            print("ERROR: File not found.")

if __name__ == "__main__":
    print("=== CLOUD STORAGE SIMULATOR STARTING ===")
    
    # Check Class Method
    print(UserAccount.get_active_user_count())
    
    # 1. Create a user with 50 MB of quota
    user1 = UserAccount("DataAnalyst_99", storage_limit_mb=50)
    print(f"User created. Secure API Key: {user1.get_api_key}")
    
    # 2. Initialize our abstracted storage providers
    standard_api = StandardStorage()
    archive_api = ArchiveStorage()
    
    standard_api.ping_server()

    # 3. Create some files (Objects)
    file_doc = CloudFile("quarterly_report.pdf", 15.0)
    file_img = CloudFile("vacation_photo.png", 20.0)
    file_data = CloudFile("dataset.csv", 40.0) # Too big for standard if doc and img are uploaded!
    #file_bad = CloudFile("virus.exe", 5.0) # Invalid extension
    
    # 4. Perform Business Logic Operations
    standard_api.upload_file(user1, file_doc)
    #standard_api.upload_file(user1, file_bad) # Will fail gracefully
    
    user1.display_quota()
    
    # Try uploading 40MB file to standard (Will fail, 15 + 40 = 55 > 50)
    standard_api.upload_file(user1, file_data) 
    
    # Let's upload the 40MB file to Archive instead. It compresses by 50% (becomes 20MB).
    # 15MB (Standard) + 20MB (Archive) = 35MB. This will succeed!
    archive_api.upload_file(user1, file_data)
    
    user1.display_quota()
    
    # 5. Download testing
    standard_api.download_file(user1, file_doc.file_id)
    archive_api.download_file(user1, file_data.file_id)
    
    # 6. Delete and free up space
    print("\n--- API: Clean Up ---")
    archive_api.delete_file(user1, file_data.file_id)
    user1.display_quota()

    print("\n=== CLOUD STORAGE SIMULATOR SHUTDOWN ===")