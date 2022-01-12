from django.contrib import admin
from django.urls import path
from .views import listview, signupview, loginview, logoutview, rtcreateview, evcreateview,\
     tdcreateview, TrDetail, TrCreate, TrDelete, TrUpdate, RtDelete, RtUpdate, EvDelete, EvUpdate,\
     TdDelete, TdUpdate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', listview, name="list"),
    path('signup/', signupview, name="signup"),
    path('login/', loginview, name="login"),
    path('logout/', logoutview, name="logout"),
    path('detail/<int:pk>/', TrDetail.as_view(), name="detail"),

    path('trcreate/', TrCreate.as_view(), name="trcreate"),
    path('trdelete/<int:pk>/', TrDelete.as_view(), name="trdelete"),
    path('trupdate/<int:pk>/', TrUpdate.as_view(), name="trupdate"),

    path('rtcreate/<int:pk>/', rtcreateview, name="rtcreate"),
    path('rtdelete/<int:pk>/', RtDelete.as_view(), name="rtdelete"),
    path('rtupdate/<int:pk>/', RtUpdate.as_view(), name="rtupdate"),

    path('evcreate/<int:pk>/', evcreateview, name="evcreate"),
    path('evdelete/<int:pk>/', EvDelete.as_view(), name="evdelete"),
    path('evupdate/<int:pk>/', EvUpdate.as_view(), name="evupdate"),

    path('tdcreate/<int:pk>/', tdcreateview, name="tdcreate"),
    path('tddelete/<int:pk>/', TdDelete.as_view(), name="tddelete"),
    path('tdupdate/<int:pk>/', TdUpdate.as_view(), name="tdupdate"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +\
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
