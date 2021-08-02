from django.http import HttpResponse
import json


def check(request):
    user_pk = request.session.get('user')
    if not user_pk:
        context = {'s': 'false'}
        return HttpResponse(json.dumps(context), content_type="application/json")
    context = {'s': 'true'}
    return HttpResponse(json.dumps(context), content_type="application/json")
