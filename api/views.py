from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserSubmission, EmailTemplate, AdditionalEmail
from .serializers import UserSubmissionSerializer, EmailTemplateSerializer, AdditionalEmailSerializer
from .services import EmailService

class UserSubmissionView(generics.ListCreateAPIView):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

class EmailTemplateView(generics.ListCreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

class AdditionalEmailView(generics.ListCreateAPIView):
    queryset = AdditionalEmail.objects.all()
    serializer_class = AdditionalEmailSerializer


class SendMailView(APIView):
    def post(self, request):
        template_id = request.data.get('template_id')
        recipient_type = request.data.get('recipient_type', 'all')
        
        try:
            template = EmailTemplate.objects.get(id=template_id)
            recipients = []
            
            # Gather recipients based on type
            if recipient_type in ['all', 'submissions']:
                submissions = UserSubmission.objects.all()
                recipients.extend(submissions)
            
            if recipient_type in ['all', 'additional']:
                additional = AdditionalEmail.objects.all()
                recipients.extend(additional)
            
            # Send emails
            try:
                EmailService.send_bulk_email(template, recipients)
                return Response({
                    'message': 'Emails sent successfully',
                    'recipient_count': len(recipients)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f'Failed to send emails: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except EmailTemplate.DoesNotExist:
            return Response({
                'error': 'Template not found'
            }, status=status.HTTP_404_NOT_FOUND)