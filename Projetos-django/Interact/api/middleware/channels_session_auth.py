from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from models.auth_model import User


@database_sync_to_async
def _get_user(session_key):
    if not session_key:
        return AnonymousUser()
    try:
        session = Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return AnonymousUser()

    session_data = session.get_decoded()
    user_id = session_data.get('user_id')
    if not user_id:
        return AnonymousUser()

    return User.objects.filter(id=user_id).first() or AnonymousUser()


class SessionAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        session = scope.get('session')
        session_key = getattr(session, 'session_key', None)
        scope['user'] = await _get_user(session_key)
        return await super().__call__(scope, receive, send)


def SessionAuthMiddlewareStack(inner):
    from channels.sessions import SessionMiddlewareStack

    return SessionAuthMiddleware(SessionMiddlewareStack(inner))
