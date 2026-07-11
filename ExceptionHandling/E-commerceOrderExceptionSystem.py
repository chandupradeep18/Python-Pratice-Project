#24-06-2026
#E-commerce Order Exception System
from datetime import datetime,date,timedelta
import random
class OrderError(Exception):
    pass
class OutOfStockError(OrderError):
    def __init__(self, product_name,requested,available):
        self.product_name=product_name
        self.requested=requested
        self.available=available
        super().__init__(f"'{product_name}': requested  {requested}, only {available} available.")

class ProductNotActiveError(OrderError):
    pass

class PaymentDeclinedError(OrderError):
    pass

class CheckoutValidationError(OrderError):
    def __init__(self, errors: list):
        self.errors=errors
        summary = f"{len(errors)} problem(s) found in cart:"
        details = '\n'.join(f" -{e}" for e in errors)
        super().__init__(f"{summary}\n{details}")

class Product:
    def __init__(self,name,price,stock):
        self.name=name
        self.price=price
        self.stock=stock
        self.is_active=True
    
    def reduce(self,qty):
        self.stock-=qty
    
    def add_stock(self,qty):
        self.stock+=qty
    
    def __str__(self):
        return f"{self.name} (₹{self.price}, stock: {self.stock})"

class InventoryLock:
    pass

class Cart:
    pass

class OrderProccessor:
    pass