from rest_framework import generics, permissions
# from dj_rest_auth.registration.views import RegisterView # No longer needed
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework import status
from .serializers import CustomRegisterSerializer

# Change inheritance to CreateAPIView
# class CustomRegisterView(RegisterView):
class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to register

    # No need to override post method anymore, CreateAPIView handles it using the serializer.
    # def post(self, request, *args, **kwargs):
    #     print("--- CustomRegisterView POST method called! ---") 
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True) 
    #         # user = self.perform_create(serializer) # CreateAPIView does this
    #         self.perform_create(serializer) # Call perform_create which calls serializer.save()
    #         # headers = self.get_success_headers(serializer.data)
    #         # data = self.get_response_data(user)
    #         # return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    #         # Simplified response for now
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except ValidationError as e:
    #         print("--- CustomRegisterView VALIDATION ERROR CAUGHT ---")
    #         print("Validation Errors:", e.detail)
    #         return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         print(f"--- CustomRegisterView UNEXPECTED ERROR: {type(e).__name__} ---")
    #         print(f"Error details: {e}")
    #         return Response({"error": "An unexpected server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 