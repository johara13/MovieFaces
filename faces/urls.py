from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from faces.views import list, IndexView

urlpatterns = [
    url(r'^list/$', list, name='list'),
    url(r'^$', IndexView.as_view(), name='index'),
    ]