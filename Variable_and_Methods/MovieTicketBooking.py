#08-06-2026
import random
class MovieTicketBooking:
    movie_name = "Inception"
    theater_name = "PVR Cinemas"
    ticket_price = 150
    total_seats = 100
    total_bookings = 0
    def __init__(self,name,phone,seats):
        if seats <= 0:
            raise ValueError("Number of seats must be greater than zero")
        if seats > MovieTicketBooking.total_seats:
            raise ValueError("Not enough seats available")
        
        MovieTicketBooking.total_bookings+=seats
        MovieTicketBooking.total_seats-=seats
        self.booking_id = random.randint(1000,9999)
        self.name = name
        self.phone = phone
        self.seats_booked = seats
        self.total_price = self.total_ticket_price()
        self.display_booking_details()

    def total_ticket_price(self):
        return self.seats_booked * MovieTicketBooking.ticket_price
    
    def display_booking_details(self):
        print(f"Booking ID: {self.booking_id}")
        print(f"Name: {self.name}")
        print(f"Phone: {self.phone}")
        print(f"Movie: {MovieTicketBooking.movie_name}")
        print(f"Theater: {MovieTicketBooking.theater_name}")
        print(f"Seats Booked: {self.seats_booked}")
        print(f"Total Price: {self.total_price}")
    
    @classmethod
    def display_Movie_Details(cls):
        print(f"Movie: {cls.movie_name}")
        print(f"Theater: {cls.theater_name}")
        print(f"Ticket Price: {cls.ticket_price}")
        print(f"Total Seats Available: {cls.total_seats}")
        print(f"Total Bookings: {cls.total_bookings}")
        print(f"Total Seats : {cls.total_seats+cls.total_bookings}")

try:
    booking1 = MovieTicketBooking("Alice", "1234567890", 10)
except ValueError as e:
    print(f"Error: {e}")
MovieTicketBooking.display_Movie_Details()