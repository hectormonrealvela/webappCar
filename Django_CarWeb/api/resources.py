from rest_framework import viewsets
from Document.models import Document, clasificador



from .serializers import ListSerializer, ObjectsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

class api_document(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    __basic_fields = ('numb','user','Nombre','gps_northing', 'gps_easting','layers', 'gps_lat', 'gps_long')
    search_fields = __basic_fields


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class api_clasificador(viewsets.ModelViewSet):
    queryset = clasificador.objects.all()
    serializer_class = ObjectsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    __basic_fields = ('objetos', 'nombre', 'path', 'coordinatex', 'coordinatey', 'coordinatez')
    search_fields = __basic_fields













