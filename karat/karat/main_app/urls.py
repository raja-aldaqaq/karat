from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('shops/', views.shops_index, name='index'),
  path('shops/<int:shop_id>', views.shops_detail, name='detail'),

  path('shop/create', views.shopCreate.as_view(), name='shop_create'),
  path('shops/<int:pk>/update/', views.shopUpdate.as_view(), name='shops_update'),
  path('shops/<int:pk>/delete/', views.shopDelete.as_view(), name='shops_delete'),
  
  #signup
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/',views.profile, name='profile'),
  path('adduser/',views.addnewuser, name='adduser'),


  # URLs for Product CRUD Operations
  path('products/', views.ProductList.as_view(), name='products_index'), #Index
  path('products/my_products', views.my_products, name='my_products'), #Index
  path('products/<int:pk>/', views.ProductDetail.as_view(), name='products_detail'), # Details/Show
  path('products/create/', views.ProductCreate.as_view(), name = 'products_create'), # Create
  path('products/<int:pk>/update/', views.ProductUpdate.as_view(), name = 'products_update'), # Update
  path('products/<int:pk>/delete/', views.ProductDelete.as_view(), name = 'products_delete'), # delete

  # display products by category
  path('products/categories/', views.category , name = 'categories'), # categories
  path('products/<category>/products_by_category/', views.category_products , name = 'products_by_category'), # products by category

  # display products by shops

  #API
  # path('gold/', views.gold),

  # ADD TO CART - When Clicked On Click Cart //ADDS to the order model
  # path('add_to_cart/<int:product_id>/<int:user_id>/<int:shop_id>/', views.add_to_cart, name='add_to_cart'),
  path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('view_cart/<int:user_id>/', views.view_cart, name='view_cart'),


]