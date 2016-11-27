from django.conf.urls import url
import diagrams.views as views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^editor/(?P<diagram_id>\d+)?$', views.editor, name="editor"),
    url(r'^delete/([0-9]*)/$', views.delete, name="delete"),
    url(r'^export/([0-9]*)/$', views.export, name="export"),
    url(r'^api/update/$', views.update, name="update"),
    url(r'^api/create/$', views.create, name="create"),
    url(r'^api/rename/$', views.rename, name="rename"),
    url(r'^api/duplicate/$', views.duplicate, name="duplicate"),
]
