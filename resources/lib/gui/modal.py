import pyxbmct


def doModal(modal_class, *args, **kwargs):
    modal = modal_class(*args, **kwargs)
    modal.doModal()
    del modal

# Create a class for our UI
class ModalWindow(pyxbmct.AddonDialogWindow):

    def __init__(self, title='My Modal', row_height = 52, col_width = 40):
        """Class constructor"""
        # Call the base class' constructor.
        super(ModalWindow, self).__init__(title)
        self._controls = {}
        self.row_height = row_height
        self.col_width  = col_width
        self.row_count  = 5
        self.col_count  = 12
        self.set_layout()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
    
    def set_layout(self):
        pass

    def set_grid(self, row_count = None, col_count = None):
        if row_count:
            self.row_count = row_count
        if col_count:
            self.col_count = col_count
        self.setGeometry(self.col_count*self.col_width, self.row_count*self.row_height, self.row_count, self.col_count)

    def set_control(self, id: str, type: str, pos_y: int, pos_x: int, height: int, width: int, action = None, items = None, index = None, **kwargs):
        control = self.get_control(id)
        if control:
            if type == 'list':
                if index is None:
                    index = control.getSelectedPosition()
                self.del_control(id)
                control = None
            elif type == 'fade' or type == 'button':
                self.del_control(id)
                control = None
            else:
                self.removeControl(control)
        if not control:
            if type == 'button':
                control = pyxbmct.Button(**kwargs)
            elif type == 'label':
                control = pyxbmct.Label(**kwargs)
            elif type == 'list':
                control = pyxbmct.List(_itemTextXOffset=-5, _itemTextYOffset=0, _itemHeight=self.row_height-16, _space=0, **kwargs)
            elif type == 'edit':
                nkwargs = {i:kwargs[i] for i in kwargs if i!='text'}
                control = pyxbmct.Edit(**nkwargs)
            elif type == 'fade':
                nkwargs = {i:kwargs[i] for i in kwargs if i!='label'}
                control = pyxbmct.FadeLabel(**nkwargs)
            self._controls[id] = control
        self.placeControl(control, pos_y, pos_x, height, width)
        if type == 'fade' and kwargs.get('label'):
            control.addLabel(kwargs.get('label'))
        if type == 'label' and kwargs.get('label'):
            control.setLabel(kwargs.get('label'))
        if type == 'edit' and kwargs.get('text'):
            control.setText(kwargs.get('text'))
        if items is not None and type == 'list' and control.size() <= 0:
            control.addItems(items)
        if index is not None and type == 'list' and control.getSelectedPosition() != index:
            control.selectItem(index)
        if action is not None:
            self.connect(control, action)
        return control
    
    def get_control(self, id):
        return self._controls.get(id)
    
    def del_control(self, id):
        if id in self._controls:
            self.removeControl(self._controls[id])
            del self._controls[id]

    def goto(self, modal_class, *args, **kwargs):
        self.close()
        modal = modal_class(*args, **kwargs)
        modal.doModal()
        del modal
