from django.shortcuts import render,redirect,get_object_or_404
from django.http import FileResponse,HttpResponse
from .models import Board,Topic,Post,Patients as Patient_Model,News,Visit,Photo
from time import strftime
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from arabic import convert
from clinic_bill import clinic_temp
from reportlab.lib.units import inch,mm
from reportlab.lib.pagesizes import A5
from django.contrib.auth.models import User
from .forms import Topic_form,Post_form,Patient_form,News_form,Visit_form,Media_form
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,UpdateView,ListView,DeleteView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
#

def main(request):
    boards=Board.objects.all()
    news=News.objects.all()
    return render(request,'home/main.html',{'boards':boards,'news':news})
def board(request,board_id):
    board=get_object_or_404(Board,id=board_id)
    query_set=board.topics.order_by('-created_at').annotate(comments=Count('posts'))
    paginator=Paginator(query_set,6)
    page=request.GET.get('page',1)
    try:
        topic_post_count=paginator.page(page)
    except PageNotAnInteger:
        topic_post_count=paginator.page(1)
    except EmptyPage:
        topic_post_count=paginator.page(paginator.num_pages)
    return render(request,"home/board.html",{'board':board,"topics":topic_post_count})
def topic(request,board_id,topic_id):
    board=get_object_or_404(Board,id=board_id)
    topic=get_object_or_404(Topic,id=topic_id,board=board)
    session=f"ali-{topic.id}"
    if not request.session.get(session):
        topic.views+=1
        topic.save()
        request.session[session]=True
    return render(request,"home/topic.html",{'board':board,'topic':topic})
