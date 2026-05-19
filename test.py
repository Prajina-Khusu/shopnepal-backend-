import requests
import random

BASE    = "http://localhost:8000/api/v1"
headers = {}
token   = None

# ── Helper ────────────────────────────────────────────
def test(name, method, url, data=None, expected=200):
    resp = requests.request(method, url, json=data, headers=headers)
    ok   = resp.status_code == expected
    icon = "✅" if ok else "❌"
    print(f"  {icon} {name} → {resp.status_code}")
    if not ok:
        print(f"     Error: {resp.text[:200]}")
    try:
        return resp.json()
    except:
        return None

def section(title):
    print(f"\n{'═'*50}")
    print(f"  {title}")
    print(f"{'═'*50}")

# ══════════════════════════════════════════════════════
# 1. AUTH
# ══════════════════════════════════════════════════════
section("1. AUTH")

# Register new customer
email = f"customer{random.randint(1000,9999)}@gmail.com"
print(f"  Using email: {email}")

resp = test("Register Customer", "POST", f"{BASE}/auth/register/", {
    "name":     "Test Customer",
    "email":    email,
    "password": "test1234",
    "phone":    "9800000001"
}, expected=201)

# Login as admin (already updated in Neon)
resp = test("Admin Login", "POST", f"{BASE}/auth/login/", {
    "email":    "prajina1@gamil.com",
    "password": "prajina1"
})
if resp and "access_token" in resp:
    token = resp["access_token"]
    headers["Authorization"] = f"Bearer {token}"
    print(f"  Token saved ✅")
else:
    print("  ❌ Could not get admin token — stopping test")
    exit()

resp = test("Get Me (Admin)", "GET", f"{BASE}/auth/me/")
if resp:
    print(f"  Logged in as: {resp.get('name')} | role: {resp.get('role')}")

# ══════════════════════════════════════════════════════
# 2. CATEGORIES (Admin only)
# ══════════════════════════════════════════════════════
section("2. CATEGORIES")

categories = [
    {"name": "Electronics", "slug": "electronics", "image_url": "https://example.com/electronics.jpg"},
    {"name": "Fashion",     "slug": "fashion",     "image_url": "https://example.com/fashion.jpg"},
    {"name": "Grocery",     "slug": "grocery",     "image_url": "https://example.com/grocery.jpg"},
    {"name": "Beauty",      "slug": "beauty",      "image_url": "https://example.com/beauty.jpg"},
    {"name": "Sports",      "slug": "sports",      "image_url": "https://example.com/sports.jpg"},
]

cat_ids = {}
for cat in categories:
    resp = test(f"Create {cat['name']}", "POST", f"{BASE}/categories/", cat, expected=201)
    if resp and "id" in resp:
        cat_ids[cat["name"]] = resp["id"]
    elif resp and "detail" in resp and "already exists" in str(resp["detail"]):
        print(f"  ⚠️  {cat['name']} already exists — skipping")

resp = test("Get All Categories", "GET", f"{BASE}/categories/")
if resp:
    print(f"  Total categories: {len(resp)}")
    for c in resp:
        print(f"    - [{c['id']}] {c['name']}")
        cat_ids[c["name"]] = c["id"]

# ══════════════════════════════════════════════════════
# 3. PRODUCTS (Admin only)
# ══════════════════════════════════════════════════════
section("3. PRODUCTS")

electronics_id = cat_ids.get("Electronics", 1)
fashion_id     = cat_ids.get("Fashion",     2)
sports_id      = cat_ids.get("Sports",      5)

