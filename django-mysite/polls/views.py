
# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import urllib

from .models import *

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def crawlFirefox(request, urle):
    try:
        urle=urle.replace("diffbot","%")
        urle=urle.replace("%C2%AC",".")
        urle=urllib.parse.unquote(urle)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
        print("Firefox Headless Browser Invoked")
        driver.get(urle)
        time.sleep(15)
        qr=driver.page_source
        driver.quit()
        if not qr:
            raise Http404("crawler did not run!!")
    
    except:
        raise Http404("something is broken!!")
    
    finally:
        return HttpResponse(qr)

def vote(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
       selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
       #Redisplay the question voting form.
       return render(request, 'polls/detail.html', {
           'question':question,
           'error_message': "You didn't select a choice.",
            })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

"""
Removed code!
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/results.html',{'question':question})
"""
