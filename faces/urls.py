from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from faces.views import list, IndexView, results

urlpatterns = [
    url(r'^list/$', list, name='list'),
    url(r'^list/(?P<document_id>[0-9]+)/$', results, name='results'),
    url(r'^$', IndexView.as_view(), name='index'),
    ]