from django.contrib import admin,messages
from .models import Project,Inquiry
from .notifications import notify
admin.site.site_header='Pranav Pise · Portfolio Studio'
admin.site.site_title='Portfolio Studio'
admin.site.index_title='Manage projects and inquiries'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
 list_display=['title','category','featured','published','order','updated_at']
 list_editable=['featured','published','order']
 list_filter=['category','featured','published']
 search_fields=['title','description']
 prepopulated_fields={'slug':('title',)}
 fieldsets=[('Project',{'fields':('title','slug','category','tagline','description','details','role','status','technologies','url')}),('Visuals',{'fields':('cover','image','color')}),('Publishing',{'fields':('published','featured','order')})]

@admin.action(description='Mark selected inquiries as contacted')
def contacted(modeladmin,request,queryset):queryset.update(status='contacted')
@admin.action(description='Retry email notifications')
def retry(modeladmin,request,queryset):
 success=sum(notify(item) for item in queryset.filter(notification_sent_at__isnull=True))
 modeladmin.message_user(request,f'{success} notification(s) delivered.',messages.INFO)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
 list_display=['name','email','service','status','created_at','notification_sent_at']
 list_filter=['status','service','created_at']
 search_fields=['name','email','company','message']
 readonly_fields=['submission_id','name','email','company','service','message','consent','created_at','notification_sent_at','notification_error']
 actions=[contacted,retry]
 def has_add_permission(self,request):return False
