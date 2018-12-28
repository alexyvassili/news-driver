from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from driver.mailoperator import get_new_mails

def index(request):
    new_mails = get_new_mails()
    template = loader.get_template('driver/index.html')
    context = {
        'new_mails': new_mails,
    }
    return HttpResponse(template.render(context, request))
