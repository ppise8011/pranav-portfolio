import uuid
from pathlib import Path
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def cover_path(instance,filename):
 return f'projects/{uuid.uuid4().hex}{Path(filename).suffix.lower()}'

def validate_cover(value):
 if value.size > 5*1024*1024:
  raise ValidationError('Image must be 5 MB or smaller.')
 if Path(value.name).suffix.lower() not in {'.jpg','.jpeg','.png','.webp'}:
  raise ValidationError('Use a JPG, PNG or WebP image.')

def validate_tags(value):
 if not isinstance(value,list) or len(value)>12 or any(not isinstance(t,str) or len(t)>50 for t in value):
  raise ValidationError('Enter a JSON list of up to 12 short technology names.')

class Project(models.Model):
 title=models.CharField(max_length=120)
 slug=models.SlugField(unique=True)
 category=models.CharField(max_length=30,choices=[(x,x) for x in ['E-commerce','Brand websites','Education','Corporate','Web applications']])
 tagline=models.CharField(max_length=180)
 description=models.TextField(max_length=1500)
 details=models.TextField(max_length=5000,blank=True)
 url=models.URLField(blank=True)
 color=models.CharField(max_length=7,default='#d9cffb',validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$','Use a hex color such as #d9cffb.')])
 cover=models.ImageField(upload_to=cover_path,blank=True,validators=[validate_cover])
 image=models.CharField(max_length=250,blank=True,help_text='Bundled cover path, e.g. projects/oatful.webp. An uploaded cover takes priority.')
 technologies=models.JSONField(default=list,blank=True,validators=[validate_tags])
 role=models.CharField(max_length=150,default='Website development')
 status=models.CharField(max_length=50,default='Live website')
 featured=models.BooleanField(default=False)
 published=models.BooleanField(default=False)
 order=models.PositiveIntegerField(default=0)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta:
  ordering=['order','title']
 def __str__(self):return self.title

class Inquiry(models.Model):
 submission_id=models.UUIDField(unique=True,default=uuid.uuid4,editable=False)
 name=models.CharField(max_length=100)
 email=models.EmailField()
 company=models.CharField(max_length=150,blank=True)
 service=models.CharField(max_length=60)
 message=models.TextField(max_length=5000)
 consent=models.BooleanField(default=False)
 status=models.CharField(max_length=20,choices=[('new','New'),('contacted','Contacted'),('closed','Closed')],default='new')
 notes=models.TextField(blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 notification_sent_at=models.DateTimeField(null=True,blank=True)
 notification_error=models.CharField(max_length=200,blank=True)
 class Meta:
  ordering=['-created_at']
 def __str__(self):return f'{self.name} — {self.service}'

class RateWindow(models.Model):
 key=models.CharField(max_length=64,unique=True)
 count=models.PositiveIntegerField(default=0)
 expires_at=models.DateTimeField()
