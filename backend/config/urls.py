from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from portfolio import views
urlpatterns=[path('admin/',admin.site.urls),path('api/csrf/',views.csrf),path('api/projects/',views.projects),path('api/inquiries/',views.inquiries),path('',views.home)]
if settings.DEBUG:urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
