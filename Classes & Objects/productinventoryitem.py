#08-06-2026
#Product Inventory Item
class Product:
    store_name="Amazon"
    total_product=1
    catalogue={}
    def __init__(self,name,category,price,quantity,supplier):
        if price <=0:
            raise ValueError("Price of The Product Can`t be Zero or Less")
        if quantity <0:
            raise ValueError("Product Quantity Can`t Be Lessthan zero")
        self.p_id="PRO_"+str(Product.total_product)
        self.name=name
        self.category=category
        self.price=price
        self.quantity=quantity
        self.supplier=supplier
        self.status = "Is Active" if quantity>0 else "Out of Stock"
        Product.total_product+=1
        Product.catalogue[self.p_id]=self
    
    def restock(self,quantity):
        if quantity <=0:
            raise ValueError("Product Quantity Can`t Be Lessthan zero")
        self.quantity+=quantity
        self.status="In Stock"
        print(f"{quantity} Added to {self.name} New Quantity : {self.quantity}")

    def sell(self,quantity):
        if quantity <=0:
            raise ValueError("Product Quantity Can`t Be Lessthan zero")
        if quantity > self.quantity:
            raise ValueError("Insuffiecent Quantity")
        self.quantity-=quantity
        if self.quantity == 0:
            self.status="Out of Stock"
            print(f"  [-] {quantity} units sold. '{self.name}' is now OUT OF STOCK.")
        else:
            print(f"{quantity} Sold from {self.name} and Available Stock {self.quantity}")

    def details(self):
        print("Product Details :")
        print(f"  Store      : {Product.store_name}")
        print(f"  Product ID : {self.p_id}")
        print(f"  Name       : {self.name}")
        print(f"  Category   : {self.category}")
        print(f"  Price      : ₹{self.price}")
        print(f"  Quantity   : {self.quantity}")
        print(f"  Supplier   : {self.supplier}")
        print(f"  Status     : {self.status}")
    
    def search_product(search):
        for pro in Product.catalogue.values():
            if search in pro.p_id or search in pro.name:
                pro.details()

    def show_full_catalogue():
        print(f"  {Product.store_name} — Product Catalogue")
        print(f"  Total Products : {Product.total_product}")
        for pid, product in Product.catalogue.items():
            tag = "✔" if product.status == "In Stock" else "✘"
            print(f"  {pid} | {product.name:<22} | "f"₹{product.price:<8} | {tag} {product.status}")

p1 = Product("Samsung Galaxy S24", "Electronics", 74999, 30, "Samsung India")
p2 = Product("Nike Air Max 270",   "Footwear",    8999,  50, "Nike Distributors")
p3 = Product("Basmati Rice 5kg",   "Groceries",   450,    5, "India Gate Foods")
p4 = Product("Sony WH-1000XM5",   "Electronics", 29999,  0, "Sony India")
p4.restock(100)
p1.sell(10)
Product.search_product("24")
Product.show_full_catalogue()