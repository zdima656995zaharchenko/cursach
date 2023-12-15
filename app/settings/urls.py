from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("currency.urls")),
    path('user/account/', include('user_account.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
