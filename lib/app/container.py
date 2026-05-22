# lib/app/container.py
from dependency_injector import containers, providers

from lib.core.config import config
from lib.core.db.postgresql.impl import PostgreSQLClient

# ── Repositories (Adapter Output Layer) ──────────────────────────────────────
from lib.app.adapter.output.persistence.user.repositories     import UserRepositoryImpl
from lib.app.adapter.output.persistence.product.repositories  import ProductRepositoryImpl
from lib.app.adapter.output.persistence.category.repositories import CategoryRepositoryImpl
from lib.app.adapter.output.persistence.cart.repositories     import CartRepositoryImpl
from lib.app.adapter.output.persistence.order.repositories    import OrderRepositoryImpl
from lib.app.adapter.output.persistence.review.repositories   import ReviewRepositoryImpl

# ── Services (Application Layer) ─────────────────────────────────────────────
from lib.app.application.services.auth_service     import AuthService
from lib.app.application.services.product_service  import ProductService
from lib.app.application.services.category_service import CategoryService
from lib.app.application.services.cart_service     import CartService
from lib.app.application.services.order_service    import OrderService
from lib.app.application.services.review_service   import ReviewService

from lib.app.adapter.output.persistence.address.repositories import AddressRepositoryImpl
from lib.app.application.services.address_service import AddressService

from lib.app.adapter.output.persistence.seller.repositories import SellerRepositoryImpl
from lib.app.application.services.seller_service import SellerService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
    modules=[
        "lib.app.adapter.input.api.v1.auth.auth",
        "lib.app.adapter.input.api.v1.products.products",
        "lib.app.adapter.input.api.v1.categories.categories",
        "lib.app.adapter.input.api.v1.cart.cart",
        "lib.app.adapter.input.api.v1.orders.orders",
        "lib.app.adapter.input.api.v1.reviews.reviews",
        "lib.app.adapter.input.api.v1.addresses.addresses",
        "lib.app.adapter.input.api.v1.seller.seller",
        "lib.app.adapter.input.api.v1.seller.products",
        "lib.app.adapter.input.api.v1.dependencies.auth",
            ]
        )

    # =========================================================================
    # INFRASTRUCTURE LAYER — core connections
    # =========================================================================

    db_client = providers.Singleton(
        PostgreSQLClient,
        database_url=config.DATABASE_URL,
    )

    # =========================================================================
    # ADAPTER LAYER — Repositories
    # each repo receives the db_client so it can open sessions
    # =========================================================================

    user_repository = providers.Singleton(
        UserRepositoryImpl,
        db_client=db_client,
    )

    product_repository = providers.Singleton(
        ProductRepositoryImpl,
        db_client=db_client,
    )

    category_repository = providers.Singleton(
        CategoryRepositoryImpl,
        db_client=db_client,
    )

    cart_repository = providers.Singleton(
        CartRepositoryImpl,
        db_client=db_client,
    )

    order_repository = providers.Singleton(
        OrderRepositoryImpl,
        db_client=db_client,
    )

    review_repository = providers.Singleton(
        ReviewRepositoryImpl,
        db_client=db_client,
    )

    # =========================================================================
    # APPLICATION LAYER — Services
    # each service receives only the repositories it needs
    # =========================================================================

    auth_service = providers.Singleton(
        AuthService,
        user_repository=user_repository,
    )

    product_service = providers.Singleton(
        ProductService,
        product_repository=product_repository,
    )

    category_service = providers.Singleton(
        CategoryService,
        category_repository=category_repository,
    )

    cart_service = providers.Singleton(
        CartService,
        cart_repository=cart_repository,
        product_repository=product_repository,  # ← needs product to check stock
    )
   
    # Add alongside your other repository providers:
    address_repository = providers.Singleton(
        AddressRepositoryImpl,
        db_client=db_client,
    )
    address_service = providers.Factory(
        AddressService,
        address_repository=address_repository,
    )

    # Update order_service to inject it:
    order_service = providers.Factory(
        OrderService,
        order_repository   = order_repository,
        cart_repository    = cart_repository,
        address_repository = address_repository,   # ← add this line
    )

    review_service = providers.Singleton(
        ReviewService,
        review_repository=review_repository,
    )


        # Add repositories
    seller_repository = providers.Singleton(
        SellerRepositoryImpl,
        db_client=db_client,
    )

    # Add service
    seller_service = providers.Singleton(
        SellerService,
        seller_repository=seller_repository,
    )