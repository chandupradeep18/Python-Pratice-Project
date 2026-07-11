#07-07-2026
#Employee Performance Bonus Evaluator
from abc import ABC,abstractmethod
from typing import List,Dict,Any
class Employee(ABC):
    COMPANY_NAME = "GlobalTech Solutions"
    MIN_PERFORMANCE_SCORE = 1.0
    MAX_PERFORMANCE_SCORE = 5.0
    GLOBAL_BONUS_MULTIPLIER = 1.0
    def __init__(self,employee_id: str, name: str, base_salary: float, performance_score: float):
        self.employee_id=employee_id
        self.name=name.upper().strip()
        if base_salary<=0:
            raise ValueError("Base salary must be a positive financial value.")
        self.__base_salary=base_salary
        self._performance_score=self.validate_score(performance_score)
    @property
    def base_salary(self)->float:
        return self.__base_salary
    @property
    def performance_score(self)->float:
        return self._performance_score
    @performance_score.setter
    def performance_score(self,new_score:float)->None:
        self._performance_score=self.validate_score(new_score)
    @staticmethod
    def validate_score(score:float)->float:
        if score < Employee.MIN_PERFORMANCE_SCORE:
            return Employee.MIN_PERFORMANCE_SCORE
        if score > Employee.MAX_PERFORMANCE_SCORE:
            return Employee.MAX_PERFORMANCE_SCORE
        return score
    @classmethod
    def adjust_global_bonus_multiplier(cls,new_multiplier:float)->None:
        if new_multiplier<0 or not isinstance(new_multiplier,(float,int)):
            raise ValueError("Global multiplier cannot be negative.")
        cls.GLOBAL_BONUS_MULTIPLIER=new_multiplier
    def _calculate_base_modifoer(self)->float:
        return (self._performance_score/Employee.MAX_PERFORMANCE_SCORE)*self.GLOBAL_BONUS_MULTIPLIER
    @abstractmethod
    def calculate_bonus(self)->float:
        pass

class SalesEmployee(Employee):
    def __init__(self, employee_id: str, name: str, base_salary: float, performance_score: float, total_revenue_generated: float, quota_target: float, customer_retention_rate: float):
        super().__init__(employee_id, name, base_salary, performance_score)
        self.total_revenue_generated=total_revenue_generated
        self.quota_target=quota_target
        self.customer_retention_rate=customer_retention_rate
    def calculate_bonus(self)->float:
        base_modifier=self._calculate_base_modifoer()
        quota_fulfillment=self.total_revenue_generated/self.quota_target
        if quota_fulfillment>=1.2:
            quota_bonus_tier=0.20
        elif quota_fulfillment>=1.0:
            quota_bonus_tier=0.10
        else:
            quota_bonus_tier=0.02
        retention_incentive=self.customer_retention_rate*5000.0
        calculated_payout=(self.base_salary*0.15*base_modifier)+(self.total_revenue_generated*quota_bonus_tier)+retention_incentive
        return round(calculated_payout,2)

class DeveloperEmployee(Employee):
    def __init__(self, employee_id: str, name: str, base_salary: float, performance_score: float, tasks_completed: int, critical_bugs_produced: int, innovation_index: float):
        super().__init__(employee_id, name, base_salary, performance_score)
        self.tasks_completed=tasks_completed
        self.critical_bugs_produced=critical_bugs_produced
        self.innovation_index=innovation_index
    
    def calculate_bonus(self)->float:
        base_modifier=self._calculate_base_modifoer()
        bug_penalty_factor = 1.0 - (self.critical_bugs_produced * 0.08)
        if bug_penalty_factor<0.2:
            bug_penalty_factor=0.2
        task_velocity_bonus=self.tasks_completed*75.0
        innovation_grant=(self.base_salary*0.05)*(self.innovation_index-1.0)
        calculated_payout=((self.base_salary*0.12*base_modifier)+task_velocity_bonus)
        calculated_payout+=innovation_grant
        return round(calculated_payout,2)
    
class ManagerEmployee(Employee):
    def __init__(self, employee_id: str, name: str, base_salary: float, performance_score: float, team_project_success_rate: float, department_budget_saved: float, team_attrition_count: int):
        super().__init__(employee_id, name, base_salary, performance_score)
        self.team_project_success_rate=team_project_success_rate
        self.department_budget_saved=department_budget_saved
        self.team_attrition_count=team_attrition_count
    
    def calculate_bonus(self):
        base_modifier=self._calculate_base_modifoer()
        if self.team_attrition_count==0:
            retention_multiplier=1.15
        elif self.team_attrition_count>3:
            retention_multiplier=0.50
        else:
            retention_multiplier=1.0
        budget_shared_incentive = self.department_budget_saved * 0.05
        leadership_core_bonus = self.base_salary * 0.22 * base_modifier * self.team_project_success_rate
        
        calculated_payout = (leadership_core_bonus * retention_multiplier) + budget_shared_incentive
        return round(calculated_payout, 2)

