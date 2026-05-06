import requests

BASE    = "http://localhost:8000/api/v1"
token   = None
headers = {}

def test(name, method, url, data=None, expected=200):
    resp = requests.request(method, url, json=data, headers=headers)
    status = "✅" if resp.status_code == expected else "❌"
    print(f"{status} {name} → {resp.status_code}")
    if resp.status_code not in [200, 201]:
        print(f"   Error: {resp.text[:150]}")
    try:
        return resp.json()
    except:
        return None

# ── AUTH ──────────────────────────────────────────────
print("\n══════════════════════════════")
print("  AUTH")
print("══════════════════════════════")

test("Register", "POST", f"{BASE}/auth/register", {
    "name":     "API Test User",
    "email":    "apitest@gmail.com",
    "password": "test1234",
    "phone":    "9800000000"
}, expected=201)

resp = test("Login", "POST", f"{BASE}/auth/login", {
    "email":    "apitest@gmail.com",
    "password": "test1234"
})
if resp and "access_token" in resp:
    token = resp["access_token"]
    headers["Authorization"] = f"Bearer {token}"
    print(f"   Token saved ✅")
else:
    print("   ❌ Could not get token — remaining tests may fail")

test("Get Me", "GET", f"{BASE}/auth/me")

# ── CATEGORIES ────────────────────────────────────────
print("\n══════════════════════════════")
print("  CATEGORIES")
print("══════════════════════════════")

resp = test("Get All Categories", "GET", f"{BASE}/categories")
if resp:
    print(f"   Total categories: {len(resp)}")

# ── PRODUCTS ──────────────────────────────────────────
print("\n══════════════════════════════")
print("  PRODUCTS")
print("══════════════════════════════")

resp = test("Get All Products", "GET", f"{BASE}/products")
if resp:
    print(f"   Total products: {resp.get('total', 0)}")

resp = test("Get Products with Search", "GET",
    f"{BASE}/products?search=phone&limit=5")
if resp:
    print(f"   Search results: {resp.get('total', 0)}")

# ── CART ──────────────────────────────────────────────
print("\n══════════════════════════════")
print("  CART")
print("══════════════════════════════")

resp = test("Get Cart", "GET", f"{BASE}/cart")
if resp:
    print(f"   Cart items: {len(resp.get('items', []))}")
    print(f"   Cart total: Rs. {resp.get('total', 0)}")

# ── ORDERS ────────────────────────────────────────────
print("\n══════════════════════════════")
print("  ORDERS")
print("══════════════════════════════")

resp = test("Get My Orders", "GET", f"{BASE}/orders")
if resp:
    print(f"   Total orders: {len(resp)}")

# ── REVIEWS ───────────────────────────────────────────
print("\n══════════════════════════════")
print("  REVIEWS")
print("══════════════════════════════")

resp = test("Get Reviews for Product 1", "GET", f"{BASE}/reviews/1")
if resp is not None:
    print(f"   Total reviews: {len(resp)}")

# ── SUMMARY ───────────────────────────────────────────
print("\n══════════════════════════════")
print("  DONE")
print("══════════════════════════════\n")