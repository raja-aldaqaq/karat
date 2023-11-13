from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('shops/', views.shops_index, name='index'),
    path('shops/<int:shop_id>', views.shops_detail, name='detail'),

    path('shop/create', views.shopCreate.as_view(), name='shop_create'),
    path('shops/<int:pk>/update/', views.shopUpdate.as_view(), name='shops_update'),
    path('shops/<int:pk>/delete/', views.shopDelete.as_view(), name='shops_delete'),

    # signup
    path('accounts/signup/', views.signup, name='signup'),

    # URLs for Product CRUD Operations
    path('products/', views.ProductList.as_view(),
         name='products_index'),  # Index
    path('products/<int:pk>/', views.ProductDetail.as_view(),
         name='products_detail'),  # Details/Show
    path('products/create/', views.ProductCreate.as_view(),
         name='products_create'),  # Create
    path('products/<int:pk>/update/', views.ProductUpdate.as_view(),
         name='products_update'),  # Update
    path('products/<int:pk>/delete/', views.ProductDelete.as_view(),
         name='products_delete'),  # delete

    # ADD TO CART - When Clicked On Click Cart //ADDS to the order model
    #     path('add_to_cart/<int:product_id>/<int:user_id>/<int:shop_id>/',
    #          views.add_to_cart, name='add_to_cart'),
    #     path('cart/<int:user_id>/', views.view_cart, name='cart')
]
