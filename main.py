import sys
from PyQt6.QtWidgets import *

from controller.game_controller import GameController

class StartGameForm(QDialog):
    def __init__(self, controller: GameController):
        super().__init__()
        self.controller = controller
        self.completer = QCompleter(self.controller.get_names())
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setCompleter(self.completer)
        self.form_layout.addRow(QLabel("Name:"), self.name_input)

        self.mode_input = QComboBox()
        self.mode_input.addItem("Casual", "casual")
        self.mode_input.addItem("Zeit", "time")

        self.mode_input.currentTextChanged.connect(self.mode_changed)

        self.form_layout.addRow(QLabel("Modus:"), self.mode_input)

        self.time_limit = QSpinBox()
        self.time_limit.hide()
        self.time_limit_label = QLabel("Zeitlimit (Minuten):")
        self.time_limit_label.hide()
        self.form_layout.addRow(self.time_limit_label, self.time_limit)
        self.formGroupBox.setLayout(self.form_layout)

    def mode_changed(self, value: str):
        if value == "Zeit":
            self.time_limit.show()
            self.time_limit_label.show()
        else:
            self.time_limit.hide()
            self.time_limit_label.hide()

    def accept(self):
        self.controller.start(self.name_input.text(), self.mode_input.currentData(), self.time_limit.value())
class MainWindow(QMainWindow):

    def __init__(self):
        self.controller = GameController()
        super().__init__()
        self.initUI()

    def initUI(self):

        btn1 = QPushButton("Start Game", self)
        btn1.move(175, 150)

        btn1.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(500, 500, 450, 350)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked(self):
        self.w = StartGameForm(self.controller)
        self.w.show()

def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()