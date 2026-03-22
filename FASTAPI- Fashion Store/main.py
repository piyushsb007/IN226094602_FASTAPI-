from fastapi import FastAPI,Query,status,HTTPException,Response
from pydantic import BaseModel,Field
from collections import Counter
from typing import List

app = FastAPI(description = "Fashion Store")
# =======================================================
#                   Product Data
# =======================================================
products =  [
        {
            "id": 1,
            "name": "Classic Oxford Shirt",
            "brand": "Allen Solly",
            "category": "Shirt",
            "price": 789,
            "sizes_available": ["S", "M", "L", "XL"],
            "in_stock": True
        },
        {
            "id": 2,
            "name": "Slim Fit Blue Jeans",
            "brand": "JaiHind",
            "category": "Jeans",
            "price": 979,
            "sizes_available": ["M", "L", "XL"],
            "in_stock": True
        },
        {
            "id": 3,
            "name": "Air Runner Sneakers",
            "brand": "Nike",
            "category": "Shoes",
            "price": 1120,
            "sizes_available": ["M", "L"],
            "in_stock": False
        },
        {
            "id": 4,
            "name": "Floral Summer Dress",
            "brand": "Zara",
            "category": "Dress",
            "price": 695,
            "sizes_available": ["S", "M", "L"],
            "in_stock": True
        },
        {
            "id": 5,
            "name": "Denim Trucker Jacket",
            "brand": "JaiHind",
            "category": "Jacket",
            "price": 1110,
            "sizes_available": ["M", "L", "XL"],
            "in_stock": True
        },
        {
            "id": 6,
            "name": "Casual Linen Shirt",
            "brand": "H&M",
            "category": "Shirt",
            "price": 845,
            "sizes_available": ["S", "M", "L"],
            "in_stock": False
        }
    ]

# =======================================================
#                   Request Model
# =======================================================
class OrderRequest(BaseModel): #task 6
    customer_name: str = Field(...,min_length = 2 , max_length = 100)
    product_id: int = Field(...,gt=0) 
    size: str = Field(...,min_length=1) 
    quantity: int = Field(...,gt=0,le=10)
    delivery_address: str = Field(...,min_length = 10)
    gift_wrap: bool = Field(default= False)
    season_sale: bool = Field(default = False)

class NewProduct(BaseModel): #task 11
    name : str = Field(...,min_length = 2) 
    brand : str = Field(...,min_length = 2) 
    category : str = Field(...,min_length = 2)
    price : int = Field(...,gt=0)
    sizes_available : List[str] 
    in_stock: bool = True

# =======================================================
#                   Helper Function
# =======================================================

def find_product(product_id):
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_order_total(price, quantity,gift_wrap,season_sale): #task 7
    base_price = price * quantity
    total = base_price

    season_discount = 0
    gift_wrap_charges = 0
    bulk_discount = 0

    # season_sale, APPLY 15% off
    if season_sale :
        season_discount = base_price*0.15
        total = base_price - season_discount 
    #add gift_wrap cost
    if gift_wrap:
        gift_wrap_charges = quantity*50
        total = base_price + gift_wrap_charges
    # Apply Discount 5%
    if quantity >= 5:
        bulk_discount = base_price*0.05
        total = base_price - bulk_discount

    return {
        "message" : "All discounts and Price Breakdown",
        "base_price" : base_price ,
        "season_discount" : round(season_discount,2),
        "bulk_discount" : round(bulk_discount,2),
        "gift_wrap_charges" : gift_wrap_charges,
        "Total" : total
    }

def filter_products_logic(category=None,brand=None,max_price=None,in_stock=None): # task10  
    result = products

    if category is not None:
        result = [p for p in products if p["category"] == category]
    if brand is not None:
        result = [p for p in products if p["brand"] == brand]
    if max_price is not None:
        result = [p for p in products if p["price"] <= max_price]
    if in_stock is not None:
        result = [p for p in products if p["in_stock"] == in_stock]
    
    return result

