# Finanzplaner von Tom und Caspar
import sys

import FreeSimpleGUI as sg


keys = {
    "reg_username"      : "-REG_USERNAME-",
    "reg_pw"            : "-REG_PASSWORT-",
    "reg_pw_confirm"    : "-REG_PASSWORT_CONFIRM",
    "login_username"    : "-LOGIN_USERNAME-",
    "login_pw"          : "-LOGIN_PW-",
    "reg_frame"         : "-REG_FRAME-",
    "login_frame"       : "-LOGIN_FRAME-",
    "init_frame"        : "-INIT_FRAME-",
    "login_btn"         : "-LOGIN-BTN-",
    "reg_btn"           : "-REG_BTN-",
    "reg_ok_btn"        : "-REG_OK_BTN-",
    "login_ok_btn"      : "-LOGIN_OK_BTN-"
}

reg_col_1 = [[sg.T("Username")],[sg.T("Passwort")],[sg.T("Passwort wiederholen")]]

reg_col_2 = [
    [sg.Input(default_text="", key=keys["reg_username"])],
    [sg.Input(default_text="", key=keys["reg_pw"])],
    [sg.Input(default_text="", key=keys["reg_pw_confirm"])],
]

reg_frame = [[sg.Col(layout=reg_col_1), sg.Col(layout=reg_col_2)],]

login_col_1 = [[sg.T("Username:")],[sg.T("Passwort:")],]

login_col_2 = [
    [sg.Input(default_text="", key=keys["login_username"])],
    [sg.Input(default_text="", key=keys["login_pw"])],
]

login_frame = [[sg.Col(layout=login_col_1), sg.Col(layout=login_col_2)],]

initial_window = [
    [
        sg.Frame(title="Registrierung", layout=reg_frame, visible=False, key=keys["reg_frame"]),
        sg.Frame(title="Anmelden", layout=login_frame, visible=False, key=keys["login_frame"]),
    ],
    [
        sg.Button(button_text="Anmelden", key=keys["login_btn"]),
        sg.Button(button_text="Registrieren", key=keys["reg_btn"]),
        sg.Button(button_text="Ok", key=keys["reg_ok_btn"], visible=False),
        sg.Button(button_text="Ok", key=keys["login_ok_btn"], visible=False),
    ]
]

layout = [
    [sg.Frame(title="", layout=initial_window, visible=True, key=keys["init_frame"])],
]


def main():

    window = sg.Window(title="Finanzplaner", layout=layout)

    while True:
        event, value = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == keys["reg_btn"]:
            window[keys["reg_frame"]].update(visible=True)
            window[keys["reg_ok_btn"]].update(visible=True)
            window[keys["reg_btn"]].update(visible=False)
            window[keys["login_btn"]].update(visible=False)

        if event == keys["reg_ok_btn"]:
            print(value[keys["reg_username"]])


if __name__ == "__main__":
    main()
    sys.exit(0)
