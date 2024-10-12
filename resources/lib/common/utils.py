import xbmc
from codequick import Script

def get_kodi_version() -> float:
    try:
        version = xbmc.getInfoLabel('System.BuildVersion')
        if ' ' in version:
            version = version[:version.index(' ')]
        version = float(version)
        return version
    except Exception as e:
        Script.log(str(e), lvl=Script.ERROR)
        Script.error('Unable to parse Kodi version. Defaultint to "19.0"')
        return 19.0