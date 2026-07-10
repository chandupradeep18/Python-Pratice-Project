#30-06-2026
#Public Transit Ticket Issuer
from datetime import datetime
class TransitSystem:
    agency_name = "MetroWay City Transit"
    base_rate_per_km = 0.50
    peak_hour_multiplier = 1.5
    total_system_revenue = 0.0
    route_map = {
        "North Station": {"Central Hub": 5, "South Station": 12, "Airport": 20},
        "Central Hub": {"North Station": 5, "South Station": 7, "Airport": 15},
        "South Station": {"North Station": 12, "Central Hub": 7, "Airport": 8},
        "Airport": {"North Station": 20, "Central Hub": 15, "South Station": 8}
    }
    # Valid passenger types and their discount multipliers
    discount_rates = {
        "Adult": 1.0,      # 0% discount
        "Student": 0.75,   # 25% discount
        "Senior": 0.50     # 50% discount
    }
    
    def get_distance(self,start,end):
        if start==end:
            return 0
        if start in self.route_map and end in self.route_map[start]:
            return self.route_map[start][end]
        return -1
    
    def process_ticket_purchase(self,passenger_type,start,end, is_peak_hour, wallet_balance):
        distance = self.get_distance(start, end)
        if distance == -1:
            print("Error: Invalid route selected.")
            return False,"Error: Invalid route selected."
        if distance == 0:
            print("Error: Start and End stations are the same.")
            return False,"Error: Start and End stations are the same."
        fare=distance*TransitSystem.base_rate_per_km
        if is_peak_hour:
            fare*=TransitSystem.peak_hour_multiplier
        discount=TransitSystem.discount_rates.get(passenger_type,1.0)
        final_fare=fare*discount
        if wallet_balance < final_fare:
            print(f"Error: Insufficient funds. Fare is ${final_fare:.2f}, Wallet has ${wallet_balance:.2f}.")
            return False,"Error: Insufficient funds. Fare is ${final_fare:.2f}, Wallet has ${wallet_balance:.2f}."
        TransitSystem.total_system_revenue += final_fare
        new_ticket=Ticket(passenger_type,start,end,final_fare,is_peak_hour)
        new_balance = wallet_balance - final_fare
        return True, (new_ticket, new_balance)

class Ticket:
    next_serial_number = 10000
    def __init__(self,p_type, start_station, end_station, price, is_peak):
        self.ticket_id = f"TKT-{Ticket.next_serial_number}"
        Ticket.next_serial_number += 1
        self.passenger_type=p_type
        self.start_station=start_station
        self.end_station=end_station
        self.price=price
        self.is_peak=is_peak
        self.issue_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def format_ticket_data(self):
        return {
            "Agency": TransitSystem.agency_name,
            "Ticket ID": self.ticket_id,
            "Issued To": f"({self.passenger_type})",
            "Route": f"{self.start_station} -> {self.end_station}",
            "Peak Travel": "Yes" if self.is_peak else "No",
            "Price Paid": f"${self.price:.2f}",
            "Timestamp": self.issue_time
        }

metro = TransitSystem()
user_requests = [
    {"name": "Alice", "type": "Adult", "start": "North Station", "end": "Central Hub", "peak": True, "wallet": 20.00},
    {"name": "Bob", "type": "Student", "start": "South Station", "end": "Airport", "peak": False, "wallet": 5.00}, # Will fail (insufficient funds)
    {"name": "Charlie", "type": "Senior", "start": "Airport", "end": "Central Hub", "peak": False, "wallet": 50.00},
    {"name": "Diana", "type": "Adult", "start": "North Station", "end": "Unknown Station", "peak": True, "wallet": 100.00}, # Will fail (invalid route)
    {"name": "Eve", "type": "Student", "start": "Central Hub", "end": "Airport", "peak": True, "wallet": 15.00}
]

issued_tickets = []
for req in user_requests:
    success, result=metro.process_ticket_purchase(
        passenger_type=req["type"],
        start=req["start"],
        end=req["end"],
        is_peak_hour=req["peak"],
        wallet_balance=req["wallet"])
    if success:
        ticket_obj, remaining_balance = result
        issued_tickets.append(ticket_obj)
        print(f"SUCCESS: Ticket issued to {req['name']}. Remaining wallet balance: ${remaining_balance:.2f}")
    else:
        print(f"FAILED for {req['name']}: {result}")

for ticket in issued_tickets:
    details=ticket.format_ticket_data()
    for key, value in details.items():
        print(f"{key}: {value}")
    