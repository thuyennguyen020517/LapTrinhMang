from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.index, name='store'),
    path('lapList/', views.lapList, name='lapList'),
    path('add_laptop/', views.add_laptop, name='add_laptop'),
    path('laptop_update/<str:pk>/', views.laptop_update, name='laptop_update'),
    path('delete_laptop/<str:pk>/', views.delete_laptop, name='delete_laptop'),
    path('laptop_detail/<str:laptop_id>/',views.laptop_detail, name='laptop_detail'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('view_images/', views.view_images, name='view_images'),
    path('edit_image/<int:pk>/', views.EditImageView.as_view(), name='edit_image'),
    path('delete_image/<int:pk>/', views.DeleteImageView.as_view(), name='delete_image'),
    # CUSTOMER
    path('users/', views.users_list, name='users'),
    path('user_detail/<str:user_id>/',views.user_detail, name='user_detail'),
    path('user_update/<str:pk>/', views.user_update, name='user_update'),
    path('user_delete/<str:pk>/', views.user_delete, name='user_delete'),
    path('user_add/', views.user_add, name='user_add'),
    # Brand
    path('brand_list/', views.brand_list, name='brand_list'),
    path('brand_detail/<str:brand_id>/',views.brand_detail, name='brand_detail'),
    path('brand_add/', views.brand_add, name='brand_add'),
    path('brand_update/<str:brand_id>/', views.brand_update, name='brand_update'),
    path('brand_delete/<str:brand_id>/', views.brand_delete, name='brand_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
