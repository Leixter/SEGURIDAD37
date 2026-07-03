from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí le decimos: "Cualquier cosa que empiece con api/, mándalo a la carpeta api"
    path('api/', include('api.urls')), 
]