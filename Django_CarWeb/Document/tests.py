from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from Document.models import clasificador

class AccountTests(APITestCase):
    def test_create_customer(self):
        url = reverse('clasificador-list')
        data = {
            'objetos': 'Coche',
            'nombre': 'test_api',
            'coordinatex': '18.875294',
            'coordinatey': '23.968998',
            'coordinatez': '1.4227511'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(clasificador.objects.count(), 1)
        self.assertEqual(clasificador.objects.get().nombre, 'test_api')



