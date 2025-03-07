# Finanzplaner von Tom und Caspar
import sys
import sqlite3
import FreeSimpleGUI as sg


db_name = "data.db"


keys = {
    "reg_username"      : "-REG_USERNAME-",
    "reg_pw"            : "-REG_PASSWORT-",
    "reg_pw_confirm"    : "-REG_PASSWORT_CONFIRM-",
    "login_username"    : "-LOGIN_USERNAME-",
    "login_pw"          : "-LOGIN_PW-",
    "reg_frame"         : "-REG_FRAME-",
    "login_frame"       : "-LOGIN_FRAME-",
    "init_frame"        : "-INIT_FRAME-",
    "login_btn"         : "-LOGIN_BTN-",
    "reg_btn"           : "-REG_BTN-",
    "reg_ok_btn"        : "-REG_OK_BTN-",
    "login_ok_btn"      : "-LOGIN_OK_BTN-",
    "login_erf"         : "-LOGIN_ERF-",
    "login_fal"         : "-LOGIN_FAL-",
    "login_fal_vers"    : "-LOGIN_FAL_VERS-"
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

login_col_3 = [
    [sg.Text('', size=(30,1), key=keys["login_erf"], text_color='green')],
    [sg.Text('', size=(30,1), key=keys["login_fal"], text_color='red')],
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
        sg.Text('Sie wurden erfolgreich Angemeldet!', size=(30,1), key=keys["login_erf"], visible=False),
        sg.Text('Anmeldename oder Passwort falsch, probieren sie es bitte erneut!', size=(50,1), key=keys["login_fal"], visible=False),
        sg.Text('verusche noch überig!', size=(30,1), key=keys["login_fal_vers"], visible=False)
    ]
]

layout = [
    [sg.Frame(title="", layout=initial_window, visible=True, key=keys["init_frame"])],
]

sql_statements = [
    """CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL,
    pw_hash TEXT NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userdata (id)
    );""",
    """CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userdata (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
    );""",
    """CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES userdata (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
    );"""
]

class User:

    def __init__(self, user_id, username, pw_hash):
        self.user_id = user_id
        self.username = username
        self.pw_hash = pw_hash

    def save(self, con, cur):
        pass


def main(con, cur):

    window = sg.Window(title="Finanzplaner", layout=layout)

    # DB Init


    while True:
        event, value = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == keys["reg_btn"]:
            window[keys["reg_frame"]].update(visible=True)
            window[keys["reg_ok_btn"]].update(visible=True)
            window[keys["reg_btn"]].update(visible=False)
            window[keys["login_btn"]].update(visible=False)

        if event == keys["login_btn"]:
            window[keys["login_frame"]].update(visible=True)
            window[keys["login_ok_btn"]].update(visible=True)
            window[keys["reg_btn"]].update(visible=False)
            window[keys["login_btn"]].update(visible=False)
            versuche = 3

        if event == keys["reg_ok_btn"]:
            print(value[keys["reg_username"]])

        if event == keys["login_ok_btn"]:
            if value[keys["login_username"]] == "admin" and value[keys["login_pw"]] == "admin123":
                window[keys["login_erf"]].update(visible=True)
            else:
                versuche -= 1
                window[keys["login_fal"]].update(visible=True)
                window[keys["login_fal_vers"]].update(f"Versuche übrig: {versuche}", visible=True)
                if versuche == 0:
                    sg.popup_error("Zu viele fehlgeschlagene Versuche! Programm wird beendet.")
                    break


if __name__ == "__main__":
    try:
        with sqlite3.connect(db_name) as con:
            cur = con.cursor()

            for statement in sql_statements:
                cur.execute(statement)
            con.commit()

            main(con, cur)

            sys.exit(0)
    except sqlite3.OperationalError as e:
        print(f"Failed to Open Database: {e}")
