#12-07-2026
import requests
base_url="https://api.escuelajs.co/api/v1/"
product='products'

#listing all Product
"""params={'limit':1,'offset':1}
response=requests.get(base_url+product,json=params)
products=response.json()
for product in products:
    print(product['id'])
    print(product['title'])
    print(product['slug'])
    print(product['price'])
    print(product['creationAt'])
    print(product['updatedAt'])
    print(product['category']['id'])
    print(product['category']['name'])
    print(product['category']['slug'])
    print(product['category']['image'])
    print(product['category']['creationAt'])
    print(product['category']['updatedAt'])
    for image in product['images']:
        download = requests.get(image)
        print(download.status_code)
        filename = f"product_{product['id']}image.html"
        with open(filename, "wb") as f:
            f.write(download.content)
            print(f"Saved: {filename}")
        
        break"""

#create A product
"""payload={"title": "Classic Orange Hooded Sweatshirt","price": 150,"description": "Classic White Hooded Sweatshirt","categoryId": 2,"images": ["https://i.imgur.com/QkIa5tT.jpeg"]}
header={"Content-Type": "application/json"}
create_product=requests.post(base_url+product,json=payload,headers=header)
print(create_product.status_code)
print(create_product.json())"""

#get Product By Id
"""get_product=requests.get(base_url+product+'/73')
print('Status Code : ',get_product.status_code)
if get_product.status_code==200:
    product=get_product.json()
    print(product['id'])
    print(product['title'])
    print(product['slug'])
    print('Price : ',product['price'])
    print(product['creationAt'])
    print(product['updatedAt'])
    print(product['category']['id'])
    print(product['category']['name'])
    print(product['category']['slug'])
    print(product['category']['image'])
    print(product['category']['creationAt'])
    print(product['category']['updatedAt'])
    for image in product['images']:
        print(image)"""

#put Product By Id
payload={"title": "Classic Brown Hooded Sweatshirt","price": 200,"description": "Classic White Hooded Sweatshirt","categoryId": 2,"images": ["https://i.imgur.com/QkIa5tT.jpeg"]}
header={"Content-Type": "application/json"}
#update_product=requests.put(base_url+product+'/73',json=payload,headers=header)
#print(update_product.status_code)

#delete Product By Id
"""delete_product=requests.delete(base_url+product+'/72')
print(delete_product.status_code)
print(delete_product.json())
"""

user='users'
#get all User
"""get_all_users=requests.get(base_url+user)
print(get_all_users.status_code)
for us in get_all_users.json():
    print(us)
    break"""

#create User
"""payload={'email': 'change@mail.com', 'password': 'changeme', 'name': 'Jhon', 'role': 'customer', 'avatar': 'https://i.imgur.com/LDOO4Qs.jpg'}
check_email=requests.post(base_url+user+'/is-available',json={'email':payload['email']})
print(check_email.status_code)
print(check_email.json()['isAvailable'])
if check_email.status_code==201 and check_email.json()['isAvailable']==False:
    create_user=requests.post(base_url+user,json=payload)
    print(create_user.status_code)
    if create_user.status_code==201:
        print('User Created Successfull')
        print(create_user.json())
    else:
        print(create_user.json())
else:
    print('Email Already Exist')"""


