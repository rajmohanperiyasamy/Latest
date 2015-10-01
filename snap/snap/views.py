from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from snap.models import Article,Project
from snap.models import Comment

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from django.views.decorators.csrf import csrf_protect
from snap.forms import *
from snap.forms import ArticleForm,ProjectForm,ProfileEditFormNew
from snap.forms import ImageUploadForm
def home(request):
    data={}
    snaps = "ProfileImage.objects.all()"
    data['snaps'] = snaps
    data['user']= request.user
    return render_to_response('index.html',data,context_instance=RequestContext(request))


def contacts(request):
    
    if request.method == 'POST': # If the form has been submitted...
        name = request.POST['fullname']
        user_mail = request.POST['email']
        subject = request.POST['subject']+"  from: "+user_mail
        message = request.POST['message']
        sender = 'rajmohan@doublespring.com'
        recipients = ['rajmohanjr@gmail.com']

        from django.core.mail import send_mail
        send_mail(subject, message, sender, recipients)
        return render_to_response('success_mail.html',context_instance=RequestContext(request))
    else:
        return render_to_response('contact.html',context_instance=RequestContext(request))



@csrf_protect
def register(request):
    data={}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/home/')
    else:
        form = RegistrationForm()
    return render_to_response('register.html',{'form':form },context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_page(request):
    
    return render_to_response('login.html',{'form':form },context_instance=RequestContext(request))

@login_required
def profile(request):
    form = ArticleForm()
    data={}
#     article = Article.objects.all().order_by('-id')[:10]
    try:
        article=Article.objects.filter(created_by=request.user)
    except:
        article=None
        pass
    data['user']= request.user
    data['form']= form
    data['article']= article
    return render_to_response('user_control_panel.html',data,context_instance=RequestContext(request))

@login_required  
def add_article(request,pk=0,template='user_control_panel.html'):
    data={}
    
    form = ArticleForm()
    if request.POST:
        form = ArticleForm(request.POST or None)
        if form.is_valid():
#             form.save()
            article = form.save(commit=False)
            article.created_by = request.user
            article.save()
            msg = "Article saved successfully"
            messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect('/home/')    
#     data['article_object']=article_object
    data['form']=form
    return render_to_response('user_control_panel.html',data,context_instance=RequestContext(request))


@login_required 
def ajax_add_article(request,pk=0,template='ajax_article_form.html'):
    print"yeeeeeeeeeeeeeh ureeeeeeeeeeeeka"
    data={}
    
    form = ArticleForm()
    if request.POST:
        form = ArticleForm(request.POST or None)
        if form.is_valid():
#             form.save()
            article = form.save(commit=False)
            article.created_by = request.user
            article.save()
            msg = "Article saved successfully"
            messages.success(request, msg)
        return HttpResponseRedirect('/home/')    
#     data['article_object']=article_object
    data['form']=form
    return render_to_response(template,data,context_instance=RequestContext(request))


@login_required
def edit_article(request,pk=0,template='user_control_panel.html'):
    data={}
    article_object= None
    try:
        article_object = Article.objects.get(id = pk)
        
        form = ArticleForm(instance=article_object)
    except:
        form = ArticleForm()
    if request.POST:
        if article_object== None:
            form = ArticleForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('/home')    
        else:
            article_object = Article.objects.get(id = pk)
            form =ArticleForm(request.POST or None, instance=article_object)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('/home')
    data['article_object']=article_object
    data['form']=form
    return render_to_response('user_control_panel.html',data,context_instance=RequestContext(request))

@login_required
def delete_article(request,pk=0,template='user_control_panel.html'):
    data={}
    art=Article.objects.get(id=pk)
    art.delete()
    article = Article.objects.all().order_by('-id')[:10]
    data['article']= article
    return render_to_response('user_control_panel.html',data,context_instance=RequestContext(request))


def display_article(request,pk=0,template='articles.html'):
    data={}
    article=Article.objects.all().order_by('-id')[:10]
    data['article']= article
    return render_to_response('articles.html',data,context_instance=RequestContext(request))

def display_projects(request):
    data={}
    projects=Project.objects.all().order_by('-id')[:10]
    data['projects']= projects
    return render_to_response('project_lists.html',data,context_instance=RequestContext(request))

def article_detail(request,pk=0,template='article-detail.html'):
    data={}
    article=Article.objects.get(id=pk)
    
    
    comment=Comment.objects.filter(article_id=pk).select_related('comment').order_by('-id')[:10]
    data['article']= article
    data['comment']=comment
    return render_to_response('article-detail.html',data,context_instance=RequestContext(request))

@login_required
def post_comment(request,pk=0,template='comments.html'):
    article_id=request.POST['id_article']
    article=Article.objects.get(id=article_id)
    data={}
    comment=Comment(comment=request.POST['comment'],commented_by=request.user,article=article)
    comment.save()
    str="/article-detail/"+article_id
    data['Comment']= comment
    return HttpResponseRedirect(str)





def upload_pic(request):
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data={}
    data['PROJECT_PATH']=PROJECT_PATH
    print"dddddddddddd succccc111111111111111111111111111"
    data={}
    if request.method == 'POST':
        print"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",request.FILES
        form = ImageUploadForm(request.POST, request.FILES or None)
        if form.is_valid():
            print"forrrrrrrrrrrrrrrrrrrrrr 11111111"
            form.save()
            return HttpResponse('image upload success')
        else:
                
            print"00000000000000000000000000000000000000",form.errors
    else:
        print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        form = ImageUploadForm()
        print"dddddddddddd succccccks 2222222222222222222222222",form
    
    return render_to_response('file-upload.html',{'form': form},context_instance=RequestContext(request))


def add_project(request):
    print"dddddddddddd succccc111111111111111111111111111"
    data={}
    if request.method == 'POST':
        print"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",request.FILES
        form = ProjectForm(request.POST, request.FILES or None)
        if form.is_valid():
            print"forrrrrrrrrrrrrrrrrrrrrr 11111111"
            form.save()
            return HttpResponse('image upload success')
        else:
                
            print"00000000000000000000000000000000000000",form.errors
    else:
        print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        form = ProjectForm()
        print"dddddddddddd succccccks 2222222222222222222222222",form
    
    return render_to_response('add_project.html',{'form': form},context_instance=RequestContext(request))

def profile_edit(request,template="profile.html"):
    data = {}
    
    user_object= None
    
    current_user = request.user
    usr_id=current_user.id
    try:
        user_object = User.objects.get(id = usr_id)
        
#         form = ProfileEditFormNew(instance=user_object)
        form = ProfileEditForm(instance=user_object)
    except:
#         form = ProfileEditFormNew()
        form = ProfileEditForm()
    
        
    if request.method == 'POST':
#         form = ProfileEditFormNew(request.POST,instance=request.user)
        form = ProfileEditForm(request.POST,instance=request.user)
        print"possssssssssst form",form
        if form.is_valid():
            user = form.save(commit=False)
            current_user = request.user
            print"rrrrrrrrrrrrrssssssssssssssssssssssssssssssssssrrr",current_user.id
            
            user.save()
            return HttpResponse('profile  image upload success')
           
        else:
            print" faileeeeed"
    return render_to_response(template, {'form':form,'profile':profile,},context_instance=RequestContext(request))