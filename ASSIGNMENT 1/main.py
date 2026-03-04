from fastapi import FastAPI,Query

app = FastAPI()

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True },
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True}, 
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

# Q1. Add 3 More Products 
# Scenario: Your client just added 3 new items to their store — a Laptop Stand, a Mechanical Keyboard, and a Webcam. 
# The mobile app needs to show them. Add these to your products list.
@app.get('/')
def home():
    return {"message":"Welcome to Our Ecommerce Website"}

@app.get('/products')
def get_all_product():
    return{"product":products , "total":len(products)}

# Q2. Easy Add a Category Filter Endpoint 
# Scenario: The mobile app wants to show only Electronics on one page and only Stationery on another.
#  You need a new endpoint that filters products by category.
@app.get("/products/category/{category_name}")
def get_by_category(category_name:  str):
    result = [p for p in products if p["category"] == category_name]
    if not result:
        return {"error": "No products found in this category"}
    return {"category": category_name,'filter_products': result , 'total' : len(result)}

#Q3. Show Only In-Stock Products
# Scenario: Customers are complaining they can see products that are out of stock and then get disappointed. 
# The app team wants a separate endpoint that returns ONLY available products.
@app.get("/products/{in_stock}")
def in_stock(in_stock:str):
    result = [p for p in products if p["in_stock"] == True]
    return {"in_stock_products": result, "count": len(result)}

#Q4. Build a Store Info Endpoint
# Scenario: The mobile app's home screen needs to show a summary of the store — total products, 
# how many are in stock, and all available categories. 
# Build one endpoint that returns all of this.
@app.get("/store/summary")
def get_summary():
    in_stock = [p for p in products if p["in_stock"] == True]
    out_of_stock = len(products) - len(in_stock)
    categories = list(set(p["category"] for p in products))
    return { "store_name": "My E-commerce Store", "total_products": len(products), "in_stock": in_stock, "out_of_stock": out_of_stock, "categories":categories }

#Q5. Search Products by Name
# Scenario: Users want to search for products. 
# When they type "mouse" in the search bar, the app should show all products whose name contains that word. 
# Build this search endpoint.
@app.get('/products/search/{keyword}')
def filter_product(keyword:str):
    result = [p for p in products if keyword.lower() in p["name"].lower() ]
    if not result:
        return {"message": "No products matched your search"}
    return {"Product": keyword ,"Results": result, "total_count":len(result)}

#Q6(Bonus Q)
# Cheapest & Most Expensive Product
# Scenario: The app wants to show a "Best Deal" section (cheapest product) and a "Premium Pick" section (most expensive product) on the home screen. 
# Build one endpoint that returns both.
@app.get('/products/deals')
def get_deal():
   result = products
   highest_price = max(products ,key=lambda p:p['price'])
   lowest_price = min(products ,key=lambda p:p['price'])
   return { "best_deal": lowest_price, "premium_pick": highest_price }
