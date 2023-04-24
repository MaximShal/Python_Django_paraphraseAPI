from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paraphrase/', include('paraphrase_app.urls')),
]
