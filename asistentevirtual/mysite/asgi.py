import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

django.setup()

django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    # Tráfico normal
    "http": get_asgi_application(),
    
    # Tráfico de WebSockets
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})