# Finanzplaner von Tom und Casper
import sys

import FreeSimpleGUI as sg


layout = [[sg.Text("Test")],]


def main():

    window = sg.Window(title="Finanzplaner", layout=layout)

    while True:
        event, value = window.read()

        if event == sg.WIN_CLOSED:
            break


if __name__ == "__main__":
    main()
    sys.exit(0)
