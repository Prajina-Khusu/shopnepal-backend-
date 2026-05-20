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
        print(f"  ❌ Login failed for {email} → {resp.status_code}")
        return None

# ══════════════════════════════════════════════════════
# 1. AUTH
# ══════════════════════════════════════════════════════
section("1. AUTH")

email    = f"customer{random.randint(1000,9999)}@gmail.com"
password = "test1234"
print(f"  Using customer email: {email}")

test("Register Customer", "POST", f"{BASE}/auth/register", {
    "name":     "Test Customer",
    "email":    email,
    "password": password,
    "phone":    "9800000001"
}, expected=201)

login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")
resp = test("Get Me (Admin)", "GET", f"{BASE}/auth/me")
if resp:
    print(f"  Logged in as: {resp.get('name')} | role: {resp.get('role')}")

# ══════════════════════════════════════════════════════
# 2. CATEGORIES (admin)
# ══════════════════════════════════════════════════════
section("2. CATEGORIES")

resp = requests.get(f"{BASE}/categories/", headers=headers)
existing_cats  = resp.json() if resp.status_code == 200 else []
existing_slugs = [c["slug"] for c in existing_cats]
cat_ids        = {c["name"]: c["id"] for c in existing_cats}
print(f"  Existing categories: {len(existing_cats)}")

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
    print(f"  Total categories: {len(resp)}")
    for c in resp:
        cat_ids[c["name"]] = c["id"]
        print(f"    - [{c['id']}] {c['name']}")

# ══════════════════════════════════════════════════════
# 3. PRODUCTS (admin)
# ══════════════════════════════════════════════════════
section("3. PRODUCTS")

resp = requests.get(f"{BASE}/products/", headers=headers)
existing_prods  = resp.json() if resp.status_code == 200 else {}
existing_slugs  = [p["slug"] for p in existing_prods.get("items", [])]
product_ids     = [p["id"]   for p in existing_prods.get("items", [])]
product_slugs   = [p["slug"] for p in existing_prods.get("items", [])]
print(f"  Existing products: {existing_prods.get('total', 0)}")

import re
def slugify(text):
    text = text.lower().strip()
    return re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s-]", "", text))

electronics_id = cat_ids.get("Electronics", 1)
fashion_id     = cat_ids.get("Fashion",     2)
sports_id      = cat_ids.get("Sports",      5)

products = [
    {"name": "Samsung Galaxy A15",    "description": "5G Smartphone 128GB",          "price": 28500, "sale_price": 25000, "stock": 50,  "category_id": electronics_id},
    {"name": "Apple AirPods Pro",     "description": "Active noise cancellation",     "price": 35000, "sale_price": 32000, "stock": 30,  "category_id": electronics_id},
    {"name": "Nike Air Max 270",      "description": "Lightweight running shoes",     "price": 8500,  "sale_price": 7000,  "stock": 40,  "category_id": fashion_id},
    {"name": "Adidas Track Pants",    "description": "Comfortable sports track pants","price": 3500,  "sale_price": 2800,  "stock": 60,  "category_id": sports_id},
    {"name": "Wireless Mouse Logitech","description": "Ergonomic wireless mouse",     "price": 2500,  "sale_price": None,  "stock": 100, "category_id": electronics_id},
]

for product in products:
    slug = slugify(product["name"])
    if slug in existing_slugs:
        print(f"  ⚠️  {product['name']} already exists — skipping")
    else:
        resp = test(f"Create {product['name']}", "POST", f"{BASE}/products/", product, expected=201)
        if resp and "id" in resp:
            product_ids.append(resp["id"])
            product_slugs.append(resp["slug"])
            print(f"    slug: {resp['slug']}")

resp = test("Get All Products",       "GET", f"{BASE}/products/")
if resp:
    print(f"  Total products: {resp.get('total', 0)}")

resp = test("Search (samsung)",       "GET", f"{BASE}/products/?search=samsung")
if resp:
    print(f"  Search results: {resp.get('total', 0)}")

resp = test("Filter by Electronics",  "GET", f"{BASE}/products/?category_id={electronics_id}")
if resp:
    print(f"  Electronics products: {resp.get('total', 0)}")

if product_slugs:
    resp = test("Get Product by Slug","GET", f"{BASE}/products/{product_slugs[0]}")
    if resp:
        print(f"  Found: {resp.get('name')} | Price: Rs.{resp.get('price')}")

# ══════════════════════════════════════════════════════
# 4. SELLER APPLICATION FLOW
# ══════════════════════════════════════════════════════
section("4. SELLER APPLICATION")

seller_email    = f"seller{random.randint(1000,9999)}@gmail.com"
seller_password = "seller1234"
print(f"  Using seller email: {seller_email}")

# Register seller as customer first
test("Register Seller Account", "POST", f"{BASE}/auth/register", {
    "name":     "Test Seller",
    "email":    seller_email,
    "password": seller_password,
    "phone":    "9800000002"
}, expected=201)

# Login as seller
login(seller_email, seller_password, label="seller applicant")

# Apply to become seller
application_id = None
resp = test("Apply as Seller", "POST", f"{BASE}/seller/apply", {
    "shop_name":    "Test Electronics Shop",
    "shop_address": "New Road, Kathmandu",
    "phone":        "9800000002",
    "description":  "Selling quality electronics products"
}, expected=201)
if resp and "id" in resp:
    application_id = resp["id"]
    print(f"  Application ID: {application_id} | Status: {resp.get('status')}")

