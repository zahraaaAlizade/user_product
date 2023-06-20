from django.test import TestCase
import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import User, Product
from .serializers import UserSerializer, ProductSerializer

client = Client()


class TokenTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_token_valid(self):
        response = client.post(reverse('token'), {'username': 'testuser', 'password': 'testpassword'},
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue('token' in response.json())

    def test_token_invalid(self):
        response = client.post(reverse('token'), {'username': 'testuser', 'password': 'wrongpassword'},
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue('error' in response.json())


class ProductTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.product = Product.objects.create(title='Test Product', description='Test Description', price=100,
                                              creator=self.user)

    def test_product_list(self):
        response = client.get(reverse('product'))

        products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), serializer.data)

    def test_product_create(self):
        client.login(username='testuser', password='testpassword')

        response = client.post(reverse('product'),
                               {'title': 'New Product', 'description': 'New Description', 'price': 200},
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Product.objects.count(), 2)

        self.assertEqual(Product.objects.last().title, 'New Product')

        self.assertEqual(Product.objects.last().description, 'New Description')

        self.assertEqual(Product.objects.last().price, 200)

        self.assertEqual(Product.objects.last().creator, self.user)

    def test_product_create_unauthorized(self):
        response = client.post(reverse('product'),
                               {'title': 'New Product', 'description': 'New Description', 'price': 200},
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
