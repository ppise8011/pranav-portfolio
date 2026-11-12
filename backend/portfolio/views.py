import json
from django.conf import settings
from django.http import JsonResponse,FileResponse,HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET,require_POST
from django.views.decorators.cache import never_cache
from django.db import transaction
from .models import Project,Inquiry
from .forms import InquiryForm
from .limits import allowed
from .notifications import notify

@require_GET
@never_cache
def csrf(request):return JsonResponse({'token':get_token(request)})

def csrf_failure(request,reason=''):
 return JsonResponse({'error':'Your session could not be verified. Refresh the page and try again.'},status=403)

@require_GET
@never_cache
def projects(request):
 fields=['slug','title','category','tagline','description','details','url','color','image','technologies','role','status','featured','order']
 data=[]
 for project in Project.objects.filter(published=True):
  row={f:getattr(project,f) for f in fields}
  if project.cover:row['image']=project.cover.url
  data.append(row)
 return JsonResponse({'projects':data})

@require_POST
def inquiries(request):
 if request.content_type!='application/json':return JsonResponse({'error':'Send JSON content.'},status=415)
 if len(request.body)>16000:return JsonResponse({'error':'Your message is too large.'},status=413)
 try:data=json.loads(request.body)
 except (ValueError,UnicodeError):return JsonResponse({'error':'Invalid JSON.'},status=400)
 if not isinstance(data,dict):return JsonResponse({'error':'Invalid inquiry.'},status=400)
 if data.get('website'):return JsonResponse({'error':'Unable to accept this inquiry.'},status=400)
 if data.get('consent') is not True:return JsonResponse({'error':'Please agree to share your details so I can reply.'},status=400)
 form=InquiryForm(data)
 if not form.is_valid():
  return JsonResponse({'error':'Please check the form fields. '+ ' '.join(f'{key}: {errors[0]}' for key,errors in form.errors.items())},status=400)
 cleaned=form.cleaned_data
 if not allowed(request,'inquiry',5,600):
  response=JsonResponse({'error':'Too many inquiries. Please try again in 10 minutes or email me directly.'},status=429)
  response['Retry-After']='600'
  return response
 # UUID idempotency prevents duplicate records after a browser/network retry.
 with transaction.atomic():
  inquiry,created=Inquiry.objects.get_or_create(submission_id=cleaned.pop('submission_id'),defaults=cleaned)
 if created:notify(inquiry)
 return JsonResponse({'ok':True,'message':'Your inquiry has been received.'},status=201 if created else 200)

@require_GET
def home(request):
 path=settings.FRONTEND_DIST/'index.html'
 if not path.exists():return HttpResponse('Build the frontend first: cd frontend && npm install && npm run build',status=503,content_type='text/plain')
 return FileResponse(path.open('rb'),content_type='text/html')
