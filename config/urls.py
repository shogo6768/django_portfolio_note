from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import TopPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TopPage.as_view(), name='toppage'),
    path('blog/', include('blogs.urls')),
    path('accounts/', include('accounts.urls')),
    path('qa/', include('QA.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('upload/', login_required(views.upload), name='ckeditor_upload'),
    path('browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