# ============================================================
#              DAY 1 — GET APIs
# ============================================================

# Task 1:- Add GET / returning {\'message\': \'Welcome to TrendZone Fashion Store\'}.
@app.get("/")
def home():
    return {
        "message" : "Welcome to TendZone Fashion Store"
    }

# Task 2 :- Create a products list with at least 6 clothing items: id, name, brand, category (Shirt/Jeans/Shoes/Dress/Jacket), price (int), sizes_available 
# (list of str e.g. [\'S\',\'M\',\'L\']), in_stock (bool). Build GET /products returning all products, total, and in_stock_count.
@app.get("/products")
def get_all_products():
    
    in_stock = [p for p in products if p["in_stock"] == True]

    return {
        "product" : products , 
        "total":len(products),
        "in_stock_count" : len(in_stock)
    }

# Task 5 :- Build GET /products/summary (above /products/{product_id}). 
# Return: total products, in-stock count, out-of-stock count, brands list (unique), and count per category.
@app.get("/products/summary")
def get_summary():
    in_stock = [p for p in products if p['in_stock']]
    out_stock = [p for p in products if not p['in_stock']]
    brands = {p["brand"] for p in products}
    category = Counter(p["category"] for p in products)
    return {
        # "products" : products, 
        "total_products" : len(products),
        "in_stock_count" : len(in_stock) ,
        "out_stock_count" : len(out_stock) , 
        "brands" : list(brands),
        "category_count" : dict(category)
    }

# Task 10 :- Build GET /products/filter with optional params: category (str), brand (str), max_price (int), in_stock (bool). 
# Use filter_products_logic() helper. All checks use is not None.
@app.get("/products/filter")
def get_filter_products(
    category : str = Query(None) ,
    brand : str = Query(None) ,
    max_price : int = Query(None) ,
    in_stock : bool = Query(None) 
):
    filter_products = filter_products_logic(category,brand,max_price,in_stock)
    return {
        "Filter_products" : filter_products , "count" : len(filter_products)
    }

# Task 16:-Build GET /products/search with required param keyword (str). 
# Search across name, brand, AND category, case-insensitive. 
# Return matches and total_found. If no results, return a friendly message.
@app.get("/products/search")
def search_products(
   keyword : str
):
    result = [p for p in products if (keyword.lower() in p["name"].lower() or keyword.lower() in p["category"].lower() or keyword.lower() in p["brand"].lower())]

    if not result:
        return {
            "message" : f"No product Found for: {keyword} , 'result' : []"
        }
    return {
        "keyword" : keyword,
        "total_found" : len(result),
        "results" : result
    }

# Task 17:- Build GET /products/sort — allow sort_by: price, name, brand, category. Default: sort by price ascending. 
# Validate both params. Return sorted list with sort metadata.
@app.get("/products/sort")
def sort_products(
    sort_by : str = Query('price',description = "Sort by name or brand or category"),
    order : str = Query('asc' , description = "asc or desc")
):
    if sort_by not in ["price" , "name" , "brand" , "category"]:
        return {'error' : "sort_by must be name or brand or category"}            
    if order not in ["asc" , "desc"]:
        return {'error' : "order must be asc or desc"}            
    reverse = (order == "desc")
    sorted_product = sorted(products,key= lambda p:p[sort_by] , reverse = reverse)

    return{
        "sort_by" : sort_by,
        "order" : order,
        "sorted_products" : sorted_product
    }

