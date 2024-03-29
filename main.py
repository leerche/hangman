import sys
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QTimer, QTime, QRegularExpression

from controller.game_controller import GameController
from data.encode import WordEncode

# Dialog zum Spielstart:
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

        
    # Validierung der Benutzereingaben:
    def validateinput(self):
        if len(self.name_input.text()):
            self.accept()
        else:
            self.name_input.setPlaceholderText("Name Required")
    
    # erzeuge das Formular zum Spielstart (Spielernamen eingeben, Spielmodus auswählen):
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

    # Ändere die im Formular dargestellten Elemente bei Wechsel des Spielmodus:
    def mode_changed(self, value: str):
        if value == "Zeit":
            self.time_limit.show()
            self.time_limit_label.show()
        else:
            self.time_limit.hide()
            self.time_limit_label.hide()
            
# Dialog zum Spielende:
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

    # beende das Programm:
    def close(self):
        sys.exit()
        
# Hauptfenster, in welchem das Spiel stattfindet:
class MainWindow(QMainWindow):
    # Definition und Anordnung der UI-Elemente:
    def __init__(self):
        self.controller = GameController()
        super().__init__()
        central_widget = QWidget()
        self.tip_button = QPushButton("Tip", self)
        self.tip_button.clicked.connect(self.tip)

        self.tip_input = QLineEdit()
        self.tip_input.returnPressed.connect(self.tip)

        self.name = QLabel()
       
        self.used_characters = QLabel("Benutzte Zeichen: ")
        self.word_status = QLabel()

        self.tip_amount = QLabel()
        self.correct_tip_amount = QLabel()

        self.timer = QTimer()

        self.time = QLabel()


        self.game_layout = QGridLayout()

        self.game_layout.addWidget(self.time, 5, 1)
        self.game_layout.addWidget(self.name, 0, 1, 1, 3)

        self.game_layout.addWidget(self.used_characters, 1, 1)

        self.game_layout.addWidget(self.used_characters, 1, 1)

        self.game_layout.addWidget(self.tip_amount, 1, 2)
        self.game_layout.addWidget(self.correct_tip_amount, 1, 3)

        self.game_layout.addWidget(self.word_status, 4, 1, 2, 3, Qt.AlignmentFlag.AlignHCenter)

        self.game_layout.addWidget(self.tip_input, 6, 1)
        self.game_layout.addWidget(self.tip_button, 6, 2)


        central_widget.setLayout(self.game_layout)

        self.setCentralWidget(central_widget)
        self.centralWidget().hide()
        self.initUI()

    # zeige die UI des Spiels:
    def initUI(self):

        self.start_game_button = QPushButton("Start Game", self)
        self.start_game_button.move(175, 150)

        self.start_game_button.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(500, 500, 450, 350)
        self.setWindowIcon(QIcon('assets/hangman.png'))
        self.setWindowTitle('Hangman by Robert, Jonas, Lea & Christopher')
        self.show()

    # Klick auf den Button, welcher den Start des Spiels auslöst:
    def buttonClicked(self):
        self.w = StartGameForm(self.controller)
        self.w.open()
        self.w.accepted.connect(self.startGame)

    # Start des Spiels:
    def startGame(self):
        self.controller.start(self.w.name_input.text(), self.w.mode_input.currentData(), self.w.time_limit.value())
        
        self.updateGraphic()
        
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
        self.name.setText("Spieler: " + self.controller.getName()) 
        self.updateCorrectTipAmount()
        self.updateTipAmount()
        self.centralWidget().show()
        self.start_game_button.hide()

    # Verarbeitung der Eingabe eines Zeichen:
    def tip(self):
        self.controller.tip(self.tip_input.text())
        self.resetTipInput()
        self.updateWordStatus()
        self.updateUsedCharacters()
        self.updateCorrectTipAmount()
        self.updateTipAmount()
        self.checkGameStatus()
        self.updateGraphic()

    # aktualisiere die Anzahl korrekt erratener Buchstaben:
    def updateCorrectTipAmount(self):
        self.correct_tip_amount.setText("davon Richtig: " + self.controller.correct_tip_amount())

    # aktualisiere die Anzahl abgegebener Tips:
    def updateTipAmount(self):
        self.tip_amount.setText("Anzahl Tips: " + self.controller.tip_amount())
    # aktualisiere die Liste der benutzen Buchstaben:
    def updateUsedCharacters(self):
        self.used_characters.setText("Benutzte Zeichen: " + self.controller.tips())
    # aktualisiere die Darstellung des Lösungswortes:
    def updateWordStatus(self):
        self.word_status.setText(self.controller.word_status())

    # prüfe, ob das Spiel bereits gewonnen/verloren wurde:
    def checkGameStatus(self):
        if self.controller.isWon():
            self.timer.stop()
            self.w = GameEndedForm(self.controller, self.time)
            self.w.open()
        elif self.controller.isLost():
            self.timer.stop()
            self.w = GameEndedForm(self.controller, self.time)
            self.w.open()
    
    # leere die Eingabe für den zu erratenen Buchstaben
    def resetTipInput(self):
        self.tip_input.setText("")

    # aktualisiere den Timer:
    def showTime(self):
        self.curr_time = self.curr_time.addSecs(1)
        timeDisplay=self.curr_time.toString('hh:mm:ss')
        self.time.setText(timeDisplay)

    # aktualisiere den Countdown:
    def showCountdown(self):
        self.curr_time = self.curr_time.addSecs(-1)
        if(self.curr_time.second() == 0):
            self.timer.stop()
            self.w = GameEndedForm(self.controller, self.time)
            self.w.open()
        timeDisplay=self.curr_time.toString('hh:mm:ss')

        self.time.setText(timeDisplay)
    
    def updateGraphic(self):
        if not hasattr(self, 'graphic'):
            self.graphic = QLabel(self.controller.graphic.getGraphic())
            self.game_layout.addWidget(self.graphic, 2, 1, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        else: 
            self.graphic.setText(self.controller.graphic.getGraphic())
        


def main():
    # erstellen und verschlüsseln der Wörter:
    word_encode = WordEncode()
    word_encode.write()
    # Start der App:
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())

# Initialer Startpunkt des Programms:
if __name__ == '__main__':
    main()