class BonusPoolManager:
    def __init__(self, corporate_max_budget: float):
        self.corporate_max_budget = corporate_max_budget
        self.__processed_history: List[Dict[str, Any]] = []
    @staticmethod
    def calculate_tax_withholding(gross_bonus: float) -> float:
        if gross_bonus > 25000:
            return gross_bonus * 0.35
        elif gross_bonus > 10000:
            return gross_bonus * 0.25
        elif gross_bonus > 3000:
            return gross_bonus * 0.15
        return gross_bonus * 0.05

    def process_payroll_cycle(self, employees: List[Employee]) -> Dict[str, Any]:
        """
        Main execution workflow. It iterates through an entirely mixed array of employees,
        triggering polymorphic behaviors seamlessly without explicitly checking individual subclasses.
        """
        total_gross_payout = 0.0
        total_tax_withheld = 0.0
        payout_roster = []

        # First pass: Calculate allocations using polymorphism
        for emp in employees:
            # Dynamic dispatch: The interpreter decides which calculate_bonus to run at runtime!
            gross_bonus = emp.calculate_bonus()
            tax_amount = self.calculate_tax_withholding(gross_bonus)
            net_bonus = gross_bonus - tax_amount

            total_gross_payout += gross_bonus
            total_tax_withheld += tax_amount

            payout_roster.append({
                "id": emp.employee_id,
                "name": emp.name,
                "role": type(emp).__name__,
                "gross": gross_bonus,
                "tax": tax_amount,
                "net": net_bonus
            })

        # Safeguard business logic check: Enforce corporate financial constraints
        if total_gross_payout > self.corporate_max_budget:
            # Automatically apply a reduction ratio across the board to remain solvent
            reduction_factor = self.corporate_max_budget / total_gross_payout
            total_gross_payout = 0.0
            total_tax_withheld = 0.0

            for entry in payout_roster:
                entry["gross"] = round(entry["gross"] * reduction_factor, 2)
                entry["tax"] = round(self.calculate_tax_withholding(entry["gross"]), 2)
                entry["net"] = round(entry["gross"] - entry["tax"], 2)
                
                total_gross_payout += entry["gross"]
                total_tax_withheld += entry["tax"]

        summary_report = {
            "company": Employee.COMPANY_NAME,
            "total_gross_disbursed": round(total_gross_payout, 2),
            "total_tax_withheld": round(total_tax_withheld, 2),
            "total_net_payout": round(total_gross_payout - total_tax_withheld, 2),
            "roster_breakdown": payout_roster,
            "budget_limit_breached": total_gross_payout >= self.corporate_max_budget
        }

        self.__processed_history.append(summary_report)
        return summary_report

    @property
    def history(self) -> List[Dict[str, Any]]:
        return self.__processed_history
if __name__ == "__main__":
    # 1. Instantiating a polymorphic assortment of employee records
    staff_roster: List[Employee] = [
        SalesEmployee(
            employee_id="SLS-001", 
            name="Alice Vance", 
            base_salary=85000.0, 
            performance_score=4.8, 
            total_revenue_generated=150000.0, 
            quota_target=120000.0, 
            customer_retention_rate=0.92
        ),
        DeveloperEmployee(
            employee_id="DEV-002", 
            name="Bob Miller", 
            base_salary=110000.0, 
            performance_score=4.2, 
            tasks_completed=142, 
            critical_bugs_produced=1, 
            innovation_index=1.45
        ),
        DeveloperEmployee(
            employee_id="DEV-003", 
            name="Charlie Cruz", 
            base_salary=95000.0, 
            performance_score=2.1, 
            tasks_completed=60, 
            critical_bugs_produced=7, 
            innovation_index=1.0
        ),
        ManagerEmployee(
            employee_id="MGR-004", 
            name="Diana Prince", 
            base_salary=140000.0, 
            performance_score=4.9, 
            team_project_success_rate=0.95, 
            department_budget_saved=32000.0, 
            team_attrition_count=0
        )
    ]

    # 2. Initializing processing manager with a strict financial corporate ceiling
    payroll_manager = BonusPoolManager(corporate_max_budget=60000.0)

    # 3. Processing performance bonus calculations across different execution scenarios
    print("--- Scenario A: Processing Standard Corporate Run ---")
    report_a = payroll_manager.process_payroll_cycle(staff_roster)
    print(f"Company Profile: {report_a['company']}")
    print(f"Gross Payout Distributed: ${report_a['total_gross_disbursed']:,}")
    print(f"Tax Safe-Deposits Retained: ${report_a['total_tax_withheld']:,}")
    print(f"Net Disbursed to Bank Records: ${report_a['total_net_payout']:,}")
    print(f"Budget Adjustment Triggered: {report_a['budget_limit_breached']}")
    
    print("\nIndividual Roster Computations:")
    for person in report_a["roster_breakdown"]:
        print(f" -> [{person['id']}] {person['name']} ({person['role']}) -> Gross: ${person['gross']:,} | Net: ${person['net']:,}")

    # 4. Changing global configurations to observe how class structural adjustments work
    print("\n--- Scenario B: Global Market Boom (Doubling Corporate Multiplier) ---")
    Employee.adjust_global_bonus_multiplier(2.0)
    
    # Lower corporate max budget to force programmatic scaling optimization logic
    tight_payroll_manager = BonusPoolManager(corporate_max_budget=45000.0)
    report_b = tight_payroll_manager.process_payroll_cycle(staff_roster)
    
    print(f"Gross Payout Distributed: ${report_b['total_gross_disbursed']:,}")
    print(f"Budget Adjustment Triggered: {report_b['budget_limit_breached']} (Forced compression executed!)")
    for person in report_b["roster_breakdown"]:
        print(f" -> [{person['id']}] {person['name']} ({person['role']}) -> Scaled Down Gross: ${person['gross']:,}")