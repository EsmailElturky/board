from email import message
from ntpath import join
from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404, HttpResponse
from .models import Board
from django.contrib.auth.models import User
from .models import Topic
from .models import Post
from .forms import NewTopicForm,Postform
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

#any function in views must have request arguement
def home(request):
    boards=Board.objects.all()
    return render(request,'home.html',{'the_boards':boards})
    #render automatics go to templet folder and search for the html

class BoardListView(ListView):
    model = Board
    context_object_name='boards'
    template_name = 'home.html'

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


def board_topics(request,board_id):
    # try:
    #     board=Board.objects.get(pk=board_id)
    # except Board.DoesNotExist:
    #     raise Http404
    board=get_object_or_404(Board,pk=board_id)
    topics=board.topics.annotate(comments=Count('posts'))
    return render(request,'topics.html',{'the_board':board,'topics':topics})

@login_required
def new_topic(request,board_id):
    board=get_object_or_404(Board,pk=board_id)
    

    if request.method=='POST':
        form=NewTopicForm(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            topic.board=board
            topic.created_by=request.user
            topic.save()

            post=Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=request.user,
                topic=topic
            )
            return redirect('board_topics',board_id=board.pk)

    else:
        form=NewTopicForm()

    
    return render(request,'new_topic.html',{'the_board':board ,'form':form})


def topic_posts(request,board_id,topic_id):
    topic=get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    topic.views +=1
    topic.save()
    return render(request,'topic_posts.html',{'topic':topic})

@login_required
def reply_topic(request,board_id,topic_id):
    topic=get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    if request.method=='POST':
        form=Postform(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.topic=topic
            post.created_by=request.user
            post.save()


            return redirect('topic_posts',board_id=board_id,topic_id=topic_id)

    else:
        form=Postform()


    return render(request,'reply_topic.html',{'topic':topic,'form':form})


@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts',board_id=post.topic.board.pk,topic_id=post.topic.pk)








# Create your views here.