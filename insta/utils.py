from django.http import HttpResponse
from .models import User
from django.shortcuts import get_object_or_404
import json
import random


def check(request):
    user_pk = request.session.get('user')
    if user_pk:
        user = get_object_or_404(User, id=user_pk)
        if user.is_verified is True:
            context = {'login': 'true', 'verified': 'true'}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            context = {'login': 'true', 'verified': 'false'}
            return HttpResponse(json.dumps(context), content_type="application/json")

    context = {'login': 'false'}
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_random_unicode(length):
    get_char = chr

    include_ranges = [
        (0x0021, 0x0021),
        (0x0023, 0x0026),
        (0x0028, 0x007E),
        (0x00A1, 0x00AC),
        (0x00AE, 0x00FF),
        (0x0100, 0x017F),
        (0x0180, 0x024F),
        (0x2C60, 0x2C7F),
        (0x16A0, 0x16F0),
        (0x0370, 0x0377),
        (0x037A, 0x037E),
        (0x0384, 0x038A),
        (0x038C, 0x038C),
    ]
    char = [
        get_char(code_point) for current_range in include_ranges
        for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return ''.join(random.choice(char) for i in range(length))
