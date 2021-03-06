from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect
from collection.forms import ThingForm, ContactForm, ThingUploadForm, EditEmailForm
from collection.models import Social, Thing, Upload
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, View
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import mail_admins
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collection.serializers import ThingSerializer


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"

class DetailView(DetailView):
    model = Thing
    template_name = 'things/thing_detail.html'
    context_object_name = 'thing'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # social accounts related to the current thing
        ctx['social_accounts'] = self.object.social_accounts.all()
        ctx['uploads'] = self.object.uploads.all()
        return ctx

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
        mail_admins("User edited a thing", "User updated their thing!")
        form = form_class(data=request.POST, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            messages.success(request, 'Thing details updated.')
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


class BrowseName(View):
    def get(self, request, initial=None):
        if initial:
            things = Thing.objects.filter(name__istartswith=initial).order_by('name')
        else:
            things = Thing.objects.all().order_by('name')
        return render(request, 'search/search.html', context={
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
           # first_name = form.cleaned_data['first_name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['to@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})



def successView(request):
    # return HttpResponse('Success! Thank you for your message.')
    return redirect('home')

@login_required
def edit_thing_uploads(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)
    # double checking just for security
    if thing.user != request.user:
        raise Http404
        # set the form we're using...
    form_class = ThingUploadForm
    # if we're coming to this view from a submitted form,
    if request.method == 'POST':
        # grab the data from the submitted form,
        # note the new "files" part
        form = form_class(data=request.POST,
            files=request.FILES, instance=thing)

        if form.is_valid():
            # create a new object from the submitted form
            Upload.objects.create(
                image=form.cleaned_data['image'],
                thing=thing,
            )
            return redirect('edit_thing_uploads', slug=thing.slug)
    # otherwise just create the form
    else:
        form = form_class(instance=thing)

    # grab all the object's images
    uploads = thing.uploads.all()
    # and render the template
    return render(request, 'things/edit_thing_uploads.html', {
        'thing': thing,
        'form': form,
        'uploads': uploads,
    })

@login_required
def delete_upload(request, id):
    # grab the image
    upload = Upload.objects.get(id=id)
    # security check
    if upload.thing.user != request.user:
        raise Http404
    # delete the image
    upload.delete()
    # refresh the edit page
    return redirect('edit_thing_uploads', slug=upload.thing.slug)

@login_required
def edit_email(request):
    user = request.user
    form_class = EditEmailForm
    if request.method == 'POST':
        form = form_class(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email address updated.')
            return redirect('home')
    else:
        form = form_class(instance=user)
    return render(request, 'things/edit_email.html', {
         'form': form,
 })


@api_view(['GET'])
def api_thing_list(request):
     """
     List all things
     """
     if request.method == 'GET':
         things = Thing.objects.all()
         serializer = ThingSerializer(things, many=True)
         return Response(serializer.data)


@api_view(['GET'])
def api_thing_detail(request, id):
    """
     Get a specific thing
    """
    try:
        thing = Thing.objects.get(id=id)
    except Thing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ThingSerializer(thing)
        return Response(serializer.data)