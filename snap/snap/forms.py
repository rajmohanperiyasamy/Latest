from django import forms
from django.forms import ModelForm
from snap.models import Article,ExampleModel,Project,UserProfile,UserProfileNew
from django.utils.translation import ugettext as _

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['created_by']
        fields = ['title', 'article_subject', 'summary',]
    title = forms.CharField(required=True,widget=forms.TextInput(attrs={'required':True,'maxlength':250,'class': 'text-long', 'placeholder': "Enter the title about this article"}))
    article_subject = forms.CharField(required=True,widget=forms.TextInput(attrs={'required':True,'maxlength':250,'class': 'text-long', 'placeholder': "Enter the subject"}))
    summary = forms.CharField(required=True,widget=forms.Textarea(attrs={'required':True,'maxlength':2500, 'rows': '4','class': 'iSp8', 'placeholder': "Enter the content concerning about this article in this text box"}))

class ProfileImageForm(forms.Form):
    image = forms.FileField(label='Select a profile Image')
    
    
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
    
    
class ImageUploadForm(ModelForm):
    """Image upload form."""
    class Meta:
        model = ExampleModel
        fields = ['model_pic']
#     def clean_model_pic(self):
#         print"cccccccccccccca lllllllllllllllll eeeeeeeeeeddddddddddd"
#         image = self.cleaned_data.get('model_pic', False)
#         if image:
#                 raise ValidationError("Image file too large ( maximum 1mb )")
#         else:
#             raise forms.ValidationError(_("Couldn't read uploaded image"))
#         return None
    
class ProjectForm(ModelForm):
    """Image upload form."""
    class Meta:
        model = Project
        
        
        
class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','prof_pic','home_address','phone_number']
        
class ProfileEditFormNew(forms.ModelForm):

    class Meta:
        model = UserProfileNew