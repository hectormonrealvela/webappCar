from django.urls import path, include


from django.conf.urls import url

from .views import *


from rest_framework import routers
from api.resources import *


router = routers.DefaultRouter()
router.register(r'api/plot', api_document)
router.register(r'api/objects', api_clasificador)


urlpatterns = [

    url(r'^$', LoginFormView.as_view(), name='login'),
    url(r'^simple/', login_required(simple_upload), name='simple_upload'),
    url(r'^list/', login_required(list.as_view()), name='list'),
    path('<int:id>/delete/', login_required(delete_view), name='delete'),
    url(r'^(?P<numb>\d+)/create_image/$', login_required(create_image), name='plot'),
	url(r'^register/$', RegisterFormView.as_view(), name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^prueba/$', prueba, name='prueba'),
    url(r'^edit/', login_required(change_password), name='edit'),
    url(r'^test_api/', api_test,name='test_api'),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))


]



