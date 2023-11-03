import pyxbmct
import qrcode
import os.path
from ...platforms.nhl66 import Auth
from codequick import Script

# Create a class for our UI
class LoginWindow(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        """Class constructor"""
        # Call the base class' constructor.
        super(LoginWindow, self).__init__(title)
        # Set width, height and the grid parameters
        self.setGeometry(92*4, 52*7, 7, 4)
        # Call set controls method
        self.set_controls()
        # Call set navigation method.
        self.set_navigation()
        # Connect Backspace button to close our addon.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        # QR Code
        qrcode_path = os.path.join(Script.get_info("profile"), 'qrcode.png')
        img = qrcode.make('https://account24network.com/')
        img.save(qrcode_path)
        image = pyxbmct.Image(qrcode_path)
        self.placeControl(image, 0, 1, rowspan=4, columnspan=2)

        # QR Code Subtitle
        label = pyxbmct.Label('Scan to retrieve your code', alignment=2)
        self.placeControl(label, 4, 0, 1, 4)

        # Premium Code
        self.code_field = pyxbmct.Edit('Premium Code:')
        self.placeControl(self.code_field, 5, 0, 1, 4)

        # Close button
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 6, 0, 1, 2)
        self.connect(self.close_button, self.close)

        # Login button
        self.login_button = pyxbmct.Button('Login')
        self.placeControl(self.login_button, 6, 2, 1, 2)
        self.connect(self.login_button, self.login)

    def set_navigation(self):
        self.setFocus(self.code_field)
        self.code_field.controlDown(self.login_button)
        self.close_button.controlUp(self.code_field)
        self.close_button.controlRight(self.login_button)
        self.login_button.controlUp(self.code_field)
        self.login_button.controlLeft(self.close_button)
        self.setFocus(self.code_field)

    def login(self):
        from .account import AccountWindow
        self.login_button.setEnabled(False)
        premium_code = self.code_field.getText().strip()
        if not premium_code:
            Script.notify('Login failed', 'Premium code is empty.')
        elif not Auth.login(premium_code):
            Script.notify('Login failed', 'Premium code is invalid or expired.')
            self.code_field.setText('')
        else:
            Script.notify('Success', 'Premium code successfully registered.')
            self.close()
            account_window = AccountWindow()
            account_window.doModal()
            del account_window
            return
        self.login_button.setEnabled(True)