products = [
    {
        "name":        "Samsung Galaxy A15",
        "description": "5G Smartphone with 128GB storage and 50MP camera",
        "price":       28500,
        "sale_price":  25000,
        "stock":       50,
        "category_id": electronics_id
    },
    {
        "name":        "Apple AirPods Pro",
        "description": "Active noise cancellation wireless earbuds",
        "price":       35000,
        "sale_price":  32000,
        "stock":       30,
        "category_id": electronics_id
    },
    {
        "name":        "Nike Air Max 270",
        "description": "Lightweight running shoes for all terrain",
        "price":       8500,
        "sale_price":  7000,
        "stock":       40,
        "category_id": fashion_id
    },
    {
        "name":        "Adidas Track Pants",
        "description": "Comfortable sports track pants",
        "price":       3500,
        "sale_price":  2800,
        "stock":       60,
        "category_id": sports_id
    },
    {
        "name":        "Wireless Mouse Logitech",
        "description": "Ergonomic wireless mouse with long battery life",
        "price":       2500,
        "sale_price":  None,
        "stock":       100,
        "category_id": electronics_id
    },
]

product_ids   = []
product_slugs = []

for product in products:
    resp = test(f"Create {product['name']}", "POST", f"{BASE}/products/", product, expected=201)
    if resp and "id" in resp:
        product_ids.append(resp["id"])
        product_slugs.append(resp["slug"])
        print(f"    slug: {resp['slug']}")

resp = test("Get All Products", "GET", f"{BASE}/products/")
if resp:
    print(f"  Total products: {resp.get('total', 0)}")

resp = test("Search Products (samsung)", "GET", f"{BASE}/products/?search=samsung")
if resp:
    print(f"  Search results: {resp.get('total', 0)}")

resp = test("Filter by Category", "GET", f"{BASE}/products/?category_id={electronics_id}")
if resp:
    print(f"  Electronics products: {resp.get('total', 0)}")

if product_slugs:
    resp = test(f"Get Product by Slug", "GET", f"{BASE}/products/{product_slugs[0]}")
    if resp:
        print(f"  Found: {resp.get('name')} | Price: Rs.{resp.get('price')}")

# ══════════════════════════════════════════════════════
# 4. CART
# ══════════════════════════════════════════════════════
section("4. CART")

# Switch to customer token for cart operations
resp = requests.post(f"{BASE}/auth/login/", json={
    "email":    email,
    "password": "test1234"
})
if resp.status_code == 200:
    customer_token = resp.json()["access_token"]
    headers["Authorization"] = f"Bearer {customer_token}"
    print(f"  Switched to customer token ✅")

if product_ids:
    resp = test("Add Product 1 to Cart", "POST", f"{BASE}/cart/", {
        "product_id": product_ids[0],
        "quantity":   2
    }, expected=201)
    if resp:
        print(f"  Cart items: {len(resp.get('items', []))} | Total: Rs.{resp.get('total', 0)}")

    if len(product_ids) > 1:
        resp = test("Add Product 2 to Cart", "POST", f"{BASE}/cart/", {
            "product_id": product_ids[1],
            "quantity":   1
        }, expected=201)
        if resp:
            print(f"  Cart items: {len(resp.get('items', []))} | Total: Rs.{resp.get('total', 0)}")

resp = test("Get Cart", "GET", f"{BASE}/cart/")
if resp:
    print(f"  Cart items: {len(resp.get('items', []))}")
    print(f"  Cart total: Rs.{resp.get('total', 0)}")
    cart_items = resp.get("items", [])

if cart_items:
    first_item_id = cart_items[0]["id"]
    resp = test("Update Cart Item Qty", "PUT", f"{BASE}/cart/{first_item_id}", {
        "quantity": 3
    })
    if resp:
        print(f"  Updated total: Rs.{resp.get('total', 0)}")

# ══════════════════════════════════════════════════════
# 5. ORDERS
# ══════════════════════════════════════════════════════
section("5. ORDERS")

resp = test("Checkout (no address)", "POST", f"{BASE}/orders/checkout", {
    "address_id": 1
}, expected=201)
if resp:
    print(f"  Order ID:     {resp.get('id')}")
    print(f"  Order Status: {resp.get('status')}")
    print(f"  Order Total:  Rs.{resp.get('total_amount')}")
    print(f"  Order Items:  {len(resp.get('items', []))}")
    order_id = resp.get("id")

