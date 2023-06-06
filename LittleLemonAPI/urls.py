from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/',views.MenuItemView.as_view()),
    path('categories', views.CategoriesView.as_view()),
    path('menu-items/<int:pk>',views.SingletMenuItemView.as_view()),
    path('api-token-auth/',obtain_auth_token),
    path('manager-view/',views.manager_view),
    path('groups/manager/users',views.managers)
]
