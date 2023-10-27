from datetime import datetime, timedelta


class EntitlementSignature:

    _consider_expired_when_time_left = timedelta(seconds=10*60)

    def __init__(self, signature: str):
        if not signature:
            self._signature = ''
        else:
            self._signature = signature

    def __str__(self):
        return self._signature
    
    @property
    def premium_code(self) -> str:
        if not self._signature:
            return ''
        try:
            components = self._signature.split('.')
            if len(components) != 4:
                return ''
            return components[0]
        except:
            return ''
        
    @property
    def entitlement_name(self) -> str:
        if not self._signature:
            return ''
        try:
            components = self._signature.split('.')
            if len(components) != 4:
                return ''
            return components[1]
        except:
            return ''
        
    @property
    def token(self) -> str:
        if not self._signature:
            return ''
        try:
            components = self._signature.split('.')
            if len(components) != 4:
                return ''
            return components[2]
        except:
            return ''
        
    @property
    def expiry(self) -> datetime:
        if not self._signature:
            return None
        try:
            components = self._signature.split('.')
            if len(components) != 4:
                return None
            return datetime.fromtimestamp(int(components[3]))
        except:
            return None
        
    @property
    def expires_in(self) -> timedelta:
        if self.expiry is None:
            return None
        return self.expiry - datetime.now()
    
    @property
    def expired(self) -> bool:
        if self.expires_in is None:
            return True
        if self.expires_in < self._consider_expired_when_time_left:
            return True
        return False



