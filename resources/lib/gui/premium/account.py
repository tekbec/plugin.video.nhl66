import pyxbmct
from ...platforms.nhl66 import Auth

# Create a class for our UI
class AccountWindow(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Premium Account'):
        """Class constructor"""
        # Call the base class' constructor.
        super(AccountWindow, self).__init__(title)
        # Get account info
        self.signature = Auth.get_signature()
        self.info = Auth.get_info()
        # Set width, height and the grid parameters
        self.setGeometry(12*32, 52*6, 6, 12)
        # Call set controls method
        self.set_controls()
        # Call set navigation method.
        self.set_navigation()
        # Connect Backspace button to close our addon.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)


    def set_controls(self):
        # Code
        label = pyxbmct.Label('Code:', alignment=1)
        self.placeControl(label, 0, 0, 1, 4)
        code = 'N/A'
        if self.signature:
            code = self.signature.formatted_premium_code
        label = pyxbmct.Label(code)
        self.placeControl(label, 0, 4, 1, 8)

        # Email
        label = pyxbmct.Label('Email:', alignment=1)
        self.placeControl(label, 1, 0, 1, 4)
        label = pyxbmct.Label(self.info.get('email', 'N/A'))
        self.placeControl(label, 1, 4, 1, 8)

        # Premium
        label = pyxbmct.Label('Premium:', alignment=1)
        self.placeControl(label, 2, 0, 1, 4)
        label = pyxbmct.Label('Yes' if self.signature else 'No')
        self.placeControl(label, 2, 4, 1, 8)

        # Expiry Date
        label = pyxbmct.Label('Expiry Date:', alignment=1)
        self.placeControl(label, 3, 0, 1, 4)
        expiry_date = 'N/A'
        if 'expires_at' in self.info:
            expiry_date = self.info['expires_at'].strftime("%m/%d/%Y %H:%M")
        label = pyxbmct.Label(expiry_date)
        self.placeControl(label, 3, 4, 1, 8)

        # Expires In
        label = pyxbmct.Label('Expires In:', alignment=1)
        self.placeControl(label, 4, 0, 1, 4)
        expires_in = 'N/A'
        if 'expires_in' in self.info:
            d = self.info['expires_in'].days
            h, r = divmod(self.info['expires_in'].seconds, 3600)
            m, s = divmod(r, 60)
            if d > 0:
                expires_in = f'{d} days, {h} hours'
            else: 
                expires_in = f'{h} hours, {m} minutes'
        label = pyxbmct.Label(expires_in)
        self.placeControl(label, 4, 4, 1, 8)
        
        # Close button
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 5, 0, 1, 6)
        self.connect(self.close_button, self.close)

        # Logout button
        self.logout_button = pyxbmct.Button('Logout')
        self.placeControl(self.logout_button, 5, 6, 1, 6)
        self.connect(self.logout_button, self.logout)

    def set_navigation(self):
        self.setFocus(self.close_button)
        self.close_button.setNavigation(
            self.close_button,
            self.close_button,
            self.close_button,
            self.logout_button
        )
        self.logout_button.setNavigation(
            self.logout_button,
            self.logout_button,
            self.close_button,
            self.logout_button
        )

    def logout(self):
        from .login import LoginWindow
        Auth.logout()
        self.close()
        login_window = LoginWindow()
        login_window.doModal()
        del login_window