from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook',       'price':  99, 'category': 'Stationery',  'in_stock': True},
    {'id': 3, 'name': 'USB Hub',        'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',        'price':  49, 'category': 'Stationery',  'in_stock': True},
]

orders = []
order_counter = 1

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# Q1. Test the Search Endpoint
#Scenario: A customer on the app types different words in the search box. 
# Test GET /products/search with all the cases below and write down exactly what you see for each one.

# ────────── Search by keyword ────────────────────
@app.get('/products/search')
def search_products(
    keyword: str = Query(..., description='Word to search for'),
):
    results = [p for p in products  if keyword.lower() in p['name'].lower()]

    if not results:
        return {'message': f'No products found for: {keyword}', 'results': []}
    
    return {
        'keyword':     keyword,
        'total_found': len(results),
        'results':     results,
    }
#Q2. Test All Sort Combinations
#Scenario: The app has a "Sort By" dropdown with 4 options — Price Low to High, Price High to Low, Name A to Z, Name Z to A. 
# Test all 4 using GET /products/sort and note what the first product is in each case.
# ────────── Sort by price or name ─────────────
@app.get('/products/sort')
def sort_products(
    sort_by: str = Query('price', description='price or name'),
    order:   str = Query('asc',   description='asc or desc'),
):
    if sort_by not in ['price', 'name']:
        return {'error': "sort_by must be 'price' or 'name'"}
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    reverse         = (order == 'desc')
    sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=reverse)
    return {
        'sort_by':  sort_by,
        'order':    order,
        'products': sorted_products,
    }
 #Q3. Navigate Pages Like a Real User
#Scenario: A user opens the shop. The app shows 2 products per page — like a catalogue. 
# The user clicks Next, then Next again. Test GET /products/page and navigate through all the pages.
# ────────── Pagination ────────────────────
@app.get('/products/page')
def get_products_paged(
    page:  int = Query(1, ge=1,  description='Page number'),
    limit: int = Query(2, ge=1, le=20, description='Items per page'),
):
    start = (page - 1) * limit
    end   = start + limit
    paged = products[start:end]
    return {
        'page':        page,
        'limit':       limit,
        'total':       len(products),
        'total_pages': -(-len(products) // limit),   # ceiling division
        'products':    paged,
    }


#Q6. Search + Sort + Paginate in One Endpoint
# Scenario: Real shopping APIs don't have 3 separate endpoints — they combine everything into one smart endpoint. 
# Build GET /products/browse that can search by keyword, sort results, AND paginate — all in one call, all params optional.
@app.get("/products/browse")
def browse_product(
    keyword : str = Query(None) ,
    sort_by :str = Query("price"), 
    order : str = Query("asc"), 
    page :  int = Query(1,ge=1), 
    limit : int = Query(4,ge=1,le=20)
):
    #search
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]
    
    # Sort
    if sort_by in ["name" , "price"]:
        result = sorted(result,key = lambda p:(p['name'],p['price']))
    
    # Pagination
    total = len(result)
    start = (page - 1 )* limit
    end = start + limit
    paged = result[start:end]

    return { 
      'keyword': keyword, 
      'sort_by': sort_by, 
      'order': order, 
      'page': page, 
      'limit': limit, 
      'total_found': total, 
      'total_pages': -(- total // limit), 
      'products': paged 
    }


#Q4. Search the Orders List
#Scenario: The store manager wants to look up all orders placed by a specific customer. 
# Build GET /orders/search that searches orders by customer name and returns all matching orders.
@app.post("/orders")
def create_order(customer_name : str = Query(...)):
    global order_counter
    order = {
        "order_id" : order_counter, 
        "customer_name" : customer_name
    }

    orders.append(order)
    order_counter +=1

    return{
        "message" : "Order placed Successfully",
        "order" : order
    }

# Search orders by customer name
@app.get('/orders/search') 
def search_orders(customer_name: str = Query(...)): 
    results = [ o for o in orders if customer_name.lower() in o['customer_name'].lower() ] 
    if not results: 
        return {'message': f'No orders found for: {customer_name}'} 
    return {
        'customer_name': customer_name, 
        'total_found': len(results), 
         'orders': results
    }

#Q5. Sort Products by Category Then Price
#Scenario: The admin wants to see all products grouped by category — but within each category, cheapest first. 
# The existing /products/sort only sorts by one field. 
# Build GET /products/sort-by-category that first groups by category alphabetically, then sorts by price within each group.
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key = lambda p: (p['category'],p['price']))
    return{
        "products" : result,
        "total" : len(result)
    }

#Q6 .Bonus  Paginate the Orders List
#Scenario: The orders list keeps growing. 
# Build GET /orders/page so the admin can browse orders in pages — same pagination logic as products, applied to the orders list.
@app.get('/orders/page') 
def get_orders_paged( 
    page: int = Query(1, ge=1), 
    limit: int = Query(3, ge=1, le=20)
): 
    start = (page - 1) * limit 
    end = start + limit
    return { 
        'page': page, 
        'limit': limit, 
        'total': len(orders), 
        'total_pages': -(-len(orders) // limit), 
        'orders': orders[start : end ] 
    }