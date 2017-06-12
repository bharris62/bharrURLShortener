from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .forms import SubmitUrlForm
from .models import BharrURL

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SubmitUrlForm()
        context = {
            "title": "Bharr.co",
            "form": form
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Bharr.co",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():

            submitted_url = form.cleaned_data.get('url')
            obj, created = BharrURL.objects.get_or_create(url=submitted_url)
            context = {
                "object": obj,
                'created': created
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)



class BharrRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(BharrURL, shortcode=shortcode, )
        return HttpResponseRedirect(obj.url)
