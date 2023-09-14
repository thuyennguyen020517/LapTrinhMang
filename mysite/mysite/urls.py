
from django.conf import settings
from django.views.static import serve
from django.urls import re_path as url

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from store import views as store_views
from account import views as account_views

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('store/',include('store.urls')),
    path('admin/', admin.site.urls),
    path('auth', include('account.urls')),
    path('login', account_views.login_view, name='login'),
    path('', account_views.index, name='index'),
    path('logout/', account_views.logout_view, name='logout_view'),
    path('shopping', include('shopping.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)