# Task 18:- Build GET /products/page with page (default 1) and limit (default 3). 
# Full pagination formula with total_pages. Test all pages.
@app.get("/products/page")
def products_paged(
    page  : int = Query(1,ge=1, description = "Page Number") ,
    limit  : int = Query(3,ge=1 ,description = "Item per Page") 
):
    start = (page -1) * limit
    end = start + limit
    paged = products[start:end]

    return{
        "page" : page ,
        "limit" : limit,
        "total" : len(products),
        "total_pages" : -(-len(products) // limit),
        "products" : paged
    }


# Task 20:- Build GET /products/browse combining: optional keyword, category filter, brand filter, in_stock filter, max_price filter, sort_by, order, page, limit. 
# Apply all filters first, then sort, then paginate. Return full metadata and results.
@app.get("/products/browse")
def browse_all_products(
    keyword : str = Query(None),
    category : str = Query(None),
    brand : str = Query(None),
    in_stock : str = Query(None),
    max_price : int = Query(None),
    sort_by : str = Query("price",description = "sort_by price , name , brand , category "),
    order : str = Query("asc" ,description = "order by asc or desc"),
    page : int = Query(1, ge=1),
    limit : int = Query(3, ge=1)
):
    filtered = products.copy()
    # Search n Filter
    if keyword:
        filtered = [p for p in filtered if keyword.lower() in p["name"].lower()]
    
    if category:
        filtered = [p for p in filtered if category.lower() == p["category"].lower()]
    
    if brand:
        filtered = [p for p in filtered if brand.lower() == p["brand"].lower()]

    if in_stock is not None:
        filtered = [p for p in filtered if in_stock == p["in_stock"]]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    # Sorting
    if order.lower() == "desc":
        reverse = True
    else:
        reverse = False
    
    if sort_by in ["price","name","brand","category"]:
        filtered.sort(key= lambda x:x[sort_by] , reverse=reverse)
    
    # Pagination
    total_items = len(filtered)
    start = (page -1 )* limit
    end = start + limit

    paged = filtered[start:end]

    return{
        "total_items" : total_items,
        "page" : page,
        "limit" : limit,
        "total_pages" : -(-total_items // limit),
        "results" : paged
    }


# Task 3 :- Build GET /products/{product_id}. Return the product or an error. Test both.
@app.get("/products/{product_id}")
def get_product(product_id : int):

    product = find_product(product_id)

    if not product:
        raise HTTPException(status_code = 404 , detail = "Product not Found")
    return {"product" : product }

# ============================================================
#              DAY 1 — ORDERS GET APIs + Storage
# ============================================================

# Task 4 :- Create orders = [] and order_counter = 1. Build GET /orders returning all orders, total, and total_revenue.

wishlist = [] # task 14
orders = []
order_counter = 1

# Order Storage
@app.get("/orders")
def get_orders():
    total_orders = len(orders)
    # total_revenue = sum(o["price"] for o in orders)

    return{
        "orders" : orders ,
        "total_order" : total_orders,
        # "total_revenue" : total_revenue
    }

# ============================================================
#              DAY 2 — POST + PYDANTIC (Orders)
# ============================================================

# Task 6:- Create OrderRequest: customer_name (min 2), product_id (gt 0), size (str, min 1), quantity (gt 0, le 10),
# delivery_address (min 10), gift_wrap (bool, default False). Test: send quantity=0 and confirm rejection.
# --done--
# Task 7:- Write find_product(product_id) helper. Write calculate_order_total(price, quantity, gift_wrap) — add ₹50 per item if gift_wrap=True. 
#Also apply a 5% bulk discount if quantity >= 5. Show breakdown. Plain functions.
@app.get("/test-total")
def test_total(price:int , quantity:int , gift_wrap : bool = False):
    total = calculate_order_total(price,quantity,gift_wrap)
    return {"Final total": total}

# Task 8:- Build POST /orders. Check product exists. Check in_stock. 
# Check that the requested size is in sizes_available — if not, return an error listing the available sizes. Use calculate_order_total(). 
# Return order with order_id, product name, brand, size, quantity, gift_wrap, and total. 
@app.post("/orders")
def placed_order(order: OrderRequest):
    global order_counter
    product = find_product(order.product_id)
    if not product:
        raise HTTPException(status_code = 404 , detail = "Product Not Found")
    if not product["in_stock"]:
        raise HTTPException(status_code = 400 , detail= f"{product['name']} not in Stock" )
    if order.size.upper() not in product['sizes_available']:
        raise HTTPException(status_code = 400 , detail = f" Size not Available, Available sizes:- {product["sizes_available"]} " )
    
    total_order = calculate_order_total(product['price'],order.quantity,order.gift_wrap,order.season_sale)

    new_order = {
        "order_id" : order_counter ,
        "customer_name": order.customer_name, 
        "product_name" : product["name"],
        "brand" : product["brand"] ,
        "size" : order.size.upper(), 
        "quantity" : order.quantity, 
        "gift_wrap" : order.gift_wrap,
        "total" : total_order,
        "total_cost" : total_order["Total"]
    }
    
    orders.append(new_order)
    order_counter += 1

    return {"order" : new_order}

# Task 9:- Add a season_sale field (bool, default False) to OrderRequest. - done
# Modify calculate_order_total() — if season_sale=True apply 15% off before gift wrap charge and bulk discount. 
# Show all discounts separately in the response. 
# --Done--

# ============================================================
#              DAY 4 — CRUD OPERATIONS (Products)
# ============================================================

# Task 11 :- Create NewProduct model: name (min 2), brand (min 2), category (min 2), price (gt 0), sizes_available (list of str), in_stock (default True). 
# Build POST /products — reject if name+brand combo already exists. Return with status 201.
@app.post("/products")
def newproducts(newproduct: NewProduct):

    for p in products:
        if p['name'].lower() == newproduct.name.lower() and p["brand"].lower() == newproduct.brand.lower():
            raise HTTPException(
            status_code=400,
            detail="Product with same name and brand already exists"
        )
   # Create new product
    product_id = len(products) + 1

    new_product = {
        "id": product_id,
        **newproduct.model_dump()
        # "name": newproduct.name,
        # "brand": newproduct.brand,
        # "category": newproduct.category,
        # "price": newproduct.price,
        # "sizes_available": newproduct.sizes_available,
        # "in_stock": newproduct.in_stock
    }
    products.append(new_product)
    return new_product

# Task 12 :- Build PUT /products/{product_id} with optional query params price (int) and in_stock (bool). Return 404 if not found. Apply only non-None updates.
@app.put("/products/{product_id}")
def update_products(product_id: int , price:int = Query(None), in_stock:bool = Query(None)):
    product = find_product(product_id)

    if not product:
        raise HTTPException(status_code = 404 , detail= "Product Not Found")
    
    if price is not None:
        product["price"] = price
    if in_stock is not None:
        product["in_stock"] = in_stock
    
    return {
        "message" : "Product Updated" ,
        "product" : product
    }

# Task 13 :- Build DELETE /products/{product_id}. Return 404 if not found.
# If the product has any orders in the orders list, return an error — cannot delete a product with order history. Otherwise delete.
@app.delete("/products/{product_id}")
def delete_product(product_id : int):
    product = find_product(product_id)

    if not product:
        raise HTTPException(status_code = 404 , detail= "Product Not Found")
    products.remove(product)
    return {"message" : f"Product '{product["name"]}' deleted"}

# ============================================================
#              DAY 5 — MULTI-STEP WORKFLOW (Wishlist → Order)
# ============================================================

# Task 14 :- Build a wishlist. Add wishlist = []. 
# Build POST /wishlist/add (query params: customer_name, product_id, size) — check product exists and size is valid. 
# Don\'t allow the same customer+product+size combo twice. 
# Build GET /wishlist returning wishlist items and total wishlist value.
@app.post("/wishlist/add")
def add_to_wishlist(
    customer_name : str ,
    product_id : int ,
    size : str
):
    product = find_product(product_id)
    # check product exists
    if not product:
        raise HTTPException(status_code = 404 , detail= "Product Not Found")
    # check size is valid
    if size not in product['sizes_available']:
         raise HTTPException(status_code = 400 , detail = f" Size not Available, Available sizes:- {product["sizes_available"]} " )
    # Prevent duplicates(customer+product+size)
    for item in wishlist:
        if (item["customer_name"].lower() == customer_name.lower() and item['product_id'] == product_id and item['size'].lower()==size.lower()):
            raise HTTPException(status_code = 400 , detail = "Item already in Wishlist")
    #Add to wishlist 
    wishlist_item = {
        "customer_name" : customer_name ,
        "product_id" : product_id ,
        "product_name" : product["name"],
        "brand" : product["brand"] ,
        "price": product["price"],
        "size" : size
    }

    wishlist.append(wishlist_item)
    
    return{
        "message" : "Item added to Wishlist Successfully",
        "Wishlist_items" : wishlist_item
    }    
@app.get("/wishlist")
def get_wishlist():
    if not wishlist:
        return {"message" : "Wishlist is Empty" , "items" : [] , "grand_total": 0 }
    
    return{
        "Wishlist" : wishlist,
        "item_counts" : len(wishlist),
        "grand_total" : sum(p["price"] for p in wishlist)
    }


# Task 15:-Build DELETE /wishlist/remove (query params: customer_name, product_id). 
# Build POST /wishlist/order-all — request body with customer_name, delivery_address. 
# Loop all wishlist items for that customer, place an order for each, collect confirmations, 
# clear their wishlist entries, return all orders and grand total with status 201.
@app.delete("/wishlist/remove")
def remove_from_wishlist(
    customer_name : str,
    product_id : int
):
    for item in wishlist:
        if item["product_id"] == product_id:
            wishlist.remove(item)
            return {"message" : f"{item['product_name']} is removed from Wishlist"}
    return  {
        "error" : "Item not in Wishlist"
    }
@app.post("/wishlist/order-all")
def order_all(
    customer_name : str,
    delivery_address : str,
    response : Response
):
    global order_counter

    if not wishlist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Wishlist is empty'}
    
    placed_order = []

    grand_total = 0

    for item in wishlist:
        order = {
            "order_id" : order_counter,
            "customer_name" : customer_name,
            "product_id" : item["product_id"],
            "product_name" : item["product_name"],
            "brand" : item["brand"],
            "price" : item["price"],
            "delivery_address" : delivery_address,
        }
        order_counter +=1
        orders.append(order)
        placed_order.append(order)
        grand_total += item["price"]

    wishlist.clear()
     
    response.status_code = status.HTTP_201_CREATED

    return{
        "message" : "Order Successful",
        "All_orders" : placed_order,
        "Grand_total" : grand_total
    }

# ============================================================
#              DAY 6 — ADVANCED APIs (Orders)
# ============================================================

# Task 19:- Build GET /orders/search — search by customer_name. 
# Build GET /orders/sort — sort by total_cost or quantity. 
# Build GET /orders/page — paginate orders. All above any variable order routes.
@app.get("/orders/search")
def search_order(customer_name : str = Query(...)):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not result :
        return {"message" : f"No order Found in {customer_name}"}
    
    return {
        "customer_name" : customer_name,
        "total_found" : len(result) ,
        "orders" : result
    }

@app.get("/orders/sort")
def orders_sort(
    sort_by : str = Query(...,description= "sort by total_cost or quantity"),
    order : str = Query("desc",description = "order asc or  desc")
):
    if sort_by not in ["total_cost" , "quantity"]:
         return {'error' : "sort_by must be total_cost or quantity "}            
    if order not in ["asc" , "desc"]:
        return {'error' : "order must be asc or desc"}  
    
    reverse =  ( order == "desc")
    sorted_orders = sorted(orders,key = lambda p:p.get(sort_by, 0),reverse = reverse)
    return {
        "sort_by" : sort_by,
        "order" : order,
        "total_orders": len(sorted_orders),
        "orders": sorted_orders
    }

@app.get("/orders/page")
def order_page(
    page  : int = Query(1,ge=1, description = "Page Number") ,
    limit  : int = Query(3,ge=1 ,description = "Item per Page") 
):
    start = (page - 1) * limit
    end = start + limit
    paged = orders[start:end]

    return{
        "page" : page,
        "limit" : limit,
        "total" : len(orders),
        "total_pages" : -(-len(orders) // limit),
        "orders" : paged
    }
