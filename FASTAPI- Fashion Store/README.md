#  FastAPI Fashion Store Backend

A backend application built using FastAPI that simulates a real-world fashion e-commerce platform. This project was developed as part of my FastAPI internship to demonstrate API design, backend logic, and multi-step workflow handling.

---

## 🚀 Project Overview

This application provides REST APIs to manage fashion products, handle wishlist operations, process orders, and perform advanced operations like search, sorting, and pagination.

All endpoints are tested and verified using Swagger UI.

---

## ✨ Features

### 🛍️ Product Management
- View all products with stock count
- Get product details by ID
- Add new products with validation
- Update product price and stock status
- Delete products with business rules

### ❤️ Wishlist & Order Workflow
- Add items to wishlist (with size selection)
- View wishlist with grand total
- Remove items from wishlist
- Order all wishlist items in one step
- Store and retrieve order history

### 💰 Pricing & Discounts
- Base price calculation
- 15% Season Sale discount
- 5% Bulk discount (quantity ≥ 5)
- Gift wrap charges (₹50 per item)
- Full price breakdown in every order

### 🔍 Advanced Functionality
- Search products (name, brand, category — case-insensitive)
- Sort products by price, name, brand, or category
- Pagination for products and orders
- Combined browse endpoint (search + filter + sort + pagination)

---

## 🛠️ Tech Stack

- 🐍 Python
- ⚡ FastAPI
- 📦 Pydantic
- 🚀 Uvicorn

---

## ▶️ How to Run

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Server
```bash
uvicorn main:app --reload
```

### 3️⃣ Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## 📸 API Testing

All endpoints are tested using Swagger UI. Screenshots of all API responses are included in the `screenshots/` folder.

---

## 📌 Key Highlights

- Clean API structure with route ordering (static routes before dynamic)
- Proper input validation using Pydantic (`Field`, `Query`)
- Full CRUD implementation for products
- Multi-step workflow (Wishlist → Order → Order History)
- Advanced APIs with search, filtering, sorting, and pagination
- Helper functions for clean, reusable logic

---

## ⚠️ Notes

- Data is stored in-memory (resets when server restarts)
- This project focuses on backend logic and API design

---

## 📎 Repository Structure

```
fastapi-fashion-store/
│
├── main.py
├── README.md
├── requirements.txt
└── screenshots/
```

## 🎯 Conclusion

This project demonstrates practical backend development using FastAPI, covering all essential concepts from basic CRUD APIs to advanced filtering, discounts, and multi-step workflows. 
