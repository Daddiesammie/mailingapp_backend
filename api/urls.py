from django.urls import path
from . import views

urlpatterns = [
    path('submissions/', views.UserSubmissionView.as_view(), name='user-submissions'),
    path('templates/', views.EmailTemplateView.as_view(), name='email-templates'),
    path('templates/<int:pk>/', views.EmailTemplateDetailView.as_view(), name='template-detail'),
    path('additional-emails/', views.AdditionalEmailView.as_view(), name='additional-emails'),
    path('send-mail/', views.SendMailView.as_view(), name='send-mail'),
]