@login_required
def new_topic(request,board_id):
    board=get_object_or_404(Board,id=board_id)
    if request.method=="POST":
        form=Topic_form(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            # user=User.objects.first()
            user=request.user
            topic.board=board
            topic.created_by=user
            topic.save()
            message=form.cleaned_data.get("message")
            post=Post.objects.create(message=message,topic=topic,created_by=user)
            return redirect("board",board.id)
    else:
        form=Topic_form()
    return render(request,"home/new_topic.html",{'board':board,'form':form})
@login_required
def reply(request,board_id,topic_id):
    board=get_object_or_404(Board,id=board_id)
    topic=get_object_or_404(Topic,id=topic_id,board=board)
    if request.method=="POST":
        form=Post_form(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.topic=topic
            message.created_by=request.user
            message.save()
            topic.updated_by=request.user
            topic.updated_at=timezone.now()
            topic.save()
            return redirect('topic',board.id,topic.id)
    else:
        form=Post_form()
    return render(request,"home/reply.html",{'topic':topic,'form':form})

#cbv
# patients
class New_visit(View):
    def render(self,request,form):
        return render(request,"home/new_visit.html",{'form':form})
    def post(self, request,**kwargs):
        date=strftime("%Y-%m-%d")
        id=self.kwargs['patient_id']
        patient=get_object_or_404(Patient_Model,pk=id)
        try:
            visit=Visit.objects.get(date=date)
        except Visit.DoesNotExist:
            visit=None
        if request.method=="POST":
            form=Visit_form(request.POST,request.FILES)
            file=request.FILES.get('file')
            image=request.FILES.get('image')
            # file=form.cleaned_data.get('file')#not used because it need form.save()
            if form.is_valid():
                if visit is None:
                    new_visit=form.save()
                    new_visit.patient.add(patient)
                    patient.visits +=1
                    patient.save()
                    photo=Photo.objects.create(images=image,file=file,patient=patient,visit=new_visit)
                else:
                    if visit not in patient.visit.all():
                        patient.visits +=1
                        patient.save()
                        visit.patient.add(patient)
                        photo=Photo.objects.create(images=image,file=file,patient=patient,visit=visit)
                return redirect('patient',patient.id)
        return self.render(request,form)
    def get(self,request,**kwargs):
        form=Visit_form()
        return self.render(request,form)
# gbv
@method_decorator(login_required,name='dispatch')
class Add_Patient(CreateView):
    model=Patient_Model
    form_class=Patient_form
    success_url=reverse_lazy("patients")
    template_name="home/add_patient.html"  
@method_decorator(login_required,name='dispatch')
class Edit_post(UpdateView):
    model=Post
    # form_class=Post_form
    fields=['message']
    pk_url_kwarg='post_id'
    template_name="home/update_post.html"
    context_object_name="post"
    def form_valid(self, form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.created_at=timezone.now()
        post.save()
        return redirect("topic",post.topic.board.id,post.topic.id)
@method_decorator(login_required,name='dispatch')
class Patients(ListView):
    model=Patient_Model
    context_object_name='patients'
    template_name="home/patients.html"
def get_patient(request,patient_id):
    patient=get_object_or_404(Patient_Model,pk=patient_id)
    return render(request,"home/patient.html",{'patient':patient})
class New_news(CreateView):
    model=News
    form_class=News_form
    # success_url=reverse_lazy('main')#not use in creative
    template_name="home/new_news.html"
    def form_valid(self, form):
        news=form.save(commit=False)
        news.created_by=self.request.user
        news.save()
        return redirect("main")
def add_media(request,patient_id):
    date=strftime("%Y-%m-%d")
    patient=get_object_or_404(Patient_Model,pk=patient_id)
    visit=get_object_or_404(Visit,date=date,patient__id=patient_id)#to go from son __
    if request.method=="POST":
        form=Media_form(request.POST,request.FILES)#should add post & files
        if form.is_valid():
            media=form.save(commit=False)
            media.patient=patient
            media.visit=visit
            media.added_at=timezone.now()
            media.save()
            return redirect('patient',patient.id)

    else:
        form=Media_form()
    return render(request,'home/add_media.html',{'form':form})
class Edit_media(UpdateView):

    model=Photo
    form_class=Media_form
    pk_url_kwarg='photo_id'
    context_object_name="photo"
    # success_url=reverse_lazy('main')
    template_name="home/edit_media.html"
    
    def form_valid(self, form):
        date=strftime("%Y-%m-%d")
        photo=self.get_object()
        photo_id=photo.id
        patient=photo.patient
        visit=get_object_or_404(Visit,date=date,patient__id=patient.id)
        new_photo=form.save(commit=False)
        new_photo.patient=patient
        new_photo.added_at=timezone.now()
        new_photo.save()
        return redirect('patient',patient.id)
        #or
        # photo=self.get_queryset().first()
        # patient=photo.patient
       
def delete_media(request,patient_id,photo_id):
    photo=get_object_or_404(Photo,pk=photo_id)
    delete_choice=request.GET.get('choice')
    if request.method=='POST':
        if delete_choice=='image':
            photo.images.delete()
        else:
            photo.file.delete()
        
        return redirect('patient',patient_id)
    return render(request,'home/delete_media.html',{'photo':photo,'choice':delete_choice})
class Edit_patient(UpdateView):
    model=Patient_Model
    form_class=Patient_form
    context_object_name='patient'
    # success_url=reverse_lazy('main')
    pk_url_kwarg='patient_id'
    template_name='home/update_patient.html'
    def form_valid(self, form):
        patient=form.save()
        return redirect('patients')
class Delete_patient(DeleteView):
    model=Patient_Model
    pk_url_kwarg='patient_id'
    success_url=reverse_lazy('patients')
    context_object_name='patient'
    template_name='home/delete_patient.html'
class Delete_news(DeleteView):
    model=News
    pk_url_kwarg='news_id'
    success_url=reverse_lazy('main')
    context_object_name='news'
    template_name='home/delete_news.html'

class Edit_news(UpdateView):
    model=News
    fields=['name','content']
    pk_url_kwarg='news_id'
    success_url=la=reverse_lazy('main')
    template_name='home/edit_news.html'
# def create_pill(request,patient_id):
#     # date=strftime("%Y-%m-%d")
#     patient=get_object_or_404(Patient_Model,pk=patient_id)
#     if request.method=='POST':
#         date=request.POST.get('date')
#         patient_path=f"{patient.name}-{date}.pdf"
#         path=os.path.join('media/pdfs',patient_path)
#         c=canvas.Canvas(path,pagesize=A5)
#         c=clinic_temp(c)
#         name=request.POST.get('name')
#         age=request.POST.get('age')
#         gender=request.POST.get('gender')
#         item1=request.POST.get('item1')
#         item2=request.POST.get('item2')
#         item3=request.POST.get('item3')
#         item4=request.POST.get('item4')
#         item5=request.POST.get('item5')
#         items=[item1,item2,item3,item4,item5]
#         c.setFillColor("red")
#         c.setFont("Arabic",12)#come from pdfmetrics in setting
#         c.drawString(3*inch,5.1*inch,convert(name))
#         c.drawString(0.1*inch,5.1*inch,convert(date))
#         c.drawString(4*inch,4.8*inch,convert(age))
#         c.drawString(0.1*inch,4.8*inch,convert(gender))
#         y=4*inch
#         for item in items:
#             c.drawString(0.1*inch,y,f"{items.index(item)+1} - {item}")
#             y-=30
#         c.showPage()
#         c.save()
#     return render (request,'home/make_pill.html',{'patient':patient})
# def download_file(request,patient_id):
#     path=request.GET['path']
#     file_path = os.path.join(settings.MEDIA_ROOT,path)
#     if os.path.exists(file_path):
#         return FileResponse(open(file_path,'rb'),content_type='application/pdf',as_attachment=True)
# def download_image(request,patient_id):
#     path=request.GET['path']
#     file_path = os.path.join(settings.MEDIA_ROOT,path)
#     if os.path.exists(file_path):
#         return FileResponse(open(file_path,'rb'),content_type='application/pdf',as_attachment=True)
    
    