from django.http import HttpResponse
import json

<<<<<<< HEAD
=======

>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a
def check(request):
    user_pk = request.session.get('user')
    if not user_pk:
        context = {'s': 'false'}
        return HttpResponse(json.dumps(context), content_type="application/json")
    context = {'s': 'true'}
<<<<<<< HEAD
    return HttpResponse(json.dumps(context), content_type="application/json")
=======
    return HttpResponse(json.dumps(context), content_type="application/json")
>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a
