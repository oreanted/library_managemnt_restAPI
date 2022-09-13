from django.urls import path, include

from apps.book import views
# local imports
from apps.book.utils import OptionalSlashRouter

router = OptionalSlashRouter()

router.register(r'book', views.EmployeeViewSet, basename='book')

urlpatterns = [
    path(r'book/', include(router.urls)),
]
