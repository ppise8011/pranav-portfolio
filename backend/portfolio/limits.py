import time,hmac,hashlib
from datetime import datetime,timezone
from django.conf import settings
from django.db import transaction
from django.db.models import F
from .models import RateWindow

def allowed(request,scope,limit=5,seconds=600):
 ip=request.META.get('REMOTE_ADDR','unknown')
 if settings.TRUST_PROXY:
  ip=request.META.get('HTTP_X_REAL_IP',ip)
 bucket=int(time.time())//seconds
 raw=f'{scope}:{ip}:{bucket}'.encode()
 key=hmac.new(settings.SECRET_KEY.encode(),raw,hashlib.sha256).hexdigest()
 with transaction.atomic():
  row,_=RateWindow.objects.get_or_create(key=key,defaults={'expires_at':datetime.fromtimestamp((bucket+1)*seconds,timezone.utc)})
  return bool(RateWindow.objects.filter(pk=row.pk,count__lt=limit).update(count=F('count')+1))
