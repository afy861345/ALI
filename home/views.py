from django.shortcuts import render,redirect,get_object_or_404
from .models import Board,Topic,Post,Patients as Patient_Model,News
from time import strftime
from django.contrib.auth.models import User
from .forms import Topic_form,Post_form,Patient_form,News_form
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,UpdateView,ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
#fbv
def main(request):
    boards=Board.objects.all()
    return render(request,'home/main.html',{'boards':boards})
def board(request,board_id):
    board=get_object_or_404(Board,id=board_id)
    query_set=board.topics.order_by('-created_at').annotate(comments=Count('posts'))
    paginator=Paginator(query_set,1)
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
# class New_visit(View):
#     def render(self,request,form):
#         return render(request,"home/new_visit.html",{'form':form})
#     def post(self, request,**kwargs):
#         id=self.kwargs['patient_id']
#         patient=get_object_or_404(Patient_Model,pk=id)
#         if request.method=="POST":
#             form=Visit_form(request.POST)
#             if form.is_valid():
#                 visits=Visit.objects.all()
#                 for visit in visits:
#                     if visit:
#                         print(1)
#                         return redirect('main')
#                 else:
#                     print(0)
#         return self.render(request,form)
#     def get(self,request,**kwargs):
#         form=Visit_form()
#         return self.render(request,form)
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

    
