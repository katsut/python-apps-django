from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/work13/live-feed/$', consumers.LiveFeedConsumer.as_asgi()),
    re_path(r'ws/work13/post/(?P<post_id>\w+)/$', consumers.PostConsumer.as_asgi()),
]
