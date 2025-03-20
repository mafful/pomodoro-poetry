from .home import router as home_router
from .ping import router as ping_router
from .tasks import router
from .add_fixtures import router as add_fixtures_router

routers = [home_router, ping_router, router, add_fixtures_router]

# Ensure routers are explicitly available for import
__all__ = (
    "routers",
)
