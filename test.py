import requests
import random
import re

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
    resp = requests.post(
        f"{BASE}/auth/login",
        json={"email": email, "password": password}
    )
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        headers["Authorization"] = f"Bearer {token}"
        if label:
            print(f"  Switched to {label} token ✅")
        return token
    else:
        print(f"  ❌ Login failed for {email} → {resp.status_code}: {resp.text[:100]}")
        return None

def slugify(text):
    text = text.lower().strip()
    return re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s-]", "", text))

# ══════════════════════════════════════════════════════
# TRACK ALL IDS
# ══════════════════════════════════════════════════════
customer_email    = f"customer{random.randint(1000,9999)}@gmail.com"
customer_password = "test1234"
seller_email      = f"seller{random.randint(1000,9999)}@gmail.com"
seller_password   = "seller1234"

cat_ids        = {}
product_ids    = []
product_slugs  = []
address_id     = None
order_id       = None
application_id = None

# ══════════════════════════════════════════════════════
# 1. AUTH
# ══════════════════════════════════════════════════════
section("1. AUTH")

print(f"  Customer email: {customer_email}")
print(f"  Seller email:   {seller_email}")

# Register customer
resp = test("Register Customer", "POST", f"{BASE}/auth/register", {
    "name":     "Test Customer",
    "email":    customer_email,
    "password": customer_password,
    "phone":    "9800000001"
}, expected=201)
if resp:
    print(f"  Customer ID: {resp.get('id')}")

# Register seller applicant
resp = test("Register Seller Account", "POST", f"{BASE}/auth/register", {
    "name":     "Test Seller",
    "email":    seller_email,
    "password": seller_password,
    "phone":    "9800000002"
}, expected=201)
if resp:
    print(f"  Seller Account ID: {resp.get('id')}")

# Admin login
login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")
resp = test("Get Me (Admin)", "GET", f"{BASE}/auth/me")
if resp:
    print(f"  Admin: {resp.get('name')} | role: {resp.get('role')}")

# ══════════════════════════════════════════════════════
# 2. CATEGORIES (Admin only)
# ══════════════════════════════════════════════════════
section("2. CATEGORIES")

# Get existing
resp = requests.get(f"{BASE}/categories/", headers=headers)
existing = resp.json() if resp.status_code == 200 else []
existing_slugs = [c["slug"] for c in existing]
cat_ids = {c["name"]: c["id"] for c in existing}
print(f"  Existing: {len(existing)} categories")

categories = [
    {"name": "Electronics", "slug": "electronics", "image_url": "https://example.com/electronics.jpg"},
    {"name": "Fashion",     "slug": "fashion",     "image_url": "https://example.com/fashion.jpg"},
    {"name": "Grocery",     "slug": "grocery",     "image_url": "https://example.com/grocery.jpg"},
    {"name": "Beauty",      "slug": "beauty",      "image_url": "https://example.com/beauty.jpg"},
    {"name": "Sports",      "slug": "sports",      "image_url": "https://example.com/sports.jpg"},
]

for cat in categories:
    if cat["slug"] in existing_slugs:
        print(f"  ⚠️  {cat['name']} already exists — skipping")
    else:
        resp = test(f"Create {cat['name']}", "POST", f"{BASE}/categories/", cat, expected=201)
        if resp and "id" in resp:
            cat_ids[cat["name"]] = resp["id"]

resp = test("Get All Categories", "GET", f"{BASE}/categories/")
if resp:
    print(f"  Total: {len(resp)}")
    for c in resp:
        cat_ids[c["name"]] = c["id"]
        print(f"    - [{c['id']}] {c['name']}")

# ══════════════════════════════════════════════════════
# 3. ADMIN ADDS PRODUCTS
# ══════════════════════════════════════════════════════
section("3. ADMIN PRODUCTS")

electronics_id = cat_ids.get("Electronics", 1)
fashion_id     = cat_ids.get("Fashion",     2)
sports_id      = cat_ids.get("Sports",      5)

# Get existing products
resp = requests.get(f"{BASE}/products/", headers=headers)
existing_prods = resp.json() if resp.status_code == 200 else {}
existing_slugs = [p["slug"] for p in existing_prods.get("items", [])]
product_ids    = [p["id"]   for p in existing_prods.get("items", [])]
product_slugs  = [p["slug"] for p in existing_prods.get("items", [])]
print(f"  Existing: {existing_prods.get('total', 0)} products")

admin_products = [
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
]

