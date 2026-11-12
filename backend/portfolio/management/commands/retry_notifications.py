from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import Inquiry,RateWindow
from portfolio.notifications import notify
class Command(BaseCommand):
 help='Retry up to 100 pending inquiry notifications and clean expired throttle records. Run with one scheduler.'
 def handle(self,*args,**options):
  success=sum(notify(i) for i in Inquiry.objects.filter(notification_sent_at__isnull=True)[:100])
  RateWindow.objects.filter(expires_at__lt=timezone.now()).delete()
  self.stdout.write(f'{success} notification(s) sent.')
