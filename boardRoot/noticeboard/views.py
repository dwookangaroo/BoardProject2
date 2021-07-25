from django.shortcuts import render, get_object_or_404
from noticeboard.models import Notice

# redirect 할때 필요한 import
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
# Create your views here.


def index(request):
    article_list = Notice.objects.all().order_by('-writeDate')
    context = {'article_list': article_list}
    return render(request, 'noticeboard/index.html', context)


def write_article(request):
    return render(request, 'noticeboard/writeArticle.html')

def add_article(request):
    notice = Notice()
    notice.title = request.POST['title']
    notice.content = request.POST['content']
    notice.writeID = 'bit'
    notice.save()
    # redirect 할떄 reverse함수(template를 파이썬에서 쓸수잇는 함수)
    return HttpResponseRedirect(reverse('noticeboard:index'))

def view_article(request, article_id):
    notice = get_object_or_404(Notice, pk=article_id)
    #article 키 값에 notice를 넘겨준다
    return render(request, 'noticeboard/detail.html', {'article':notice})

def update_article(request, article_id):
    notice = Notice.objects.get(id=article_id)

    if request.method == 'POST':
        notice.title = request.POST['title'] # title, content만 바꿔주면된다
        notice.content = request.POST['content']
        notice.writeDate = timezone.datetime.now() #수정할때 지금의 시간
        notice.save() # save
        # reverse함수에 parameter 넣어주기 args={}
        return HttpResponseRedirect(reverse('noticeboard:view', args={article_id}))
    else: #포스트 접근법이 아닐때
        return render(request, 'noticeboard/detail.html', {'article':notice})

def delete_article(request, article_id):
    notice = Notice.objects.get(id=article_id)
    notice.delete()
    return HttpResponseRedirect(reverse('noticeboard:index'))