from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  

# Home page view
def home(request):
    return HttpResponse("Welcome to the Home Page!✌️")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include the URLs from the api app
]

