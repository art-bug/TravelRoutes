from django.urls import path
from .views import home, load_circular_routes, get_circular_routes

urlpatterns = [
    path('', home, name='home'),
    path('select-usa-city', load_circular_routes, name="load_circular_routes"),
    path('routes', get_circular_routes, name="get_circular_routes")
]
