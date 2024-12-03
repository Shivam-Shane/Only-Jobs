from django.urls import path
from onlyjobs import views
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static

handler404=views.custom_404_view
urlpatterns = [
    path('', views.login_view, name='login'),  # Root URL renders login page
    path('sign_up/', views.sign_up_view, name='sign_up'),  # Sign-up URL
    path('home/', views.home, name='home'),  # Logout URL
    path('forget_password/', views.forget_password, name='forget_password'),
    path('logout/', views.logout, name='logout'),
    path('post_create', views.post_create, name='post_create'),
    path('verify_otp',views.verify_otp, name='verify_otp'),
    path('jobs/', views.jobs_listing, name='jobs'),
    path('notifications',views.notification,name='notification'),
    path('profile', views.profile_update, name='profile_update'),
    path('profilepicupdate',views.profile_picture_upload,name='profile_picture_upload')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)