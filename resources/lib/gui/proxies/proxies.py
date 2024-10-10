from codequick.storage import PersistentDict
from codequick import Script
import pyxbmct, xbmcgui
from ..modal import ModalWindow
from ...common.labels import labels

# Create a class for our UI
class ProxiesWindow(ModalWindow):

    def __init__(self, title='Proxies'):
        title = Script.localize(labels.get('proxies'))
        self.platforms = [
            {
                'id': 'nhltv',
                'name': 'NHL.TV'
            },
            {
                'id': 'espn',
                'name': 'ESPN'
            },
            {
                'id': 'nhl66',
                'name': 'NHL66'
            }
        ]
        super(ProxiesWindow, self).__init__(title, col_width=60)
        

        # Set base window
        self.set_layout()
        # Call set navigation method.
        self.set_navigation()
        # Connect Backspace button to close our addon.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    
    def set_layout(self):
        # Window size
        self.set_grid(len(self.platforms)*3+1, 12)

        # Platforms
        i = 0
        for platform in self.platforms:
            self.set_control(f'{platform["name"]}_label', 'label', i, 0, 1, 12, label=f'------------------------ {platform["name"]} ------------------------', alignment=6, font='font14')
            self.set_control(f'{platform["name"]}_fade',   'fade'  , i+1, 0, 1, 12, label=self.get_proxy_label(platform['id']), _alignment=6)
            self.set_control(f'{platform["name"]}_edit_button', 'button', i+2, 3, 1, 3, action=self.edit(platform), label=Script.localize(labels.get('edit')))
            self.set_control(f'{platform["name"]}_clear_button', 'button', i+2, 6, 1, 3, action=self.clear(platform), label=Script.localize(labels.get('clear')))
            if i == 0:
                self.setFocus(self.get_control(f'{platform["name"]}_edit_button'))
            i += 3

        # Footer
        self.set_control('close_button', 'button', self.row_count-1, 9, 1, 3, action=self.close, label=Script.localize(labels.get('close')))

        # Set Navigation Controls
        self.set_navigation()



    def clear(self, platform):
        def f():
            with PersistentDict('proxies.pickle') as db:
                db[platform['id']] = None
            self.set_layout()
        return f



    def edit(self, platform):
        def f():
            from .set_proxy import SetProxyWindow
            self.goto(SetProxyWindow, platform=platform['id'])
        return f

    

    def get_proxy_label(self, platform_id):
        with PersistentDict('proxies.pickle') as db:
            entry = db.get(platform_id)
            url = None
            if entry:
                url = entry.get('url')
            if not url: return Script.localize(labels.get('no_proxy'))
            return url
            


    def set_navigation(self):
        for i in range(len(self.platforms)):
            edit_button: xbmcgui.Control = self.get_control(f'{self.platforms[i]["name"]}_edit_button')
            clear_button: xbmcgui.Control = self.get_control(f'{self.platforms[i]["name"]}_clear_button')
            edit_button.setNavigation(
                edit_button if i == 0 else self.get_control(f'{self.platforms[i-1]["name"]}_edit_button'),
                self.get_control('close_button') if i == len(self.platforms)-1 else self.get_control(f'{self.platforms[i+1]["name"]}_edit_button'),
                edit_button,
                clear_button
            )
            clear_button.setNavigation(
                clear_button if i == 0 else self.get_control(f'{self.platforms[i-1]["name"]}_clear_button'),
                self.get_control('close_button') if i == len(self.platforms)-1 else self.get_control(f'{self.platforms[i+1]["name"]}_clear_button'),
                edit_button,
                self.get_control('close_button') if i == len(self.platforms)-1 else clear_button
            )
        self.get_control('close_button').setNavigation(
            self.get_control(f'{self.platforms[-1]["name"]}_clear_button'),
            self.get_control('close_button'),
            self.get_control(f'{self.platforms[-1]["name"]}_clear_button'),
            self.get_control('close_button')
        )
