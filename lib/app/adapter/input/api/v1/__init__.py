from fastapi import APIRouter
from lib.app.adapter.input.api.v1.auth.auth             import router as auth_router
from lib.app.adapter.input.api.v1.products.products     import router as products_router
from lib.app.adapter.input.api.v1.categories.categories import router as categories_router
from lib.app.adapter.input.api.v1.cart.cart             import router as cart_router
from lib.app.adapter.input.api.v1.orders.orders         import router as orders_router
from lib.app.adapter.input.api.v1.reviews.reviews       import router as reviews_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(products_router)
router.include_router(categories_router)
router.include_router(cart_router)
router.include_router(orders_router)
router.include_router(reviews_router)

__all__ = ["router"]