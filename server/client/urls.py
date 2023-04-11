from django.urls import path
from .import views
from .models import UserModel

# images urls 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authentication urls start 
    path('login', views.LoginPage,name="login"),
    path('logout', views.LogoutUser,name="logout"),
    # Authentication urls end

    path('authorization',views.adminOnly,name='authorization'),
    path('',views.IndexView,name='index'),
    path('create-ticket',views.TicketForm,name='create-ticket'),
    path('ticket/<int:id>',views.TicketDetailsModel,name='ticket'),
    path('download_pdf/<int:id>',views.PDFTemplate,name='download_pdf'),
     path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

