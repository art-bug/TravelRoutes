from django.shortcuts import render, reverse
from .travel_circular_routes import *
from django.core.paginator import Paginator

# Create your views here.

country_cities = None
distance_matrix = None

city_populations = None

index_cities = None

circular_routes = []

def get_routes_context(request):
    page_number = int(request.GET.get("page", 1))

    paginator = Paginator(circular_routes, 3)

    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    prev_url = ""
    next_url = ""

    if page.has_previous():
        prev_url = f"{reverse('get_circular_routes')}?page={page.previous_page_number()}"

    if page.has_next():
        next_url = f"{reverse('get_circular_routes')}?page={page.next_page_number()}"

    context = {
        "usa_cities": country_cities["United States"],
        "travel_circular_routes": page,
        "is_paginated": is_paginated,
        "prev_url": prev_url,
        "next_url": next_url
    }

    return context

def get_circular_routes(request):
    route_context = get_routes_context(request)
    return render(request, "optimal_travel_routes/home.html", route_context)

def load_circular_routes(request):
    global distance_matrix, city_populations, country_cities, index_cities, circular_routes

    city = int(request.GET["city"])

    circular_routes = travel_circular_routes(distance_matrix, city, max_distance=400.0, travel_days=7)

    string_routes = map(lambda route: (index_cities[route_city] for route_city in route), circular_routes)
    routes_scores = map(lambda route: set_score(list(route), city_populations), string_routes)
    sorted_circular_routes = sort_circular_routes(routes_scores)
    beautified_routes = list(map(lambda route: (" -> ".join(route[0]), route[1]), sorted_circular_routes))

    circular_routes = beautified_routes

    return get_circular_routes(request)

def home(request):
    global country_cities, distance_matrix, city_populations, index_cities

    distance_matrix_sheet, populations_sheet = get_worksheets("Funventurer_test_task_data.xlsx")
    country_cities, distance_matrix = get_distance_matrix(distance_matrix_sheet)
    index_cities = {index:city for cities in country_cities.values() for city, index in cities}
    city_populations = get_city_populations(populations_sheet)

    home_context = {
        "usa_cities": country_cities["United States"],
        **get_routes_context(request),
        "just_loaded": True
    }

    return render(request, "optimal_travel_routes/home.html", home_context)
