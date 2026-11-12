import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
logger=logging.getLogger(__name__)
def notify(inquiry):
 if inquiry.notification_sent_at:return True
 if not settings.EMAIL_HOST:
  inquiry.notification_error='SMTP not configured; inquiry saved. Configure email and retry notifications.'
  inquiry.save(update_fields=['notification_error'])
  return False
 try:
  message=EmailMessage(subject='New portfolio inquiry',body=f'Name: {inquiry.name}\nEmail: {inquiry.email}\nCompany: {inquiry.company}\nService: {inquiry.service}\n\n{inquiry.message}',from_email=settings.DEFAULT_FROM_EMAIL,to=[settings.INQUIRY_NOTIFY_EMAIL],reply_to=[inquiry.email])
  if message.send()!=1:raise RuntimeError('No message delivered')
  inquiry.notification_sent_at=timezone.now()
  inquiry.notification_error=''
  inquiry.save(update_fields=['notification_sent_at','notification_error'])
  return True
 except Exception:
  logger.warning('Notification failed for inquiry %s; retained for retry.',inquiry.pk)
  inquiry.notification_error='SMTP delivery failed. Check server email settings and retry.'
  inquiry.save(update_fields=['notification_error'])
  return False
