
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls'))
]

handler404 = "utilis.error_views.handler404"
handler500 = "utilis.error_views.handler500"
