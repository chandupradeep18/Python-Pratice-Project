#04-07-2026
#Payment Gateway Integrator
from abc import ABC,abstractmethod
import uuid
from time import time
import random
from datetime import datetime

class PaymentAuthenticationError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class FraudDetectionError(Exception):
    pass

class Product:
    def __init__(self,name:str,price:float):
        self.product_id=str(uuid.uuid4())[:8]
        self.name=name
        self.price=price

class Customer:
    def __init__(self,first_name:str,last_name:str,email:str):
        self.customer_id=str(uuid.uuid4())[:8]
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.orders={}
        self.cart={}
    
    def get_full_name(self):
        return self.first_name+' '+self.last_name
    
    def add_to_cart(self,product:Product,qty:int):
        if qty<=0:
            raise ValueError('Invalid Qty for Product')
        if product.product_id in self.cart:
            self.cart[product.product_id]['qty']+=qty
        else:
            self.cart[product.product_id]={'name':product.name,'price':product.price,'qty':qty}
        print(f'Product {product.name} Added to Cart with Qty : {qty}')
    
    def generate_order(self):
        if not self.cart:
            print('Cart is Empty')
            return
        order=Order(self)
        for item in self.cart.values():
            order.create_order(item)
        self.cart.clear()
        print(f'New Order Created with Id : {order.order_id}')
        return order

class Order:
    base_tax_rate = 0.08
    def __init__(self,customer:Customer):
        self.order_id=str(uuid.uuid4())
        self.customer=customer
        self.items=[]
        self.is_paid=False
        self.transaction_id=None
        self.status="Pending"
        self.item_value=0.0
        self.tax_value=0.0
        self.total_value=0.0
        self.fee=0.0
        self.paid_amount=0.0
        self.created_at=datetime.now()
    
    def create_order(self,item):
        self.items.append(item)
        print(f'{item['name']} added to order')
    
    def get_subtotal(self)->float:
        self.item_value=sum(item['price']*item['qty'] for item in self.items)
        return self.item_value
    
    def get_tax_amount(self)->float:
        self.tax_value=self.get_subtotal()*Order.base_tax_rate
        return self.tax_value
    
    def get_total(self):
        self.total_value=self.get_subtotal()+self.get_tax_amount()
        return self.total_value
    
    def generate_invoice(self)->str:
        invoice = f"\n--- INVOICE: ORDER {self.order_id} ---\n"
        invoice += f"Customer: {self.customer.get_full_name()}\n"
        invoice += "-" * 30 + "\n"
        for item in self.items:
            invoice += f"{item['name']} ${item['price']}\n"
        invoice += "-" * 30 + "\n"
        invoice += f"Subtotal:           ${self.get_subtotal()}\n"
        invoice += f"Tax ({(Order.base_tax_rate*100)}%):        ${self.get_tax_amount()}\n"
        invoice += f"TOTAL DUE:          ${self.get_total()}\n"
        return invoice

class PaymentGateway(ABC):
    supported_currencies = ['USD', 'EUR', 'GBP', 'INR']
    total_successful_transactions = 0
    total_volume_processed = 0.0

    def __init__(self,gateway_name):
        self.gateway_name=gateway_name
        self._is_authenticated=False
        self._transaction_log=[]
    
    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def process_transaction(self,amount,currency,source_details):
        pass

    @abstractmethod
    def generate_receipt(self,transaction_id:str,amount:float)->str:
        pass

class CreditCard(PaymentGateway):
    processing_fee_percentage = 0.029
    def __init__(self, merchant_name:str,api_key:str,secret_key:str,card_no:str):
        super().__init__(merchant_name)
        self.__api_key=api_key
        self.__secret_key=secret_key
        self.__card_no=card_no.strip()
    
    def validate_card_number(self):
        return len(self.__card_no)==16 and self.__card_no.isdigit()
    
    def _run_fraud_check(self,amount:float)->bool:
        if amount >5000:
            raise FraudDetectionError("Transaction exceeds maximum safe limit. Flagged for review.")
        return True
    
    def authenticate(self)->float:
        if len(self.__api_key)<10 or len(self.__secret_key)<10:
            raise PaymentAuthenticationError("Invalid API credentials provided to Gateway.")
        self._is_authenticated=True
        return True
    
    def process_transaction(self, amount, currency, customer):
        if not self._is_authenticated:
            self.authenticate()
        if currency not in CreditCard.supported_currencies:
            raise ValueError('Invalid Currency')
        if not self.validate_card_number():
            raise PaymentAuthenticationError("Invalid Card Details provided to Gateway.")
        fee = amount*self.processing_fee_percentage
        total=amount+fee
        #self._run_fraud_check(total)
        return True,fee,total
    
    def generate_receipt(self, transaction_id, amount):
        return f"CC-RECEIPT [{transaction_id}]: Successfully charged ${amount:.2f} via Secure Credit Network."

