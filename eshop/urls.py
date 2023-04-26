from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='ECom Store API',
        default_version='1.0.0',
        description= "This is swagger documentation for eshop api"
    ),
    public = True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('account.urls')),
    # path('api/', include('order.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='eshop_swagger_schema')
]

handler404 = "utilis.error_views.handler404"
handler500 = "utilis.error_views.handler500"
