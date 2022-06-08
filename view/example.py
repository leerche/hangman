import PySimpleGUI as sg

from controller.game_controller import GameController

game_controller = GameController()
word_status = game_controller.word_status()


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Bisherige Tips: '), sg.Text('Anzahl: 0')],
            [sg.Text(word_status)],
            [sg.InputText()],
            [sg.Button('Tip')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    game_controller.tip(values[0])
    game_status = game_controller.word_status()


window.close()