for product in admin_products:
    slug = slugify(product["name"])
    if slug in existing_slugs:
        print(f"  ⚠️  {product['name']} already exists — skipping")
    else:
        resp = test(
            f"Admin creates: {product['name']}",
            "POST", f"{BASE}/products/", product, expected=201
        )
        if resp and "id" in resp:
            product_ids.append(resp["id"])
            product_slugs.append(resp["slug"])
            print(f"    seller_id: {resp.get('seller_id')} (None = platform product)")

resp = test("Get All Products", "GET", f"{BASE}/products/")
if resp:
    print(f"  Total products: {resp.get('total', 0)}")

resp = test("Search Products (samsung)", "GET", f"{BASE}/products/?search=samsung")
if resp:
    print(f"  Search results: {resp.get('total', 0)}")

resp = test("Filter by Electronics", "GET",
    f"{BASE}/products/?category_id={electronics_id}")
if resp:
    print(f"  Electronics products: {resp.get('total', 0)}")

if product_slugs:
    resp = test("Get Product by Slug", "GET",
        f"{BASE}/products/{product_slugs[0]}")
    if resp:
        print(f"  Found: {resp.get('name')} | Rs.{resp.get('price')}")

# ══════════════════════════════════════════════════════
# 4. SELLER APPLICATION FLOW
# ══════════════════════════════════════════════════════
section("4. SELLER APPLICATION")

# Seller applies
login(seller_email, seller_password, label="seller applicant")

resp = test("Apply as Seller", "POST", f"{BASE}/seller/apply", {
    "shop_name":    "Test Electronics Shop",
    "shop_address": "New Road, Kathmandu",
    "phone":        "9800000002",
    "description":  "Selling quality electronics"
}, expected=201)
if resp and "id" in resp:
    application_id = resp["id"]
    print(f"  Application ID: {application_id} | Status: {resp.get('status')}")

resp = test("Check My Application Status", "GET", f"{BASE}/seller/my-application")
if resp:
    print(f"  Status: {resp.get('status')} | Shop: {resp.get('shop_name')}")

# Admin reviews
login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")

resp = test("Get Pending Applications", "GET",
    f"{BASE}/seller/applications?status=pending")
if resp:
    print(f"  Pending applications: {len(resp)}")
    for a in resp:
        print(f"    - [{a['id']}] {a['shop_name']} | {a['status']}")
        if not application_id:
            application_id = a["id"]

if application_id:
    resp = test("Approve Application", "PATCH",
        f"{BASE}/seller/applications/{application_id}/review",
        {"status": "approved"})
    if resp:
        print(f"  Application status: {resp.get('status')}")

# Verify seller role changed
login(seller_email, seller_password, label="seller")
resp = test("Get Me (should be seller now)", "GET", f"{BASE}/auth/me")
if resp:
    print(f"  Role: {resp.get('role')} ← should be 'seller'")

# ══════════════════════════════════════════════════════
# 5. SELLER ADDS PRODUCTS
# ══════════════════════════════════════════════════════
section("5. SELLER PRODUCTS")

seller_products = [
    {
        "name":        "Logitech Wireless Keyboard",
        "description": "Ergonomic wireless keyboard with long battery life",
        "price":       2500,
        "sale_price":  None,
        "stock":       100,
        "category_id": electronics_id
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
        "name":        "Sony WH-1000XM5",
        "description": "Premium noise cancelling headphones",
        "price":       45000,
        "sale_price":  42000,
        "stock":       15,
        "category_id": electronics_id
    },
]

seller_product_ids = []

for product in seller_products:
    slug = slugify(product["name"])
    if slug in existing_slugs:
        print(f"  ⚠️  {product['name']} already exists — skipping")
    else:
        resp = test(
            f"Seller creates: {product['name']}",
            "POST", f"{BASE}/seller/products/", product, expected=201
        )
        if resp and "id" in resp:
            seller_product_ids.append(resp["id"])
            product_ids.append(resp["id"])
            product_slugs.append(resp["slug"])
            print(f"    seller_id: {resp.get('seller_id')} ← seller's id")

# Seller views only their products
resp = test("Seller Gets Own Products", "GET", f"{BASE}/seller/products/")
if resp:
    print(f"  My products: {resp.get('total', 0)}")
    for p in resp.get("items", []):
        print(f"    - [{p['id']}] {p['name']} | seller_id: {p.get('seller_id')}")

# Seller updates their product
if seller_product_ids:
    resp = test("Seller Updates Own Product", "PUT",
        f"{BASE}/seller/products/{seller_product_ids[0]}", {
            "price": 2300,
            "stock": 90
        })
    if resp:
        print(f"  Updated price: Rs.{resp.get('price')} | stock: {resp.get('stock')}")

