# When a user visits a specific URL, Django looks for a matching URL pattern and calls the corresponding view.py function to handle the request.
from django.urls import path, include  # Make sure to import `include`
from django.contrib import admin      # Import `admin` for the admin URLs
from . import views


# Home page view

def home(request):
    return HttpResponse("Welcome to the Home Page!✌️")


urlpatterns = [
    path('nl_query/', views.process_nl_query),
    
    # PostgreSQL endpoints
    path('postgres/tables/', views.get_postgres_tables),
    path('postgres/<str:table>/describe/', views.describe_postgres_table),
    path('postgres/<str:table>/sample/', views.sample_postgres_table),
    path('postgres/<str:table>/insert/', views.insert_postgres_data),
    path('postgres/<str:table>/update/', views.update_postgres_data),
    path('postgres/<str:table>/delete/', views.delete_postgres_data),

    # MongoDB endpoints
    path('mongo/collections/', views.get_mongo_collections),
    path('mongo/<str:collection>/sample/', views.sample_mongo_documents),
    path('mongo/run/', views.run_manual_mongo_query),

    # Mongo logs
    path('logs/', views.get_query_logs),
    path('logs/add/', views.add_query_log),
    path('logs/remove/', views.remove_query_log),
    path('logs/clear/', views.clear_query_logs),
]



