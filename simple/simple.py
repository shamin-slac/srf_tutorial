import json
from functools import partial
from typing import Dict

from PyQt5.QtCore import Qt, pyqtSlot
from pydm import Display

# Storing magic numbers as constants is clean living
CHECKBOX_A_KEY = "A"
CHECKBOX_B_KEY = "B"


class SimpleGUI(Display):
    
    def ui_filename(self):
        """
        This is where you put the name of the ui file associated with this
        program
        :return:
        """
        return "simple.ui"
    
    # the "_=None" is to provide default values if none are provided
    def __init__(self, parent=None, args=None):
        """
        This initialization function runs once upon GUI launch
        :param parent:
        :param args:
        """
        # the super line makes sure that we call Display's init function
        super().__init__(parent=parent, args=args)
        
        # A dictionary to store the checked state of our checkboxes
        self.checked_dict: Dict = {CHECKBOX_A_KEY: False, CHECKBOX_B_KEY: False}
        
        # The following three object names came from the UI file
        # Here we're connecting their native signals to custom slots
        
        # https://doc.qt.io/qt-6/qabstractbutton.html#clicked
        self.ui.push_button.clicked.connect(self.display_options)
        
        # https://doc.qt.io/qt-6/qcheckbox.html#stateChanged
        # https://www.learnpython.org/en/Partial_functions
        self.ui.checkbox_a.stateChanged.connect(partial(self.manage_options,
                                                        CHECKBOX_A_KEY))
        self.ui.checkbox_b.stateChanged.connect(partial(self.manage_options,
                                                        CHECKBOX_B_KEY))
    
    @pyqtSlot(int)
    def manage_options(self, key: str, checked_state: int):
        """
        Maps the Qt checked status to a native bool in our internal dictionary
        :param key: desired dictionary key
        :param checked_state: Comes from the emitted signal
        :return:
        """
        self.checked_dict[key] = True if checked_state == Qt.Checked else False
    
    @pyqtSlot()
    def display_options(self):
        """
        Print our internal dictionary to our status label. We're using the
        JSON library to convert it to a string.
        :return:
        """
        self.ui.output_label.setText(json.dumps(self.checked_dict))
