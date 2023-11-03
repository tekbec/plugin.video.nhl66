from codequick.storage import PersistentDict
import pyxbmct, xbmcgui
from codequick.script import Script
from .consts import proxies_providers
from ..modal import ModalWindow

# Create a class for our UI
class SetProxyWindow(ModalWindow):

    def __init__(self, title='Proxy', platform=None):
        self.platform = platform
        self.providers = {
            'custom': {
                'id': 'custom',
                'name': 'Custom'
            }
        }
        self.providers.update(proxies_providers)
        self.provider = self.providers['custom']
        self.location = None
        self.username = ''
        self.password = ''
        
        # Try to load from db
        with PersistentDict('proxies.pickle') as db:
            # Search an entry
            entry = db.get(self.platform)
            if entry:
                # Check if provider specified and valid
                provider = entry.get('provider')
                if provider and provider in self.providers:
                    self.provider = self.providers[provider]
                    # If not custom provider
                    if provider != 'custom':
                        # Try to apply location
                        location = entry.get('location')
                        locations = self.get_locations()
                        if location and location in locations:
                            self.location = locations[location]
                        # Try to apply username and password
                        self.username = entry.get('username', '')
                        self.password = entry.get('password', '')

        super(SetProxyWindow, self).__init__(title)

        # Set base window
        self.set_layout()
        # Connect Backspace button to close our addon.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)


    
    def set_layout(self):
        # Window size
        if self.provider['id'] == 'custom':
            self.set_grid(6, 12)
        else:
            self.set_grid(12, 12)

        # Provider Selection
        self.set_control('provider_label', 'label', 0, 0, 1, 12, label='------------------------ Provider ------------------------', alignment=6, font='font14')
        self.set_control('provider_list',  'list',  1, 1, 3, 4, action=self.on_provider_change, items=[x['name'] for x in self.providers.values()], _alignmentY=6)
        self.set_control('selected_provider_label', 'label', 1, 5, 2, 7, label=f'Selected: {self.provider["name"]}', alignment=6)

        # Custom
        if self.provider['id'] == 'custom':
            # Remove unused controls
            if self.get_control('location_label'): self.del_control('location_label')
            if self.get_control('location_list'):  self.del_control('location_list')
            if self.get_control('selected_location_label'): self.del_control('selected_location_label')
            if self.get_control('credentials_label'): self.del_control('credentials_label')
            if self.get_control('username_edit'): self.del_control('username_edit')
            if self.get_control('password_edit'): self.del_control('password_edit')
            # Create specific controls
            self.set_control('proxy_label', 'label', 3, 0, 1, 12, label='------------------------ Custom Entry ------------------------', alignment=6, font='font14')
            self.set_control('proxy_edit', 'edit', 4, 0, 1, 12, label='Proxy:')

        # Provider
        else:
            # Remove unused controls
            if self.get_control('proxy_label'): self.del_control('proxy_label')
            if self.get_control('proxy_edit'): self.del_control('proxy_edit')
            # Create specific controls
            self.set_control('location_label', 'label', 3, 0, 1, 12, label='------------------------ Location ------------------------', alignment=6, font='font14')
            self.set_control('location_list',  'list',  4, 1, 4, 10, action=self.on_location_change, items=[self.format_location_name(x) for x in self.get_locations().values()])
            self.set_control('selected_location_label', 'label', 7, 0, 1, 12, label=f'Selected: {self.format_location_name(self.location)}', alignment=6)
            self.set_control('credentials_label', 'label', 8, 0, 1, 12, label='------------------------ Credentials ------------------------', alignment=6, font='font14')
            self.set_control('username_edit', 'edit', 9, 0, 1, 12, label='Username:', text=self.username)
            self.set_control('password_edit', 'edit', 10, 0, 1, 12, label='Password:', text=self.password)

        # Footer
        if self.provider['id'] == 'custom':
            self.set_control('close', 'button', 5, 0, 1, 6, action=self.close, label='Close')
            self.set_control('save',  'button', 5, 6, 1, 6, action=self.on_save, label='Save' )
        else:
            self.set_control('close', 'button', 11, 0, 1, 6, action=self.close, label='Close')
            self.set_control('save',  'button', 11, 6, 1, 6, action=self.on_save, label='Save' )
        
        self.setFocus(self.get_control('provider_list'))
        self.set_navigation()


    
    def get_locations(self):
        if self.provider['id'] == 'custom':
            return []
        return self.provider['locations']
    

    
    def format_location_name(self, location):
        if not location:
            return 'N/A'
        name = f'{location["country"]} - {location["city"]}'
        if 'suffix' in location:
            name += f' - {location["suffix"]}'
        return name



    def on_provider_change(self):
        # Get the provider list control
        control = self.get_control('provider_list')

        # If control not found, set a default provider
        if not control: 
            self.provider = self.providers['custom']
            self.location = None
            return self.set_layout()
        
        # Get the selected index
        index = control.getSelectedPosition()
        providers_list = list(self.providers.values())

        # If the index is out of range, set a default provider
        if index >= len(providers_list):
            self.provider = self.providers['custom']
            self.location = None
            return self.set_layout()
        
        # Set the provider
        self.provider = providers_list[index]

        # Set default location
        locations = self.get_locations()
        if len(locations) == 0:
            self.location = None
        else:
            self.location = list(locations.values())[0]
        return self.set_layout()



    def on_location_change(self):
        # Get the current provider locations
        locations = self.get_locations()

        # If no location found, undefine the location
        if len(locations) == 0:
            self.location = None
        else:

            # Get the location list control
            control = self.get_control('location_list')

            # If no control found, undefine the location
            if not control: 
                self.location = None
            else:

                # Get the selected index
                index = control.getSelectedPosition()
                locations_list = list(locations.values())

                # If the index is out of range, set a default location
                if index >= len(locations_list):
                    self.location = locations_list[0]
                else:

                    # Set the location
                    self.location = locations_list[index]

        # Always update the selected location label
        return self.set_control('selected_location_label', 'label', 7, 0, 1, 12, label=f'Selected: {self.format_location_name(self.location)}', alignment=6)



    def on_save(self):
        entry = None
        if self.provider['id'] == 'custom':
            url = self.get_control('proxy_edit').getText()
            if url:
                entry = {
                    'provider': 'custom',
                    'url': url
                }
        else:
            username = self.get_control('username_edit').getText()
            password = self.get_control('password_edit').getText()
            if not username:
                return Script.notify('Bad credentials', 'Username cannot be empty.')
            if not password:
                return Script.notify('Bad credentials', 'Password cannot be empty.')
            url = f'https://{username}:{password}@{self.location["hostname"]}:{self.location["port"]}'
            entry = {
                'provider': self.provider['id'],
                'location': self.location['id'],
                'username': username,
                'password': password,
                'url': url
            }
        with PersistentDict('proxies.pickle') as db:
            db[self.platform] = entry
        from .proxies import ProxiesWindow
        self.goto(ProxiesWindow)



    def set_navigation(self):
        provider: xbmcgui.Control = self.get_control('provider_list')
        location: xbmcgui.Control = self.get_control('location_list')
        username: xbmcgui.Control = self.get_control('username_edit')
        password: xbmcgui.Control = self.get_control('password_edit')
        proxy:    xbmcgui.Control = self.get_control('proxy_edit')
        close:    xbmcgui.Control = self.get_control('close')
        save:     xbmcgui.Control = self.get_control('save')
        provider.setNavigation(
            provider,
            proxy if proxy else location,
            provider,
            proxy if proxy else location,
        )
        if location:
            location.setNavigation(
                provider,
                username,
                provider,
                username,
            )
        if username:
            username.setNavigation(
                location,
                password,
                location,
                password,
            )
        if password:
            password.setNavigation(
                username,
                save,
                username,
                save,
            )
        if proxy:
            proxy.setNavigation(
                provider,
                save,
                provider,
                save,
            )
        close.setNavigation(
            proxy if proxy else password,
            close,
            close,
            save
        )
        save.setNavigation(
            proxy if proxy else password,
            save,
            close,
            save
        )