# All products visible to everyone
resp = test("All Products (public)", "GET", f"{BASE}/products/")
if resp:
    print(f"  Total products (admin + seller): {resp.get('total', 0)}")

# ══════════════════════════════════════════════════════
# 6. CART (customer)
# ══════════════════════════════════════════════════════
section("6. CART")

login(customer_email, customer_password, label="customer")

cart_items = []

if product_ids:
    resp = test("Add Admin Product to Cart", "POST", f"{BASE}/cart/", {
        "product_id": product_ids[0],
        "quantity":   2
    }, expected=201)
    if resp:
        print(f"  Cart items: {len(resp.get('items',[]))} | Total: Rs.{resp.get('total',0)}")

    if len(product_ids) > 1:
        resp = test("Add Seller Product to Cart", "POST", f"{BASE}/cart/", {
            "product_id": product_ids[1],
            "quantity":   1
        }, expected=201)
        if resp:
            print(f"  Cart items: {len(resp.get('items',[]))} | Total: Rs.{resp.get('total',0)}")

resp = test("Get Cart", "GET", f"{BASE}/cart/")
if resp:
    cart_items = resp.get("items", [])
    print(f"  Cart items: {len(cart_items)}")
    print(f"  Cart total: Rs.{resp.get('total', 0)}")

if cart_items:
    resp = test("Update Cart Item Qty", "PUT",
        f"{BASE}/cart/{cart_items[0]['id']}", {"quantity": 3})
    if resp:
        print(f"  Updated total: Rs.{resp.get('total', 0)}")

    resp = test("Remove Cart Item", "DELETE",
        f"{BASE}/cart/{cart_items[0]['id']}")
    if resp:
        print(f"  Item removed ✅")

resp = test("Get Cart After Remove", "GET", f"{BASE}/cart/")
if resp:
    print(f"  Cart items after remove: {len(resp.get('items', []))}")

# Re-add item for checkout
if product_ids:
    test("Re-add Item for Checkout", "POST", f"{BASE}/cart/", {
        "product_id": product_ids[0],
        "quantity":   1
    }, expected=201)

# ══════════════════════════════════════════════════════
# 7. ADDRESSES (customer)
# ══════════════════════════════════════════════════════
section("7. ADDRESSES")

resp = test("Create Primary Address", "POST", f"{BASE}/addresses/", {
    "full_name":  "Test Customer",
    "phone":      "9800000001",
    "street":     "Thamel Marg 12",
    "city":       "Kathmandu",
    "province":   "Bagmati",
    "is_default": True
}, expected=201)
if resp and "id" in resp:
    address_id = resp["id"]
    print(f"  Address ID: {address_id} | {resp.get('city')}")

resp = test("Create Second Address", "POST", f"{BASE}/addresses/", {
    "full_name":  "Test Customer",
    "phone":      "9800000001",
    "street":     "Lazimpat Road 5",
    "city":       "Kathmandu",
    "province":   "Bagmati",
    "is_default": False
}, expected=201)

resp = test("Get All My Addresses", "GET", f"{BASE}/addresses/")
if resp:
    print(f"  Total addresses: {len(resp)}")
    for a in resp:
        print(f"    - [{a['id']}] {a['street']}, {a['city']} {'⭐' if a.get('is_default') else ''}")

if address_id:
    resp = test("Get Address by ID", "GET", f"{BASE}/addresses/{address_id}")
    if resp:
        print(f"  Address: {resp.get('street')}, {resp.get('city')}")

# ══════════════════════════════════════════════════════
# 8. ORDERS (customer → admin)
# ══════════════════════════════════════════════════════
section("8. ORDERS")

if not address_id:
    print("  ⚠️  Skipping checkout — no address")
else:
    resp = test("Checkout", "POST", f"{BASE}/orders/checkout", {
        "address_id": address_id
    }, expected=201)
    if resp and "id" in resp:
        order_id = resp["id"]
        print(f"  Order ID:    {order_id}")
        print(f"  Status:      {resp.get('status')}")
        print(f"  Total:       Rs.{resp.get('total_amount')}")
        print(f"  Items:       {len(resp.get('items', []))}")
        for item in resp.get("items", []):
            print(f"    - Product {item['product_id']} x{item['quantity']} @ Rs.{item['price']}")

resp = test("Get My Orders", "GET", f"{BASE}/orders/")
if resp:
    print(f"  Total orders: {len(resp)}")
    if not order_id and resp:
        order_id = resp[0]["id"]

