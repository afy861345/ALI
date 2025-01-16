from django.shortcuts import render,redirect,get_object_or_404
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import Topic_form
# Create your views here.
def main(request):
    boards=Board.objects.all()
    return render(request,'home/main.html',{'boards':boards})
def board(request,board_id):
    board=get_object_or_404(Board,id=board_id)
    return render(request,"home/board.html",{'board':board})
def topic(request,board_id,topic_id):
    board=get_object_or_404(Board,id=board_id)
    topic=get_object_or_404(Topic,id=topic_id,board=board)
    return render(request,"home/topic.html",{'board':board,'topic':topic})
def new_topic(request,board_id):
    board=get_object_or_404(Board,id=board_id)
    if request.method=="POST":
        form=Topic_form(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            user=User.objects.first()
            topic.board=board
            topic.created_by=user
            topic.save()
            message=form.cleaned_data.get("message")
            post=Post.objects.create(message=message,topic=topic,created_by=user)
            return redirect("board",board.id)
    else:
        form=Topic_form()
    return render(request,"home/new_topic.html",{'board':board,'form':form})