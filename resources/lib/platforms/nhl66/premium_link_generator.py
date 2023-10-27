from .link import Link
from .auth import Auth
from .consts import PREMIUM_NHL_API_BASE_URL, STREAM_INFO_PATH
from ...common.requests import post
import json

class PremiumLinkGenerator:

    @staticmethod
    def generate_premium_link(link: Link) -> str:
        signature = Auth.get_signature()
        if not signature or signature.expired:
            return None
        if not link.premium_flavor:
            return None
        response = post(url=PREMIUM_NHL_API_BASE_URL + STREAM_INFO_PATH, provider='nhl66_premium', skip_cache=True, json={
            'flavor': link.premium_flavor,
            'source_id': link.id,
            'token': str(signature)
        })
        if response.status_code != 200:
            return None
        try:
            stream_info = json.loads(response.text)
            return stream_info['url']
        except:
            return None