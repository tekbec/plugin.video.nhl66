import pyxbmct
from ...platforms.nhl66 import Auth

# Create a class for our UI
class ExpiredWindow(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Expired Account'):
        """Class constructor"""
        # Call the base class' constructor.
        super(ExpiredWindow, self).__init__(title)
        # Set width, height and the grid parameters
        self.setGeometry(12*32, 52*4, 4, 12)
        # Call set controls method
        self.set_controls()
        # Call set navigation method.
        self.set_navigation()
        # Connect Backspace button to close our addon.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)


    def set_controls(self):
        # Message
        label = pyxbmct.Label('Your account is expired.', alignment=2)
        self.placeControl(label, 1, 0, 1, 12)

        # Close button
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 3, 0, 1, 6)
        self.connect(self.close_button, self.close)

        # Logout button
        self.logout_button = pyxbmct.Button('Logout')
        self.placeControl(self.logout_button, 3, 6, 1, 6)
        self.connect(self.logout_button, self.logout)

    def set_navigation(self):
        self.setFocus(self.logout_button)
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