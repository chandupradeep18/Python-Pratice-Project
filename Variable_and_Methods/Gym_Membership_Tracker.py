#29-06-2026
#Gym Membership Tracker
from datetime import datetime
class MembershipPlan:
    def __init__(self,name,monthly_fee,includes_classes,cancellation_fee): #bdfbngnbfgn
        self.name=name
        self.monthly_fee=monthly_fee
        self.includes_classes=includes_classes
        self.cancellation_fee=cancellation_fee
        print(f'New Gym Member Plan {name} Has Be Created')
    
    def __str__(self):
        return f"""MemberShip Plan Details
Name : {self.name}
Monthly Fee : {self.monthly_fee}
includes_classes : {self.includes_classes}
cancellation_fee : {self.cancellation_fee}"""
BASIC_PLAN = MembershipPlan("Basic", 30.00, False, 15.00)
PREMIUM_PLAN = MembershipPlan("Premium", 60.00, True, 25.00)
VIP_PLAN = MembershipPlan("VIP", 100.00, True, 0.00)

class Member:
    id_sequence=1000
    total_active_members=0
    def __init__(self,first_name,last_name,plan):
        self.first_name=first_name
        self.last_name=last_name
        self.member_id=f"GYM-{Member.id_sequence}"
        Member.id_sequence+=1
        self.plan=plan
        self.status='Active'
        self.account_balance=0.0
        self.total_visits=0
        self.visit_history=[]
        self.payment_history=[]
        Member.total_active_members += 1

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class GymManager:
    tax_rate=0.08
    late_fee=15.00
    global_revenue=0.0
    def __init__(self,gym_name):
        self.gym_name=gym_name
        self.members={}
    
    def register_member(self,first_name,last_name,plan):
        new_member=Member(first_name,last_name,plan)
        self.members[new_member.member_id]=new_member
        initial_charge=plan.monthly_fee+(plan.monthly_fee*GymManager.tax_rate)
        new_member.account_balance+=initial_charge
        return new_member.member_id
    
    def check_in(self,member_id,date_string,wants_class=False):
        if member_id not in self.members:
            print("Error: Member ID not found.")
            return False
        member=self.members[member_id]
        if member.status=="Frozen":
            print(f"Access Denied: Account {member_id} is currently frozen.")
            return False
        if member.status=="Canceled":
            print(f"Access Denied: Account {member_id} is canceled.")
            return False
        if member.account_balance>100.00:
            print(f"Access Denied: Outstanding balance (${member.account_balance:.2f}) exceeds limit")
            return False
        if wants_class and not member.plan.includes_classes:
            print(f"Access Denied: The {member.plan.name} plan does not include group classes.")
            return False
        member.total_visits+=1
        member.visit_history.append(date_string)
        print(f"Welcome, {member.get_full_name()}! Enjoy your workout.")
        return True
    
    def process_monthly_billing(self):
        total_billed_this_month = 0.0
        for member in self.members.values():
            if member.status == "Canceled":
                continue
            if member.status=="Frozen":
                charge = 5.00
            else:
                charge=member.plan.monthly_fee + (member.plan.monthly_fee * GymManager.tax_rate)
            if member.account_balance>0:
                member.account_balance += GymManager.late_fee
                charge += GymManager.late_fee
            member.account_balance+=charge
            total_billed_this_month += charge
        return total_billed_this_month
    
    def process_payment(self,member_id, amount):
        if member_id in self.members:
            member = self.members[member_id]
            if amount<=0:
                print("Payment must be greater than zero.")
                return False
            member.account_balance-=amount
            GymManager.global_revenue += amount
            member.payment_history.append({'Date':datetime.now(),'Paid Amount':amount,'Balance':member.account_balance})
            print(f"Payment of ${amount:.2f} processed for {member.get_full_name()}.")
            return True
        else:
            print("Member not found.")
            return False
    
    def freeze_account(self,member_id):
        if member_id in self.members:
            member = self.members[member_id]
            if member.status=="Active":
                member.status="Frozen"
                print("Account successfully frozen.")
                return True
            else:
                print(f"Account is already {member.status}.")
                return False
        else:
            print("Member not found.")
            return False
    
    def upgrade_plan(self,member_id,new_plan):
        if member_id in self.members:
            member = self.members[member_id]
            if member.status!="Active":
                print("Cannot upgrade a non-active account.")
                return False
            if member.plan.monthly_fee >=new_plan.monthly_fee:
                print("New plan must be a higher tier to upgrade.")
                return False
            upgrade_fee=new_plan.monthly_fee-member.plan.monthly_fee
            member.account_balance+=upgrade_fee
            member.plan=new_plan
            print(f"Upgraded to {new_plan.name} plan. Upgrade fee of ${upgrade_fee:.2f} applied.")
            return True
        else:
            print("Member not found.")
            return False
    
    def cancel_membership(self,member_id):
        if member_id in self.members:
            member = self.members[member_id]
            if member.status=='Canceled':
                print("Account is already canceled.")
                return False
            if member.plan.cancellation_fee>0:
                member.account_balance+=member.plan.cancellation_fee
            member.status = "Canceled"
            Member.total_active_members -= 1
            print(f"Account canceled. Final balance owed: ${member.account_balance}")
            return True
        else:
            print("Member not found.")
            return False
    
    def generate_management_report(self):
        report = {
            "Total Members in System": len(self.members),
            "Active/Frozen Members": Member.total_active_members,
            "Total Gym Revenue": GymManager.global_revenue,
            "Members with Outstanding Balances": sum(1 for m in self.members_db.values() if m.account_balance > 0)
        }
        return report

# 1. Initialize Gym
iron_forge_gym = GymManager("Iron Forge Fitness")

# 2. Register Members
id_1 = iron_forge_gym.register_member("Alice", "Smith", BASIC_PLAN)
id_2 = iron_forge_gym.register_member("Bob", "Jones", PREMIUM_PLAN)
id_3 = iron_forge_gym.register_member("Charlie", "Brown", VIP_PLAN)

total=iron_forge_gym.process_monthly_billing()
print(total)

iron_forge_gym.process_payment(id_2, 100.00)
iron_forge_gym.check_in(id_2, "2023-10-25", wants_class=True)
iron_forge_gym.check_in(id_1, "2023-10-25", wants_class=False)

# 7. Freeze an account
iron_forge_gym.freeze_account(id_3)

# 8. Cancel a membership (Alice will be charged the $15 cancellation fee)
iron_forge_gym.cancel_membership(id_1)
