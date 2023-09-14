
from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.shop, name="shopping"),
	path('/cart_details/<str:cart_id>/',views.cart_details, name='cart_details'),
	path('/add_to_cart/<int:laptop_id>',views.add_to_cart, name='add_to_cart'),
 	path('/delete_cart_item/<int:cart_item_id>',views.delete_cart_item, name='delete_cart_item'),

    # path('product_detail/<str:laptop_id>/',views.product_detail, name='product_detail'),
	# path('cart/', views.cart, name="cart"),
	# path('checkout/', views.checkout, name="checkout"),

	# path('update_item/', views.updateItem, name="update_item"),
	# path('process_order/', views.processOrder, name="process_order"),

]