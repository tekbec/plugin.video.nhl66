from codequick.storage import PersistentDict
from codequick import Script
from codequick.script import Settings
from typing import Optional
from ...common.requests import post
from .entitlement_signature import EntitlementSignature
from .consts import PREMIUM_ACCOUNT_API_BASE_URL, SIGNATURE_PATH
from .device import Device
import json, traceback, xbmcaddon

class Auth:

    _auth_failed = False

    @staticmethod
    def is_premium() -> bool:
        signature = Auth.get_signature()
        if not signature or signature.expired:
            return False
        else:
            return True

    @staticmethod
    def get_signature() -> Optional[EntitlementSignature]:
        premium_code = Settings.get_string('premium_code')
        if not premium_code:
            return None
        premium_code = premium_code.replace('-', '').strip()
        try:
            with PersistentDict('auth') as db:
                signature = None
                if 'signature' in db:
                    signature = EntitlementSignature(db['signature'])
                if signature is None or signature.expired or signature.premium_code != premium_code:
                    signature = Auth._generate_signature()
                    if signature:
                        db['signature'] = str(signature)
                return signature

        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)
            traceback.print_exc()
            return None
       
    
    @staticmethod
    def _generate_signature() -> Optional[EntitlementSignature]:
        if Auth._auth_failed:
            Script.log(f'Authentication already failed, signature generation is bypassed.', lvl=Script.WARNING)
            return None
        premium_code = Settings.get_string('premium_code')
        if not premium_code:
            return None
        premium_code = premium_code.replace('-', '').strip()
        Script.log('Generating signature...')
        response = post(url=PREMIUM_ACCOUNT_API_BASE_URL + SIGNATURE_PATH, provider='nhl66_premium', skip_cache=True, json={
            'code': premium_code,
            'device_uuid': Device.get_device_uuid(),
            'ent_name': 'NHL'
        })
        if response.status_code != 200:
            Script.log(f'Response status code: {str(response.status_code)}', lvl=Script.ERROR)
            Script.log(f'Response body: {response.text}', lvl=Script.ERROR)
            addon_data = xbmcaddon.Addon()
            addon_icon = addon_data.getAddonInfo('icon')
            Script.notify(heading='Invalid Premium Code', message='Remove or review it in the settings.', icon=addon_icon)
            Auth._auth_failed = True
            return None
        try:
            raw_signature = json.loads(response.text)
            signature = EntitlementSignature(raw_signature)
            if signature.expired:
                return None
            Script.log(f'Signature generated: {str(signature)}')
            return signature
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)
            traceback.print_exc()
            return None