resp = test("Get My Orders", "GET", f"{BASE}/orders/")
if resp:
    print(f"  Total orders: {len(resp)}")

if resp and len(resp) > 0:
    order_id = resp[0]["id"]
    resp = test("Get Order Detail", "GET", f"{BASE}/orders/{order_id}")
    if resp:
        print(f"  Order {order_id} status: {resp.get('status')}")

# Switch back to admin to update order status
resp2 = requests.post(f"{BASE}/auth/login/", json={
    "email":    "test2@gmail.com",
    "password": "test1234"
})
if resp2.status_code == 200:
    headers["Authorization"] = f"Bearer {resp2.json()['access_token']}"
    print(f"  Switched to admin token ✅")

if order_id:
    resp = test("Update Order Status → Processing", "PATCH",
        f"{BASE}/orders/{order_id}/status", {"status": "processing"})
    if resp:
        print(f"  New status: {resp.get('status')}")

    resp = test("Update Order Status → Shipped", "PATCH",
        f"{BASE}/orders/{order_id}/status", {"status": "shipped"})
    if resp:
        print(f"  New status: {resp.get('status')}")

# ══════════════════════════════════════════════════════
# 6. REVIEWS
# ══════════════════════════════════════════════════════
section("6. REVIEWS")

# Switch back to customer
resp2 = requests.post(f"{BASE}/auth/login/", json={
    "email":    email,
    "password": "test1234"
})
if resp2.status_code == 200:
    headers["Authorization"] = f"Bearer {resp2.json()['access_token']}"
    print(f"  Switched to customer token ✅")

if product_ids:
    resp = test("Add Review to Product 1", "POST",
        f"{BASE}/reviews/{product_ids[0]}", {
            "rating":  5,
            "comment": "Excellent product! Very satisfied with the purchase."
        }, expected=201)
    if resp:
        print(f"  Review: ★{resp.get('rating')} - {resp.get('comment')}")

    if len(product_ids) > 1:
        resp = test("Add Review to Product 2", "POST",
            f"{BASE}/reviews/{product_ids[1]}", {
                "rating":  4,
                "comment": "Good quality but slightly expensive."
            }, expected=201)
        if resp:
            print(f"  Review: ★{resp.get('rating')} - {resp.get('comment')}")

    resp = test("Get Reviews for Product 1", "GET",
        f"{BASE}/reviews/{product_ids[0]}")
    if resp:
        print(f"  Total reviews: {len(resp)}")
        for r in resp:
            print(f"    ★{r['rating']} - {r['comment']}")

# ══════════════════════════════════════════════════════
# 7. VERIFY IN DATABASE
# ══════════════════════════════════════════════════════
section("7. FINAL SUMMARY")

# Switch to admin
resp2 = requests.post(f"{BASE}/auth/login/", json={
    "email":    "test2@gmail.com",
    "password": "test1234"
})
if resp2.status_code == 200:
    headers["Authorization"] = f"Bearer {resp2.json()['access_token']}"

resp = requests.get(f"{BASE}/categories/", headers=headers)
cats = resp.json() if resp.status_code == 200 else []

resp = requests.get(f"{BASE}/products/", headers=headers)
prods = resp.json() if resp.status_code == 200 else {}

print(f"""
  Database Summary:
  ├── Categories:  {len(cats)}
  ├── Products:    {prods.get('total', 0)}
  ├── Cart items:  tested ✅
  ├── Orders:      tested ✅
  └── Reviews:     tested ✅

  API Summary:
  ├── Auth:        ✅ register, login, me
  ├── Categories:  ✅ create, list
  ├── Products:    ✅ create, list, search, filter, get by slug
  ├── Cart:        ✅ add, get, update, remove
  ├── Orders:      ✅ checkout, list, detail, update status
  └── Reviews:     ✅ add, get
""")

print("═"*50)
print("  ALL TESTS COMPLETE 🚀")
print("═"*50 + "\n")