from rest_framework import serializers
from Document.models import Document, clasificador


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('numb', 'user', 'Nombre', 'gps_northing', 'gps_easting','layers', 'gps_lat', 'gps_long')


class ObjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = clasificador

        fields = ('objetos', 'nombre', 'path', 'coordinatex', 'coordinatey', 'coordinatez', )





