from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login1,name='login'),
    path('signup/',views.signup1,name='signup'),
    path('logout/',views.logout1,name='logout'),
    path('addcart/<int:uid>/',views.addcart,name='addcart'),
    path('viewcart/',views.viewcart,name='viewcart'),
    path('removeitem/<int:uid>/',views.removeitem,name='removeitem'),
    path('increment/<int:uid>/',views.increment,name='increment'),
    path('decrement/<int:uid>/',views.decrement,name='decrement'),
]
if(settings.DEBUG):
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)