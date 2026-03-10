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
@app.get("/products/in-stock")
def get_in_stock_products():
    result = [p for p in products if p["in_stock"]]
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


#_______________________________________________ Assignment 2 ____________________________________________________________________ 
from typing import Optional , List
from pydantic import BaseModel , Field

# Q1. Filter Products by Minimum Price
#a. Add a new query parameter min_price: int to the existing /products/filter endpoint 
#b. When min_price is sent, return only products priced at or above that value
#c. It must work together with the existing filters — combining min_price and category at the same time must work
@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    max_price: int = Query(None, description='Maximum price'),
    min_price: int = Query(None, description='Minimum price')
):
    result = products
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if max_price:
        result = [p for p in result if p["price"] <= max_price]
    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    return {"total_products": len(result),"products": result}

# Q2. GET + Path Parameter 
# ------- Get Only the Price of a Product -------
# ' Scenario: The app's cart page only needs to know a product's name and price — not the full details.
#  Instead of fetching everything, build a lightweight endpoint that returns only the name and price for a given product ID. '
@app.get("/products/{product_id}/price")
def get_price_of_product(product_id : int):
    for p in products:
        if p['id'] == product_id:
            return { "name":p["name"] , "price" : p["price"] }
    return { "error" : "Product Not Found"}

# Q3. Pydantic + POST
#  ------ Accept Customer Feedback ------
# '' Scenario: After receiving their order, customers want to leave a rating and comment for the product they bought.
# Build a POST endpoint that accepts and validates their feedback — rating must be 1 to 5, comment is optional. ''

# ----------------------Pydantic model---------------------
class CustomerFeedback(BaseModel):
    customer_name : str = Field(...,min_length = 2 ,max_length = 50)
    product_id : int = Field(...,gt = 0)
    delivery_address : str = Field(...,max_length=200)
    rating : int = Field(...,ge = 1 ,le =5)
    customer_feedback : Optional[str] = Field(...,max_length=300)

feedback = []
feedback_count = 0

@app.post("/feedback")
def submit_feedback(data : CustomerFeedback):
    feedback.append(data.model_dump())
    return {
        "message": "Feedback Submitted Successfully",
        "feedback"  : data ,
        "total_feedback" : len(feedback)
    }

# Q4. Build a Product Summary Dashboar
# Scenario: The business owner wants a quick dashboard endpoint — total products, how many are in stock, cheapest product,
# most expensive product, and a breakdown of products per category. 
# One endpoint, all the stats.
@app.get("/products/summary")
def get_product_summary():
    results = products
    in_stock = [p for p in results if p["in_stock"]]
    out_stock = [p for p in results if not p["in_stock"]]

    most_expensive = max(products,key = lambda x:x["price"])
    cheapest = min(products,key = lambda x:x["price"])

    categories = list(set(p['category'] for p in products))

    return {
    "store_name": "My E-commerce Store" ,
    "total_products" :    len(products),
    "in_stock_count":    len(in_stock),
    "out_of_stock_count": len(out_stock),
    "most_expensive":    {
        "name" : most_expensive["name"],
        "price" : most_expensive["price"]
    },
    "cheapest":  {
        "name" : cheapest["name"],
        "price" : cheapest["price"]
    },
    "categories": categories
}

# Q5. Validate & Place a Bulk Order
# Scenario: A corporate client wants to place bulk orders for their office. 
# They send their company name, contact email, and a list of items. Each item has a product ID and quantity. 
# Build an endpoint that validates the input, checks stock, calculates the total bill, and confirms the order.
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity:   int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name:  str           = Field(..., min_length=2)
    contact_email: str           = Field(..., min_length=5)
    items:         List[OrderItem] = Field(..., min_items=1)
    
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}

# Q6 .Bonus Question  Order Status Tracker
# Scenario: Right now orders are confirmed immediately. 
# The business wants a two-step flow — orders start as "pending" and only move to "confirmed" when the warehouse approves them.
# Build this status tracking system
class Order(BaseModel):
    product_id: int
    quantity: int
orders = []
@app.post("/orders")
def create_order(order: Order):

    order_data = {
        "id": len(orders) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(order_data)

    return order_data

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["id"] == order_id:
            return order

    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["id"] == order_id:
            order["status"] = "confirmed"
            return order

    return {"error": "Order not found"}