from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from core.views import CustomLoginView  # Import CustomLoginView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line for login/logout/password URLs
    path('login/', CustomLoginView.as_view(), name='login'),  # Custom login view
    path('logout/', LogoutView.as_view(), name='logout'), 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)