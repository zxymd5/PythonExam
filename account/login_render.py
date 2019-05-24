from account.models import Profile
from django.shortcuts import render


def web_index(request):
    uid = request.session.get('uid', '')
    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'web/index.html', {
        'user_info': profile and profile.data,
        'upgrade_info': profile and profile.upgrade_data,
        'has_login': bool(profile),
    })
