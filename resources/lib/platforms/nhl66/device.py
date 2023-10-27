import uuid
from codequick.storage import PersistentDict


class Device:
    
    @staticmethod
    def get_device_uuid() -> str:
        with PersistentDict('auth') as db:
            if 'device_uuid' in db:
                return db['device_uuid']
            else:
                device_uuid = str(uuid.uuid4())
                db['device_uuid'] = device_uuid
                return device_uuid