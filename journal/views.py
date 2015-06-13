from django.views.generic.base import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from datetime import date

from journal.models import Article, Container, Author
from journal.fetchDOI import FetchDOI

from overlay import settings


class OverlayManage(TemplateView):
    """Handles requests for authorised users to add and remove journal articles."""

    template_name = "admin.html"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(OverlayManage, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OverlayManage, self).get_context_data(**kwargs)
        context['containers'] = Container.objects.filter(url='')
        context['title'] = settings.journal_title
        return context


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['title'] = settings.journal_title
        context['editor'] = settings.journal_editor
        context['container'] = Container.objects.filter(url='')[0]
        return context


def user_login(request):
    """Processes a user login."""
    # Obtain the context for the user's request.
    context = RequestContext(request)

    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/admin')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    else:
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    """Logs out a currently logged-in user."""
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

@staff_member_required
def new_container(request):
    container = Container()
    container.issue = int(request.POST.get("issue", "0"))
    container.volume = int(request.POST.get("volume", "0"))
    container.date = date.today()
    container.save()

    return HttpResponseRedirect('/manage')

@staff_member_required
def new_article(request, cont=None):
    doi = FetchDOI.fetch_and_parse(request.POST.get("doi", ""))

    article = Article()
    article.local_container = Container.objects.filter(id=cont)[0]
    article.title = doi['title']

    container = Container()
    container.issue = int(doi['issue'])
    container.volume = int(doi['volume'])
    container.date = date.today()
    container.url = (doi['url'])
    container.title = doi['journal']
    container.save()

    article.remote_container = container

    article.save()

    for author in doi['authors']:
        new_author = Author()
        new_author.family = author['family']
        new_author.given = author['given']
        new_author.article = article
        new_author.save()

    return HttpResponseRedirect('/manage')

@staff_member_required
def del_article(request, article=None):
    article = Article.objects.filter(id=article)[0]
    article.delete()

    return HttpResponseRedirect('/manage')