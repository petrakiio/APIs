from django.contrib.auth.models import AnonymousUser

from models.auth_model import User


class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            request.user = User.objects.filter(id=user_id).first() or AnonymousUser()
        else:
            request.user = AnonymousUser()

        return self.get_response(request)
