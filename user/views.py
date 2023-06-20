from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .models import User, Product
from .serializers import UserSerializer, ProductSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username, password=password).first()
    if user:
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token})

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def product(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
