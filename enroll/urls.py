from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import add, show, update, delete,admin_users

urlpatterns = [
    path('', add, name='add_data'),
    path('show/', show, name='show'),
    path('update/<str:email>/', update, name='update'),
    path('delete/<str:email>/', delete, name='delete'),
    path('admin/', admin_users, name='admin_users'),  # Admin route
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
