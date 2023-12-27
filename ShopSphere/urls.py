
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from . import views,user_login

admin.site.site_header = "ShopSphere Admin"
admin.site.site_title = "ShopSphere Admin Portal"
admin.site.index_title = "Welcome to ShopSphere Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE,name="base"),
    path('', views.HOME,name="home"),
    path('contact/', views.CONTACT,name="contact"),
    path('shop/', views.SHOP,name="shop"),
    path('shop/<slug>',views.DETAIL_PRODUCT,name='detail_product'),
    path('accounts/cart/', views.CART,name="cart"),
    path('accounts/cart/add', user_login.ADDCART,name="add-cart"),
    path('accounts/cart/remove/<id>', user_login.REMOVECART,name="remove-cart"),
    path('accounts/cart/update/<action>/<id>', user_login.UPDATEQTY,name="update-quantity"),

    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register', user_login.REGISTER,name="register"),
    path('accounts/create-account', user_login.CREATEACCOUNT,name="create-account"),
    path('dologin/', user_login.LOGIN,name="dologin"),
    path('logout/',user_login.LOGOUT,name='logout'),

    path('accounts/profile', user_login.PROFILE,name="profile"),
    path('accounts/profile/update', user_login.PROFILEUPDATE,name="profileupdate"),
    path('accounts/checkout', views.CHECKOUT,name='checkout'),
    path('accounts/order', user_login.ORDER,name='order'),
    path('accounts/order/create', user_login.CREATEORDER,name='create-order'),

    path('search/',views.SEARCH,name='search'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
