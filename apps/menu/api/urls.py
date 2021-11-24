from rest_framework.routers import DefaultRouter

from .views.menu import MenuItemViewSet, MenuViewSet
from .views.menu_select import MenuSelectCreateViewSet

router = DefaultRouter()
router.register(r"menu", MenuViewSet)
router.register(r"menu_item", MenuItemViewSet)
router.register(r"menu_select", MenuSelectCreateViewSet, basename="menu_select")


urlpatterns = router.urls
