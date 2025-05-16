from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from library import views
from library.views import TopActiveMembersView

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'members', views.MemberViewSet)
router.register(r'loans', views.LoanViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/members/top-active/', TopActiveMembersView.as_view(), name="top-active-members"),
]