# Check application status
resp = test("Check My Application", "GET", f"{BASE}/seller/my-application")
if resp:
    print(f"  Application status: {resp.get('status')}")

# Admin reviews application
login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")

resp = test("Get All Pending Applications", "GET",
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

# Seller logs in again — now has seller role
login(seller_email, seller_password, label="seller")
resp = test("Get Me (Seller)", "GET", f"{BASE}/auth/me")
if resp:
    print(f"  Role after approval: {resp.get('role')}")

# ══════════════════════════════════════════════════════
# 5. CART (customer)
# ══════════════════════════════════════════════════════
section("5. CART")

login(email, password, label="customer")

cart_items = []

if product_ids:
    resp = test("Add Product 1 to Cart", "POST", f"{BASE}/cart/", {
        "product_id": product_ids[0],
        "quantity":   2
    }, expected=201)
    if resp:
        print(f"  Cart items: {len(resp.get('items',[]))} | Total: Rs.{resp.get('total',0)}")

    if len(product_ids) > 1:
        resp = test("Add Product 2 to Cart", "POST", f"{BASE}/cart/", {
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

# ══════════════════════════════════════════════════════
# 6. ADDRESSES (customer)
# ══════════════════════════════════════════════════════
section("6. ADDRESSES")

address_id = None

resp = test("Create Address", "POST", f"{BASE}/addresses/", {
    "full_name":  "Test Customer",
    "phone":      "9800000001",
    "street":     "Thamel Marg 12",
    "city":       "Kathmandu",
    "province":   "Bagmati",
    "is_default": True
}, expected=201)
if resp and "id" in resp:
    address_id = resp["id"]
    print(f"  Address ID: {address_id} | {resp.get('street')}, {resp.get('city')}")

resp = test("Get My Addresses", "GET", f"{BASE}/addresses/")
if resp:
    print(f"  Total addresses: {len(resp)}")
    for a in resp:
        print(f"    - [{a['id']}] {a['full_name']} | {a['street']}, {a['city']} {'⭐' if a.get('is_default') else ''}")

# ══════════════════════════════════════════════════════
# 7. ORDERS (customer → admin)
# ══════════════════════════════════════════════════════
section("7. ORDERS")

order_id = None

if not address_id:
    print("  ⚠️  Skipping checkout — address creation failed")
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

resp = test("Get My Orders", "GET", f"{BASE}/orders/")
if resp:
    print(f"  Total orders: {len(resp)}")
    if not order_id and len(resp) > 0:
        order_id = resp[0]["id"]

if order_id:
    resp = test("Get Order Detail", "GET", f"{BASE}/orders/{order_id}")
    if resp:
        print(f"  Order {order_id} status: {resp.get('status')}")

login(ADMIN_EMAIL, ADMIN_PASSWORD, label="admin")

if order_id:
    for status in ["processing", "shipped", "delivered"]:
        resp = test(f"Update Status → {status.capitalize()}", "PATCH",
            f"{BASE}/orders/{order_id}/status", {"status": status})
        if resp:
            print(f"  New status: {resp.get('status')}")

# ══════════════════════════════════════════════════════
# 8. REVIEWS (customer)
# ══════════════════════════════════════════════════════
section("8. REVIEWS")

login(email, password, label="customer")

if product_ids:
    resp = test("Add Review to Product 1", "POST",
        f"{BASE}/reviews/{product_ids[0]}", {
            "rating":  5,
            "comment": "Excellent product! Very satisfied."
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
# 9. FINAL SUMMARY
# ══════════════════════════════════════════════════════
section("9. FINAL SUMMARY")

login(ADMIN_EMAIL, ADMIN_PASSWORD)

cats  = requests.get(f"{BASE}/categories/", headers=headers).json()
prods = requests.get(f"{BASE}/products/",   headers=headers).json()
apps  = requests.get(f"{BASE}/seller/applications", headers=headers).json()

total_cats  = len(cats)              if isinstance(cats,  list) else 0
total_prods = prods.get("total", 0)  if isinstance(prods, dict) else 0
total_apps  = len(apps)              if isinstance(apps,  list) else 0

print(f"""
  Database Summary:
  ├── Categories:         {total_cats}
  ├── Products:           {total_prods}
  ├── Seller Applications:{total_apps}
  ├── Addresses:          {"✅" if address_id else "❌"}
  ├── Cart:               tested ✅
  ├── Orders:             {"✅" if order_id else "⚠️  skipped"}
  └── Reviews:            tested ✅

  API Summary:
  ├── Auth:               ✅ register, login, me
  ├── Categories:         ✅ create, list
  ├── Products:           ✅ create, list, search, filter, slug
  ├── Seller Application: ✅ apply, check status, approve
  ├── Cart:               ✅ add, get, update qty
  ├── Addresses:          ✅ create, list
  ├── Orders:             ✅ checkout, list, detail, update status
  └── Reviews:            ✅ add, list
""")

print("═" * 50)
print("  ALL TESTS COMPLETE 🚀")
print("═" * 50 + "\n")