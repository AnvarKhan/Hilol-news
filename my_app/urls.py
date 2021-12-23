from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('',BlogListView.as_view(),name='home'),
    path('postdetail/<int:news_id>/', views.post_detail, name="post_detail"),
    path('category/<int:category_id>/', views.category,name="category"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
