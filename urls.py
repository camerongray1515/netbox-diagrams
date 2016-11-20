from django.conf.urls import url
from diagrams.views import index

urlpatterns = [
    url(r'^$', index, name="index"),
]
