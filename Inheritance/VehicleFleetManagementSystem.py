#02-07-2026
#Vehicle Fleet Management System
from datetime import datetime,timedelta
import uuid
class Vehicle:
    total_vehicles_registered=0
    def __init__(self,plate,make,model):
        if not self.__validate_plate(plate):
            raise ValueError('Invalid Plate')
        self.plate=plate
        self.make=make
        self.model=model
        self._mileage=0.0
        self.__is_available=True
        self.__needs_maintenance=False
        Vehicle.total_vehicles_registered+=1

    @staticmethod
    def __validate_plate(plate):
        return True

    @classmethod
    def get_total_fleet_size(cls):
        return f"Total vehicles managed by company: {cls.total_vehicles_registered}"
    
    def is_available(self):
        return self.is_available
    
    def dispatch(self,trip_distance):
        if not self.__is_available:
            return f"[{self.plate}] Error: Vehicle is already dispatched."
        if self.__needs_maintenance:
            return f"[{self.plate}] Error: Vehicle grounded for maintenance."
        if self._mileage>=10000:
            self.__needs_maintenance=True
            return f"[{self.plate}] Error: Vehicle grounded for maintenance."
        self.__is_available=False
        self._mileage+=trip_distance
        return f"[{self.plate}] Dispatched for a {trip_distance} mile trip."
    
    def return_vehicle(self):
        if self.__is_available:
            return f"[{self.plate}] Error: Vehicle is already at the lot."
        self.__is_available=True
        return f"[{self.plate}] Returned safely. Current mileage: {self._mileage}"
    def perform_maintenance(self):
        if self.__needs_maintenance:
            self.__needs_maintenance=False
            self._mileage=0.0
            return f"[{self.plate}] Maintenance complete. Vehicle ready."
        else:
            return "NO Maintenance Required."
    
    def calculate_service_cost(self):
        return 0.0

class DeliveryTruck(Vehicle):
    def __init__(self, plate, make, model,cargo_capacity_lbs):
        super().__init__(plate, make, model)
        self.cargo_capacity_lbs=cargo_capacity_lbs
        self.service_rate_per_mile=1.25
    
    def calculate_service_cost(self):
        cost=self._mileage*self.service_rate_per_mile
        return cost

class PassengerVan(Vehicle):
    def __init__(self, plate, make, model,max_passengers):
        super().__init__(plate, make, model)
        self.max_passengers=max_passengers
        self.service_rate_per_mile=0.60
    
    def calculate_service_cost(self):
        cost=self._mileage*self.service_rate_per_mile
        return cost

class FleetManager:
    def __init__(self,name):
        self.company_name=name
        self.fleet={}
    
    def add_vehicle(self,vehicle:Vehicle):
        if vehicle.plate in self.fleet:
            print(f"Vehicle {vehicle.plate} is already registered.")
        else:
            self.fleet[vehicle.plate]=vehicle
            print(f"Added {vehicle.make} {vehicle.model} to fleet.")
    
    def run_daily_dispatch(self,plate,distance):
        vehicle=self.fleet.get(plate)
        if vehicle:
            print(vehicle.dispatch(distance))
        else:
            print(f"Plate {plate} not found in fleet.")
    
    def run_daily_returns(self, plate):
        vehicle = self.fleet.get(plate)
        if vehicle:
            print(vehicle.return_vehicle())
        else:
            print(f"Plate {plate} not found in fleet.")
    def generate_financial_report(self):
        """Loops through objects and uses polymorphism to calculate costs."""
        print(f"\n--- {self.company_name} Maintenance Liability Report ---")
        total_liability = 0
        for plate, vehicle in self.fleet.items():
            # The manager doesn't care if it's a Truck or Van. 
            # It just calls the method, and the specific child class handles the math.
            cost = vehicle.calculate_service_cost()
            total_liability += cost
            status = "AVAILABLE" if vehicle.is_available() else "DISPATCHED"
            print(f"[{plate}] | Type: {type(vehicle).__name__} | Status: {status} | Accrued Service Cost: ${cost:.2f}")
        
        print(f"TOTAL FLEET SERVICE LIABILITY: ${total_liability:.2f}")
        print("--------------------------------------------------\n")


# ==========================================
# 4. EXECUTION (Testing the logic)
# ==========================================
if __name__ == "__main__":
    # Create our Manager
    manager = FleetManager("Express Logistics Corp")

    # Create Objects (Instances of Child Classes)
    truck1 = DeliveryTruck("TRK99", "Ford", "F-650", 10000)
    truck2 = DeliveryTruck("TRK44", "Volvo", "VNL", 30000)
    van1 = PassengerVan("VAN123", "Mercedes", "Sprinter", 12)

    # Note: If you try to create a vehicle with a bad plate like "T", the static method will throw an error!

    # Add objects to manager
    manager.add_vehicle(truck1)
    manager.add_vehicle(truck2)
    manager.add_vehicle(van1)

    print("\n" + Vehicle.get_total_fleet_size() + "\n")

    # Run Business Logic
    manager.run_daily_dispatch("TRK99", 500)
    manager.run_daily_dispatch("VAN123", 120)
    
    # Attempt to double-dispatch the truck to test private variable safeguards
    manager.run_daily_dispatch("TRK99", 100) 
    
    # Return the van
    manager.run_daily_returns("VAN123")

    # Generate Reports
    manager.generate_financial_report()