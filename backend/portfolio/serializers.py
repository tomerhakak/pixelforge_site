from rest_framework import serializers
from .models import Service, Project # Import Project too if needed later
# Import Organization if you need to display its details, otherwise not needed for basic list/create
# from accounts.models import Organization

class ServiceSerializer(serializers.ModelSerializer):
    # Make organization read-only as it will be set automatically based on user
    organization = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'organization', 'title', 'description', 'icon_identifier', 'order')
        read_only_fields = ('id', 'organization')

# Add ProjectSerializer
class ProjectSerializer(serializers.ModelSerializer):
    # Make organization read-only
    organization = serializers.StringRelatedField(read_only=True)
    # Assuming image_url is generated in the model or view, make it read-only here
    image_url = serializers.CharField(read_only=True) # Make it CharField if it's a URL string

    class Meta:
        model = Project
        # Ensure 'image' field (ImageField) is excluded if you send 'image_url'
        fields = ('id', 'organization', 'title', 'description', 'image_url', 'link', 'technologies', 'order')
        read_only_fields = ('id', 'organization', 'image_url')

# You might add ProjectSerializer here later
# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ('id', 'title', 'description', 'image', 'link', 'technologies', 'order') 