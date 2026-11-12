from django import forms
SERVICES=['Website development','E-commerce store','Custom web application','Website improvements','Job opportunity','Something else']
class InquiryForm(forms.Form):
 name=forms.CharField(min_length=2,max_length=100)
 email=forms.EmailField(max_length=254)
 company=forms.CharField(max_length=150,required=False)
 service=forms.ChoiceField(choices=[(s,s) for s in SERVICES])
 message=forms.CharField(min_length=10,max_length=5000)
 consent=forms.BooleanField(required=True)
 submission_id=forms.UUIDField(required=True)
