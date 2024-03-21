from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.register, name='register'),
    path('register', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('upload/', views.convert_pdf_to_audio,
         name='upload_pdf'),
    path('audio/<int:pk>/', views.download_audio,
         name='audio_download'),
    path('view-files/', views.view_files, name='view_files'),
    path('logout/', views.user_logout, name='logout'),
    path('delete-file/', views.delete_file, name='delete_file'),
    path('pdf-to-audio/', views.pdf_to_audio,
         name='pdf_to_audio'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
