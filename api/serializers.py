from rest_framework import serializers
from .models import UserSubmission, EmailTemplate, AdditionalEmail

class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = '__all__'

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'

class AdditionalEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalEmail
        fields = '__all__'