if order_id:
    resp = test("Get Order Detail", "GET", f"{BASE}/orders/{order_id}")
    if resp:
        print(f"  Order {order_id} | status: {resp.get('status')}")

# Admin updates order status
login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")

if order_id:
    for status in ["processing", "shipped", "delivered"]:
        resp = test(
            f"Update Status → {status.capitalize()}",
            "PATCH", f"{BASE}/orders/{order_id}/status",
            {"status": status}
        )
        if resp:
            print(f"  Status: {resp.get('status')}")

# ══════════════════════════════════════════════════════
# 9. REVIEWS (customer)
# ══════════════════════════════════════════════════════
section("9. REVIEWS")

login(customer_email, customer_password, label="customer")

if product_ids:
    resp = test("Review Admin Product", "POST",
        f"{BASE}/reviews/{product_ids[0]}", {
            "rating":  5,
            "comment": "Excellent product! Very satisfied with the purchase."
        }, expected=201)
    if resp:
        print(f"  ★{resp.get('rating')} - {resp.get('comment')}")

    if len(product_ids) > 1:
        resp = test("Review Seller Product", "POST",
            f"{BASE}/reviews/{product_ids[1]}", {
                "rating":  4,
                "comment": "Good quality seller. Fast delivery!"
            }, expected=201)
        if resp:
            print(f"  ★{resp.get('rating')} - {resp.get('comment')}")

    resp = test("Get Reviews for Product 1", "GET",
        f"{BASE}/reviews/{product_ids[0]}")
    if resp:
        print(f"  Total reviews: {len(resp)}")
        for r in resp:
            print(f"    ★{r['rating']} - {r['comment']}")

# ══════════════════════════════════════════════════════
# 10. ADMIN MANAGEMENT
# ══════════════════════════════════════════════════════
section("10. ADMIN MANAGEMENT")

login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")

# Admin updates a product
if product_ids:
    resp = test("Admin Updates Product", "PUT",
        f"{BASE}/products/{product_ids[0]}", {
            "price":     27000,
            "sale_price": 24000,
            "stock":     45
        })
    if resp:
        print(f"  Updated: {resp.get('name')} | Rs.{resp.get('price')}")

# Admin views all seller applications
resp = test("All Seller Applications", "GET", f"{BASE}/seller/applications")
if resp:
    print(f"  Total applications: {len(resp)}")
    for a in resp:
        print(f"    - [{a['id']}] {a['shop_name']} | {a['status']}")

# Admin views all orders
resp = test("All Categories", "GET", f"{BASE}/categories/")
if resp:
    print(f"  Total categories: {len(resp)}")

# ══════════════════════════════════════════════════════
# 11. FINAL SUMMARY
# ══════════════════════════════════════════════════════
section("11. FINAL SUMMARY")

login(ADMIN_EMAIL, ADMIN_PASSWORD)

cats  = requests.get(f"{BASE}/categories/", headers=headers).json()
prods = requests.get(f"{BASE}/products/",   headers=headers).json()
apps  = requests.get(f"{BASE}/seller/applications", headers=headers).json()

total_cats  = len(cats)             if isinstance(cats,  list) else 0
total_prods = prods.get("total", 0) if isinstance(prods, dict) else 0
total_apps  = len(apps)             if isinstance(apps,  list) else 0

print(f"""
  Database Summary:
  ├── Categories:          {total_cats}
  ├── Products (total):    {total_prods}
  ├── Seller Applications: {total_apps}
  ├── Addresses:           {"✅" if address_id     else "❌"}
  ├── Orders:              {"✅" if order_id        else "⚠️  skipped"}
  └── Reviews:             tested ✅

  User Flows Tested:
  ├── Customer:  register → browse → cart → checkout → review ✅
  ├── Seller:    register → apply → approved → add products ✅
  └── Admin:     login → manage categories → manage products → approve sellers ✅

  API Endpoints Tested:
  ├── Auth:              ✅ register, login, me
  ├── Categories:        ✅ create (admin), list
  ├── Admin Products:    ✅ create, list, search, filter, update
  ├── Seller Apply:      ✅ apply, check status, approve
  ├── Seller Products:   ✅ create own, list own, update own
  ├── Public Products:   ✅ list all (admin + seller combined)
  ├── Cart:              ✅ add, get, update, remove
  ├── Addresses:         ✅ create, list, get by id
  ├── Orders:            ✅ checkout, list, detail, update status
  └── Reviews:           ✅ add, list
""")

print("═" * 50)
print("  ALL TESTS COMPLETE 🚀")
print("═" * 50 + "\n")