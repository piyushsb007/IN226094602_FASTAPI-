from fastapi import FastAPI,HTTPException
from pydantic import BaseModel  

app = FastAPI()
#_______________________________________________ Assignment 4 ____________________________________________________________________
# Cart System

products = {
1: {"name": "Wireless Mouse", "price": 499, "in_stock": True},
2: {"name": "Notebook", "price": 99, "in_stock": True},
3: {"name": "Pen Set", "price": 49, "in_stock": True},
4: {"name": "USB Hub", "price": 799, "in_stock": False}
}

# In-Memory Storage
cart = []
orders = []
order_counter = 1

# Request Model
class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

# Helper Function
def calculate_total(product, quantity):
    return product["price"] * quantity

#Q1.  Add Items to the Cart
#Scenario: A customer visits the store and wants to buy a Wireless Mouse (qty 2) and a Notebook (qty 1).
# Add both items to the cart using POST /cart/add.
@app.post("/cart/add")
def add_to_cart(product_id : int , quantity:int = 1):

    if product_id not in products:
        raise HTTPException(status_code=404, detail = "Product not found")
    
    product = products[product_id]

    if not product['in_stock']: # Q3
        raise HTTPException(status_code = 404, detail = f"{product['name']} out of stock")
    
    # Check if item in cart
    for item in cart: # Q4
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            item['subtotal'] = calculate_total(product,quantity)

            return { 
                "message" : "Cart Updated" ,
                "Cart_item" : item
                }
    # Add new item
    cart_item = {
        'product_id' : product_id,
        'product_name' : product['name'],
        'quantity' : quantity , 
        'unit_price' : product['price'],
        'subtotal' : calculate_total(product,quantity)
    }
    cart.append(cart_item) 
    return {         #Q4
        "message": "Added to cart",  
        "cart_item": cart_item
    }

# Q2. View the Cart and Verify the Total
#Scenario: The customer wants to review what's in their cart before buying. Use GET /cart and confirm the grand total matches your manual calculation.
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message" : "Cart is Empty"}
    
    grand_total = sum(item['subtotal'] for item in cart)

    return {
        'items' : cart,
        'item_count' : len(cart),
        'grand_total' : grand_total
    }


# Q3. Try Adding an Out-of-Stock Product
#Scenario: The customer sees the USB Hub on the website and tries to add it to the cart.
# But the USB Hub (id=3) is out of stock. Your API must reject it with the correct error.
# --Done above---

# Q4. Add More Quantity of an Existing Cart Item
#Scenario: The customer decides they want one more Wireless Mouse.
# When you add the same product again, the cart should update the quantity — not create a duplicate entry.
# --Done above---

# Q5. Remove an Item Then Checkout
#Scenario: The customer changed their mind about the Notebook. 
# They remove it from the cart, then proceed to checkout with only the Wireless Mouse. 
# Run the full remove + checkout flow.
@app.delete("/cart/{product_id}")
def remove_item(product_id:int):
    for item in cart:
        if item['product_id'] == product_id:
            cart.remove(item)

            return {
                "message" : f"{item['product_name']} removed from cart"
            }
    raise HTTPException(status_code = 400 , detail = "Item not in cart")
# Checkout
@app.post("/cart/checkout")
def checkout(order: CheckoutRequest):
    global order_counter

    if not cart: #Bonus Q
        raise HTTPException(status_code=400,detail= 'Cart is empty - Add items First')
    
    grand_total = sum(item["subtotal"] for item in cart)
    placed_orders = []

    for item in cart:
        new_order = {
            'order_id' : order_counter,
            'customer_name' : order.customer_name,
            'product' : item["product_name"] ,
            'quantity' : item['quantity'] ,
            'total_price' : item['subtotal'],
            'delivery_address' : order.delivery_address
        }

        orders.append(new_order)
        placed_orders.append(new_order)

        order_counter += 1
    cart.clear() 

    return{
        "message" : "Checkout Successful",
        "orders_placed" : placed_orders,
        "grand_total" : grand_total
    }

#Q6. Full Cart System Flow — 2 Customers, 2 Sessions
#Scenario: Two customers shop one after the other (server restarts between them).
# Run the complete cart flow twice — each customer adds different items, one removes something before checkout, both checkouts appear in the orders list.
@app.get("/orders")
def get_orders():
    return{
        "Orders" : orders,
        "total_orders" : len(orders)
    }

# Q Bonus Checkout with Empty Cart — Handle Gracefully
#Scenario: A bug in a mobile app sends a checkout request before the user adds any items. 
# Your API must handle this cleanly — reject it with a proper error. 
# Make sure GET /cart before the checkout shows the cart is empty, and the checkout returns the correct error.
# ---DOne above-----