class Crypto(PaymentGateway):
    network_fee_flat = 5.00
    def __init__(self, gateway_name,wallet_address):
        super().__init__(gateway_name)
        self._wallet_address=wallet_address
    
    def validate_address(self)->bool:
        return self._wallet_address.startswith("0x") and len(self._wallet_address) == 42
    
    def authenticate(self):
        if not self.validate_address():
            raise PaymentAuthenticationError("Invalid Merchant Wallet Address.")
        self._is_authenticated=True
        return True
    
    def process_transaction(self, amount, currency, source_details):
        if not self._is_authenticated:
            self.authenticate()
        total=amount+self.network_fee_flat
        print(f"[CryptoGateway] Awaiting blockchain confirmations for ${total:.2f} (Includes ${self.network_fee_flat:.2f} gas fee)")
        return True,self.network_fee_flat,total
    
    def generate_receipt(self, transaction_id: str, amount: float) -> str:
        return f"CRYPTO-BLOCK [{transaction_id}]: Smart contract executed for ${amount:.2f}."

class PaymentProcessor:
    total_volume_processed = 0.0 
    total_transactions_count = 0

    def __init__(self,gateway:PaymentGateway):
        self.gateway = gateway
    
    def checkout(self,order:Order):
        if order.is_paid:
            raise ValueError('Order Already Paid')
        print(order.generate_invoice())
        amount=order.total_value
        print(f"\n--- INITIATING PAYMENT VIA {self.gateway.gateway_name} ---")
        try:
            succes,fee,total=self.gateway.process_transaction(amount,'INR',order.customer)
            if succes:
                order.is_paid=True
                tx_id = f"TXN-{random.randint(10000, 99999)}"
                order.fee=fee
                order.paid_amount=total
                order.transaction_id=tx_id
                
                print(self.gateway.generate_receipt(tx_id,amount))
                PaymentProcessor.total_volume_processed += amount
                PaymentProcessor.total_transactions_count += 1
                print(f"Success! {order.customer.first_name}'")
        except PaymentAuthenticationError as e:
            print(f"SYSTEM ERROR: Payment Gateway Authentication Failed. {e}")
        except InsufficientFundsError as e:
            print(f"DECLINED: {e}")
        except FraudDetectionError as e:
            print(f"SECURITY ALERT: {e}")
        except Exception as e:
            print(f"UNKNOWN ERROR: An unexpected error occurred: {e}")
            
        print("-" * 40 + "\n")

if __name__ == "__main__":
    # 1. Setup our products
    laptop = Product("Dev Laptop Pro", 1200.00)
    mouse = Product("Wireless Mouse", 45.00)
    keyboard = Product("Mechanical Keyboard", 150.00)
    
    # 2. Setup our Customers
    alice = Customer("Alice", "Smith", "alice@example.com")
    bob = Customer("Bob", "Jones", "bob@crypto.com")
    
    # 3. Setup our Orders
    alice.add_to_cart(laptop,10)
    alice.add_to_cart(mouse,5)

    order1 = alice.generate_order()
    
    
    bob.add_to_cart(keyboard, 2)
    order2 = bob.generate_order()
    
    # 4. Initialize Gateways
    stripe_gateway = CreditCard("Stripe CC", api_key="sk_live_1234567890", secret_key="sec_987654321",card_no="1234567891234567")
    coinbase_gateway = Crypto("Coinbase Pay", wallet_address="0x1234567890abcdef1234567890abcdef12345678")
    
    # 5. Process Transactions using different processors
    processor_one = PaymentProcessor(stripe_gateway)
    processor_two = PaymentProcessor(coinbase_gateway)
    
    # Execute Alice's large order via Credit Card
    processor_one.checkout(order1)
    
    # Execute Bob's order via Crypto (Will fail due to insufficient funds after gas/tax)
    processor_two.checkout(order2)