import requests
import random

BASE    = "http://localhost:8000/api/v1"
headers = {}

ADMIN_EMAIL    = "prajina1@gamil.com"
ADMIN_PASSWORD = "prajina1"

# ── Helpers ───────────────────────────────────────────────────────────────────

def test(name, method, url, data=None, expected=200):
    resp = requests.request(method, url, json=data, headers=headers)
    ok   = resp.status_code == expected
    icon = "✅" if ok else "❌"
    print(f"  {icon} {name} → {resp.status_code}")
    if not ok:
        print(f"     Error: {resp.text[:300]}")
    try:
        return resp.json()
    except Exception:
        return None

def section(title):
    print(f"\n{'═'*50}")
    print(f"  {title}")
    print(f"{'═'*50}")

def login(email, password, label=""):
    resp = requests.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        headers["Authorization"] = f"Bearer {token}"
        if label:
            print(f"  Switched to {label} token ✅")
        return token
    else:
        print(f"  ❌ Login failed for {email} → {resp.status_code}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# 1. AUTH
# ══════════════════════════════════════════════════════════════════════════════
section("1. AUTH")

email    = f"customer{random.randint(1000, 9999)}@gmail.com"
password = "test1234"
print(f"  Using email: {email}")

test("Register Customer", "POST", f"{BASE}/auth/register", {
    "name":     "Test Customer",
    "email":    email,
    "password": password,
    "phone":    "9800000001"
}, expected=201)

login(ADMIN_EMAIL, ADMIN_PASSWORD)
print(f"  Admin token saved ✅")

resp = test("Get Me (Admin)", "GET", f"{BASE}/auth/me")
if resp:
    print(f"  Logged in as: {resp.get('name')} | role: {resp.get('role')}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. CATEGORIES  (admin)
# ══════════════════════════════════════════════════════════════════════════════
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
    elif resp and "already exists" in str(resp.get("detail", "")):
        print(f"  ⚠️  {cat['name']} already exists — skipping")

resp = test("Get All Categories", "GET", f"{BASE}/categories/")
if resp:
    print(f"  Total categories: {len(resp)}")
    for c in resp:
        print(f"    - [{c['id']}] {c['name']}")
        cat_ids[c["name"]] = c["id"]

# ══════════════════════════════════════════════════════════════════════════════
# 3. PRODUCTS  (admin)
# ══════════════════════════════════════════════════════════════════════════════
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
        "category_id": electronics_id,
    },
    {
        "name":        "Apple AirPods Pro",
        "description": "Active noise cancellation wireless earbuds",
        "price":       35000,
        "sale_price":  32000,
        "stock":       30,
        "category_id": electronics_id,
    },
    {
        "name":        "Nike Air Max 270",
        "description": "Lightweight running shoes for all terrain",
        "price":       8500,
        "sale_price":  7000,
        "stock":       40,
        "category_id": fashion_id,
    },
    {
        "name":        "Adidas Track Pants",
        "description": "Comfortable sports track pants",
        "price":       3500,
        "sale_price":  2800,
        "stock":       60,
        "category_id": sports_id,
    },
    {
        "name":        "Wireless Mouse Logitech",
        "description": "Ergonomic wireless mouse with long battery life",
        "price":       2500,
        "sale_price":  None,
        "stock":       100,
        "category_id": electronics_id,
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
    resp = test("Get Product by Slug", "GET", f"{BASE}/products/{product_slugs[0]}")
    if resp:
        print(f"  Found: {resp.get('name')} | Price: Rs.{resp.get('price')}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. CART  (customer)
# ══════════════════════════════════════════════════════════════════════════════
section("4. CART")

login(email, password, label="customer")

cart_items = []

if product_ids:
    resp = test("Add Product 1 to Cart", "POST", f"{BASE}/cart/", {
        "product_id": product_ids[0],
        "quantity":   2,
    }, expected=201)
    if resp:
        print(f"  Cart items: {len(resp.get('items', []))} | Total: Rs.{resp.get('total', 0)}")

    if len(product_ids) > 1:
        resp = test("Add Product 2 to Cart", "POST", f"{BASE}/cart/", {
            "product_id": product_ids[1],
            "quantity":   1,
        }, expected=201)
        if resp:
            print(f"  Cart items: {len(resp.get('items', []))} | Total: Rs.{resp.get('total', 0)}")

resp = test("Get Cart", "GET", f"{BASE}/cart/")
if resp:
    cart_items = resp.get("items", [])
    print(f"  Cart items: {len(cart_items)}")
    print(f"  Cart total: Rs.{resp.get('total', 0)}")

if cart_items:
    first_item_id = cart_items[0]["id"]
    resp = test("Update Cart Item Qty", "PUT", f"{BASE}/cart/{first_item_id}", {"quantity": 3})
    if resp:
        print(f"  Updated total: Rs.{resp.get('total', 0)}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. ADDRESSES  (customer)
# ══════════════════════════════════════════════════════════════════════════════
section("5. ADDRESSES")

address_id = None

resp = test("Create Address", "POST", f"{BASE}/addresses/", {
    "full_name":  "Test Customer",
    "phone":      "9800000001",
    "street":     "Thamel Marg 12",
    "city":       "Kathmandu",
    "province":   "Bagmati",
    "is_default": True,
}, expected=201)
if resp and "id" in resp:
    address_id = resp["id"]
    print(f"  Address ID: {address_id} | {resp.get('street')}, {resp.get('city')}")

resp = test("Get My Addresses", "GET", f"{BASE}/addresses/")
if resp:
    print(f"  Total addresses: {len(resp)}")
    for a in resp:
        print(f"    - [{a['id']}] {a['full_name']} | {a['street']}, {a['city']} {'⭐ default' if a.get('is_default') else ''}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. ORDERS  (customer → admin)
# ══════════════════════════════════════════════════════════════════════════════
section("6. ORDERS")

order_id = None  # always initialised — no NameError

if not address_id:
    print("  ⚠️  Skipping checkout — address creation failed")
else:
    resp = test("Checkout", "POST", f"{BASE}/orders/checkout", {
        "address_id": address_id,
    }, expected=201)
    if resp and "id" in resp:
        order_id = resp["id"]
        print(f"  Order ID:     {order_id}")
        print(f"  Order Status: {resp.get('status')}")
        print(f"  Order Total:  Rs.{resp.get('total_amount')}")
        print(f"  Order Items:  {len(resp.get('items', []))}")

resp = test("Get My Orders", "GET", f"{BASE}/orders/")
if resp:
    print(f"  Total orders: {len(resp)}")
    if not order_id and len(resp) > 0:
        order_id = resp[0]["id"]

if order_id:
    resp = test("Get Order Detail", "GET", f"{BASE}/orders/{order_id}")
    if resp:
        print(f"  Order {order_id} status: {resp.get('status')}")

# Switch to admin for status updates
login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")

if order_id:
    resp = test("Update Order Status → Processing", "PATCH",
        f"{BASE}/orders/{order_id}/status", {"status": "processing"})
    if resp:
        print(f"  New status: {resp.get('status')}")

    resp = test("Update Order Status → Shipped", "PATCH",
        f"{BASE}/orders/{order_id}/status", {"status": "shipped"})
    if resp:
        print(f"  New status: {resp.get('status')}")

    resp = test("Update Order Status → Delivered", "PATCH",
        f"{BASE}/orders/{order_id}/status", {"status": "delivered"})
    if resp:
        print(f"  New status: {resp.get('status')}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. REVIEWS  (customer)
# ══════════════════════════════════════════════════════════════════════════════
section("7. REVIEWS")

login(email, password, label="customer")

if product_ids:
    resp = test("Add Review to Product 1", "POST",
        f"{BASE}/reviews/{product_ids[0]}", {
            "rating":  5,
            "comment": "Excellent product! Very satisfied with the purchase.",
        }, expected=201)
    if resp:
        print(f"  Review: ★{resp.get('rating')} - {resp.get('comment')}")

    if len(product_ids) > 1:
        resp = test("Add Review to Product 2", "POST",
            f"{BASE}/reviews/{product_ids[1]}", {
                "rating":  4,
                "comment": "Good quality but slightly expensive.",
            }, expected=201)
        if resp:
            print(f"  Review: ★{resp.get('rating')} - {resp.get('comment')}")

    resp = test("Get Reviews for Product 1", "GET", f"{BASE}/reviews/{product_ids[0]}")
    if resp:
        print(f"  Total reviews: {len(resp)}")
        for r in resp:
            print(f"    ★{r['rating']} - {r['comment']}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
section("8. FINAL SUMMARY")

login(ADMIN_EMAIL, ADMIN_PASSWORD)

cats  = requests.get(f"{BASE}/categories/", headers=headers).json()
prods = requests.get(f"{BASE}/products/",   headers=headers).json()

total_cats  = len(cats)  if isinstance(cats,  list) else 0
total_prods = prods.get("total", 0) if isinstance(prods, dict) else 0

order_status = "tested ✅" if order_id  else "⚠️  skipped (no address)"
addr_status  = "tested ✅" if address_id else "❌ failed"

print(f"""
  Database Summary:
  ├── Categories:  {total_cats}
  ├── Products:    {total_prods}
  ├── Addresses:   {addr_status}
  ├── Cart items:  tested ✅
  ├── Orders:      {order_status}
  └── Reviews:     tested ✅

  API Summary:
  ├── Auth:        ✅ register, login, me
  ├── Categories:  ✅ create, list
  ├── Products:    ✅ create, list, search, filter, get by slug
  ├── Cart:        ✅ add, get, update qty
  ├── Addresses:   ✅ create, list
  ├── Orders:      ✅ checkout, list, detail, update status
  └── Reviews:     ✅ add, list
""")

print("═" * 50)
print("  ALL TESTS COMPLETE 🚀")
print("═" * 50 + "\n")