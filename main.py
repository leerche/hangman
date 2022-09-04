from ast import Expression
import sys
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QTimer, QTime, QRegularExpression

from controller.game_controller import GameController
from data.encode import WordEncode

class StartGameForm(QDialog):

    def __init__(self, controller: GameController):
        super().__init__()
        self.controller = controller
        self.setWindowIcon(QIcon('assets/hangman.png'))
        self.setWindowTitle('Start Game')

        self.completer = QCompleter(self.controller.get_names())
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.validateinput)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def validateinput(self):
        if len(self.name_input.text()):
            self.accept()
        else:
            self.name_input.setPlaceholderText("Name Required")
        
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox()
        self.form_layout = QFormLayout()
        rx = QRegularExpression("[A-z0-9]{20}")

        self.name_input = QLineEdit(self)
        validator = QRegularExpressionValidator(rx)
        self.name_input.setValidator(validator)

        self.name_input.setCompleter(self.completer)
        self.form_layout.addRow(QLabel("Name:"), self.name_input)

        self.mode_input = QComboBox()
        self.mode_input.addItem("Casual", "casual")
        self.mode_input.addItem("Zeit", "time")

        self.mode_input.currentTextChanged.connect(self.mode_changed)

        self.form_layout.addRow(QLabel("Modus:"), self.mode_input)

        self.time_limit = QSpinBox()
        self.time_limit.setMaximum(59)
        self.time_limit.setMinimum(1)
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

class GameEndedForm(QDialog):

    def __init__(self, controller: GameController, time: QLabel):
        super().__init__()
        self.controller = controller

        self.time = time
        self.setWindowIcon(QIcon('assets/hangman.png'))

        self.setWindowTitle('Game Ended')

        if(self.controller.isTimeGame()):
            self.timeLabel = QLabel("Verbliebende Zeit: ")
        else:
            self.timeLabel = QLabel("Benötigte Zeit: ")
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttonBox.accepted.connect(self.close)

        if(self.controller.isWon()):
            game_status = QLabel("Gewonnen!")
        else:
            game_status = QLabel("Verloren!")
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.timeLabel, 2, 1)
        mainLayout.addWidget(self.time, 2, 2)
        mainLayout.addWidget(game_status, 1, 1)
        mainLayout.addWidget(buttonBox, 3, 2)
        self.setLayout(mainLayout)

    def close(self):
        sys.exit()

class MainWindow(QMainWindow):

    def __init__(self):
        self.controller = GameController()
        super().__init__()
        central_widget = QWidget()
        self.tip_button = QPushButton("Tip", self)
        self.tip_button.clicked.connect(self.tip)

        self.tip_input = QLineEdit()
        self.tip_input.returnPressed.connect(self.tip)

        self.used_characters = QLabel("Benutzte Zeichen: ")
        self.word_status = QLabel()

        self.tip_amount = QLabel()
        self.correct_tip_amount = QLabel()

        self.timer = QTimer()

        self.time = QLabel()

        game_layout = QGridLayout()

        game_layout.addWidget(self.time, 5, 1)

        game_layout.addWidget(self.used_characters, 1, 1)

        game_layout.addWidget(self.tip_amount, 1, 2)
        game_layout.addWidget(self.correct_tip_amount, 1, 3)

        game_layout.addWidget(self.word_status, 2, 1, 1, 3, Qt.AlignmentFlag.AlignCenter)

        game_layout.addWidget(self.tip_input, 3, 1)
        game_layout.addWidget(self.tip_button, 3, 2)


        central_widget.setLayout(game_layout)

        self.setCentralWidget(central_widget)
        self.centralWidget().hide()
        self.initUI()


    def initUI(self):

        self.start_game_button = QPushButton("Start Game", self)
        self.start_game_button.move(175, 150)

        self.start_game_button.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(500, 500, 450, 350)
        self.setWindowIcon(QIcon('assets/hangman.png'))
        self.setWindowTitle('Hangman by Robert, Jonas, Lea & Christopher')
        self.show()

    def buttonClicked(self):
        self.w = StartGameForm(self.controller)
        self.w.open()
        self.w.accepted.connect(self.startGame)
    
    def startGame(self):
        self.controller.start(self.w.name_input.text(), self.w.mode_input.currentData(), self.w.time_limit.value())

        if(self.w.mode_input.currentData() == "casual"):
            self.curr_time = QTime(00,00,00)
            self.timer.timeout.connect(self.showTime)
            self.timer.start(1000)
            self.time.setText(self.curr_time.toString('hh:mm:ss'))
        elif(self.w.mode_input.currentData() == "time"):
            time = self.w.time_limit.value()
            self.curr_time = QTime(00,time,00)
            self.timer.timeout.connect(self.showCountdown)
            self.timer.start(1000)
            self.time.setText(self.curr_time.toString('hh:mm:ss'))


        self.updateWordStatus()
        self.updateCorrectTipAmount()
        self.updateTipAmount()
        self.centralWidget().show()
        self.start_game_button.hide()


    def tip(self):
        self.controller.tip(self.tip_input.text())
        self.resetTipInput()
        self.updateWordStatus()
        self.updateUsedCharacters()
        self.updateCorrectTipAmount()
        self.updateTipAmount()
        self.checkGameStatus()


    def updateCorrectTipAmount(self):
        self.correct_tip_amount.setText("davon Richtig: " + self.controller.correct_tip_amount())

    def updateTipAmount(self):
        self.tip_amount.setText("Anzahl Tips: " + self.controller.tip_amount())

    def updateUsedCharacters(self):
        self.used_characters.setText("Benutzte Zeichen: " + self.controller.tips())
    
    def updateWordStatus(self):
        self.word_status.setText(self.controller.word_status())

    def checkGameStatus(self):
        if self.controller.isWon():
            self.timer.stop()
            self.w = GameEndedForm(self.controller, self.time)
            self.w.open()
        elif self.controller.isLost():
            self.timer.stop()
            self.w = GameEndedForm(self.controller, self.time)
            self.w.open()
    
    def resetTipInput(self):
        self.tip_input.setText("")

    def showTime(self):
        self.curr_time = self.curr_time.addSecs(1)
        timeDisplay=self.curr_time.toString('hh:mm:ss')
        self.time.setText(timeDisplay)

    def showCountdown(self):
        self.curr_time = self.curr_time.addSecs(-1)
        if(self.curr_time.second() == 0):
            self.timer.stop()
            self.w = GameEndedForm(self.controller, self.time)
            self.w.open()
        timeDisplay=self.curr_time.toString('hh:mm:ss')

        self.time.setText(timeDisplay)

def main():

    word_encode = WordEncode()
    word_encode.write()

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()