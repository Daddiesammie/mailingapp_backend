from django.contrib import admin
from django.contrib import messages
from .models import UserSubmission, EmailTemplate, AdditionalEmail
from .services import EmailService

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email')

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    search_fields = ('name', 'subject')
    actions = ['send_email_to_all', 'send_email_to_submissions', 'send_email_to_additional']

    def send_email_to_all(self, request, queryset):
        for template in queryset:
            recipients = list(UserSubmission.objects.all()) + list(AdditionalEmail.objects.all())
            EmailService.send_bulk_email(template, recipients)
            messages.success(request, f'Email "{template.name}" sent to {len(recipients)} recipients')
    send_email_to_all.short_description = "Send selected template to all recipients"

    def send_email_to_submissions(self, request, queryset):
        for template in queryset:
            recipients = list(UserSubmission.objects.all())
            EmailService.send_bulk_email(template, recipients)
            messages.success(request, f'Email "{template.name}" sent to {len(recipients)} form submissions')
    send_email_to_submissions.short_description = "Send selected template to form submissions only"

    def send_email_to_additional(self, request, queryset):
        for template in queryset:
            recipients = list(AdditionalEmail.objects.all())
            EmailService.send_bulk_email(template, recipients)
            messages.success(request, f'Email "{template.name}" sent to {len(recipients)} additional emails')
    send_email_to_additional.short_description = "Send selected template to additional emails only"

@admin.register(AdditionalEmail)
class AdditionalEmailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
