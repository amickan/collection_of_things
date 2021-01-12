from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect
from collection.forms import ThingForm, ContactForm
from collection.models import Thing
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError


# Create your views here.
def index(request):
    # number = 6*
    # thing = "Thing name"
    things = Thing.objects.all()
    # things = Thing.objects.filter(name__contains='shiny')
    # passing the variable to the view
    return render(request, 'index.html', {
        'things': things,
    })


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"

def thing_detail(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)
    # and pass to the template
    return render(request, 'things/thing_detail.html', {
        'thing': thing,
    })


@login_required
def edit_thing(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)
    # make sure the logged in user is the owner of the thing
    if thing.user != request.user:
        raise Http404
    # set the form we're using...
    form_class = ThingForm
    # if we're coming to this view from a submitted form,
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('thing_detail', slug=thing.slug)
            # otherwise just create the form
    else:
        form = form_class(instance=thing)
    # and render the template
    return render(request, 'things/edit_thing.html', {
        'thing': thing,
        'form': form,
    })


def create_thing(request):
    form_class = ThingForm
    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to
        # the form
        form = form_class(request.POST)
        if form.is_valid():
            # create an instance but do not save yet
            thing = form.save(commit=False)
            # set the additional details
            thing.user = request.user
            thing.slug = slugify(thing.name)
            # save the object
            thing.save()
            # redirect to our newly created thing
            return redirect('thing_detail', slug=thing.slug)
            # otherwise just create the form
    else:
        form = form_class()
    return render(request, 'things/create_thing.html', {
        'form': form,
    })


def browse_by_name(request, initial=None):
    if initial:
        things = Thing.objects.filter(name__istartswith=initial).order_by('name')
    else:
        things = Thing.objects.all().order_by('name')
    return render(request, 'search/search.html', {
        'things': things,
        'initial': initial,
    })


def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['amickan1990@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})



def successView(request):
    # return HttpResponse('Success! Thank you for your message.')
    return redirect('home')