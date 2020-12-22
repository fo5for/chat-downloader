"""Lists the sites that are supported"""

from .youtube import YouTubeChatDownloader
from .twitch import TwitchChatDownloader
from .facebook import FacebookChatDownloader

from .common import ChatDownloader

def GET_ALL_SITES():
    return [
        value
        for value in globals().values()
        if isinstance(value, type) and issubclass(value,ChatDownloader)
        and value != ChatDownloader # not the base class
    ]
