#12-07-2026
import json
import requests
base_url="https://api.escuelajs.co/api/v1/"
product='products'


user_profile = {
    "user_id": 10482,
    "username": "alex_dev",
    "is_active": True,
    "roles": ["admin", "editor"],
    "profile_info": {
        "first_name": "Alex",
        "last_name": "Rivers",
        "email": "alex.rivers@example.com",
        "age": 29
    },
    "preferences": {
        "newsletter": False,
        "theme": "dark"
    },
    "social_links": None  # Serializes to JSON null
}
product_catalog = [
    {
        "id": "PROD-001",
        "name": "Wireless Noise-Canceling Headphones",
        "category": "Electronics",
        "price": 199.99,
        "in_stock": True,
        "tags": ["audio", "bluetooth", "wireless"],
        "ratings": {"average": 4.7, "count": 128}
    },
    {
        "id": "PROD-002",
        "name": "Ergonomic Mechanical Keyboard",
        "category": "Peripherals",
        "price": 129.50,
        "in_stock": False,
        "tags": ["keyboard", "office", "gaming"],
        "ratings": {"average": 4.5, "count": 89}
    }
]
order_details = {
    "order_id": "ORD-2026-98412",
    "customer": {
        "name": "Jordan Smith",
        "email": "jordan.s@example.com"
    },
    "items": [
        {"item_name": "Python Crash Course Book", "qty": 1, "unit_price": 35.00},
        {"item_name": "USB-C Hub Multiport", "qty": 2, "unit_price": 24.99}
    ],
    "subtotal": 84.98,
    "tax": 6.80,
    "grand_total": 91.78,
    "shipping_address": {
        "street": "123 Tech Lane",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701"
    }
}
#dumps->Python Object to json String
user_profile_json=json.dumps(user_profile)
print(user_profile)
print(user_profile_json)
#loads->json String to Python Object
#user_product_object=json.loads(product_catalog)
#product_catalog(user_product_object)

#dump()  ->convert python object into json file
response=requests.get(base_url+product,json={'limit':100,'offset':1})
if response.status_code==200:
    with open('Products.json','w') as file:
        json.dump(response.json(),file)
        print('File Created Successfully')
else:
    print("No Data Found")
response=requests.get(base_url+'users',json={'limit':100,'offset':1})
if response.status_code==200:
    with open('Users.json','w') as file:
        json.dump(response.json(),file)
        print('File Created Successfully')
else:
    print("No Data Found")
#load() -> json file to python object
with open('d:/Github/Remote_Github/Python-Pratice-Project/Users.json','r') as file:
    users_data=json.load(file)
print(len(users_data))
with open('d:/Github/Remote_Github/Python-Pratice-Project/Products.json','r') as file:
    products_data=json.load(file)
print(len(products_data))