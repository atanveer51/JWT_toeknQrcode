from .models import Student
from .serializers import StudentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views import View
from django.http import HttpResponse
from qrcode import make as make_qr_code
from io import BytesIO
from PIL import Image
from rest_framework import generics, permissions
from rest_framework.response import Response
# from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
class StudentModelViewSet(viewsets.ModelViewSet):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  authentication_classes=[JWTAuthentication]
  permission_classes=[IsAuthenticated]


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "message": "User Created Successfully.  Now perform Login to get your token"
        })


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('access')
        refresh_token = response.data.get('refresh') #data['refresh']
        # Optionally, you can also access the refresh token using `response.data.get('refresh')`
        # Do any additional processing or data manipulation if needed
        # Return the token in the response
        return Response({'token': token,"refresh token":refresh_token})


class TokenToQRCodeView(View):
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get('access_token')  # Assuming access_token is passed as a query parameter
        print("access_token",access_token)
        if access_token:
            qr_code = make_qr_code(access_token)
            qr_code_image = qr_code.get_image()

            # Resize the image
            new_size = (300, 300)  # Adjust the dimensions as per your requirements
            qr_code_image = qr_code_image.resize(new_size)

            buffer = BytesIO()
            qr_code_image.save(buffer, format='PNG')
            qr_code_image_data = buffer.getvalue()
            response = HttpResponse(content_type='image/png')
            response.write(qr_code_image_data)
            return response
        else:
            return HttpResponse('No access token provided.', status=400)
