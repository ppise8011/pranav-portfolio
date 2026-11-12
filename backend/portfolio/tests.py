import json,uuid,io
from unittest.mock import patch
from django.test import TestCase,Client,override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.core.management import call_command
from .models import Project,Inquiry,RateWindow,validate_cover
from .notifications import notify

class PortfolioTests(TestCase):
 def setUp(self):
  self.client=Client(enforce_csrf_checks=True)
  self.token=self.client.get('/api/csrf/').json()['token']
  self.payload={'name':'Test Visitor','email':'visitor@example.com','company':'Example','service':'Website development','message':'Please discuss a new website project.','consent':True,'submission_id':str(uuid.uuid4()),'website':''}
 def post(self,payload=None,csrf=True):
  headers={'HTTP_X_CSRFTOKEN':self.token} if csrf else {}
  return self.client.post('/api/inquiries/',data=json.dumps(payload or self.payload),content_type='application/json',**headers)
 def test_inquiry_is_saved_and_private(self):
  self.assertEqual(self.post().status_code,201)
  self.assertEqual(Inquiry.objects.count(),1)
  self.assertEqual(self.client.get('/api/inquiries/').status_code,405)
  self.assertEqual(self.client.get('/admin/portfolio/inquiry/').status_code,302)
 def test_csrf_required(self):
  self.assertEqual(self.post(csrf=False).status_code,403)
  self.assertEqual(Inquiry.objects.count(),0)
 def test_invalid_fields_rejected(self):
  for key,value in [('email','bad'),('message','short'),('consent',False),('consent','false'),('name','x'*101),('website','spam')]:
   self.assertEqual(self.post({**self.payload,key:value}).status_code,400)
  self.assertEqual(Inquiry.objects.count(),0)
 def test_duplicate_request_does_not_duplicate_record(self):
  self.assertEqual(self.post().status_code,201)
  self.assertEqual(self.post().status_code,200)
  self.assertEqual(Inquiry.objects.count(),1)
 def test_rate_limit(self):
  for _ in range(5):self.assertEqual(self.post({**self.payload,'submission_id':str(uuid.uuid4())}).status_code,201)
  self.assertEqual(self.post({**self.payload,'submission_id':str(uuid.uuid4())}).status_code,429)
 def test_published_projects_only_and_order(self):
  for slug,order,published in [('later',2,True),('first',1,True),('draft',0,False)]:
   Project.objects.create(title=slug,slug=slug,order=order,published=published)
  rows=self.client.get('/api/projects/').json()['projects']
  self.assertEqual([p['slug'] for p in rows],['first','later'])
 def test_admin_login_and_project_mutation(self):
  user=get_user_model().objects.create_superuser('reviewer','reviewer@example.com','long-test-password-2026')
  self.client.force_login(user)
  self.assertEqual(self.client.get('/admin/portfolio/project/').status_code,200)
  p=Project.objects.create(title='Preview',slug='preview',published=False)
  self.assertEqual(len(self.client.get('/api/projects/').json()['projects']),0)
  p.published=True;p.save()
  self.assertEqual(len(self.client.get('/api/projects/').json()['projects']),1)
 def test_reject_unsafe_cover(self):
  with self.assertRaises(ValidationError):validate_cover(SimpleUploadedFile('bad.svg',b'<svg/>'))
  with self.assertRaises(ValidationError):validate_cover(SimpleUploadedFile('large.png',b'x'*(5*1024*1024+1)))
 @override_settings(EMAIL_HOST='smtp.example.com')
 @patch('portfolio.notifications.EmailMessage.send',side_effect=RuntimeError('SMTP unavailable'))
 def test_email_failure_keeps_inquiry(self,send):
  self.assertEqual(self.post().status_code,201)
  inquiry=Inquiry.objects.get()
  self.assertIsNone(inquiry.notification_sent_at)
  self.assertTrue(inquiry.notification_error)
 @override_settings(EMAIL_HOST='smtp.example.com',EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
 def test_email_sent_and_not_repeated(self):
  from django.core import mail
  self.assertEqual(self.post().status_code,201)
  inquiry=Inquiry.objects.get()
  self.assertIsNotNone(inquiry.notification_sent_at)
  notify(inquiry)
  self.assertEqual(len(mail.outbox),1)
  self.assertEqual(mail.outbox[0].reply_to,['visitor@example.com'])
 def test_seed_is_idempotent(self):
  call_command('seed_projects',stdout=io.StringIO())
  count=Project.objects.count()
  p=Project.objects.first();p.title='Owner edit';p.save()
  call_command('seed_projects',stdout=io.StringIO())
  self.assertEqual(Project.objects.count(),count)
  self.assertTrue(Project.objects.filter(title='Owner edit').exists())
 def test_malformed_json_rejected(self):
  response=self.client.post('/api/inquiries/',data='[1,2]',content_type='application/json',HTTP_X_CSRFTOKEN=self.token)
  self.assertEqual(response.status_code,400)
 def test_admin_can_add_project_with_cover(self):
  import tempfile
  from PIL import Image
  user=get_user_model().objects.create_superuser('uploader','uploader@example.com','long-test-password-2026')
  admin_client=Client();admin_client.force_login(user)
  buffer=io.BytesIO();Image.new('RGB',(20,20),'purple').save(buffer,format='PNG')
  with tempfile.TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
   response=admin_client.post('/admin/portfolio/project/add/',{'title':'Uploaded project','slug':'uploaded-project','category':'Corporate','tagline':'A test cover','description':'Local admin upload verification.','details':'','url':'https://example.com/','color':'#d9cffb','cover':SimpleUploadedFile('cover.png',buffer.getvalue(),content_type='image/png'),'image':'','technologies':'[]','role':'Website development','status':'Live website','featured':'on','published':'on','order':'1','_save':'Save'})
   self.assertEqual(response.status_code,302)
   project=Project.objects.get(slug='uploaded-project')
   self.assertTrue(project.cover.storage.exists(project.cover.name))
   row=self.client.get('/api/projects/').json()['projects'][0]
   self.assertTrue(row['image'].startswith('/media/projects/'))
