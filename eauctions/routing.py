from django.urls import path

from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from auction.consumers import auction_WebSocketConsumer

# Consumer Imports
from userman.consumers import usermanConsumer


application = ProtocolTypeRouter({

    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/", auction_WebSocketConsumer),
        ])
    ),
    "channel": ChannelNameRouter({
        "userman": usermanConsumer,
    })
})
