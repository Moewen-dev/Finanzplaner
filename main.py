# Finanzplaner von Tom und Caspar
import sys
import sqlite3
import hashlib
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
        sg.Frame(title="Registrieren", layout=reg_frame, visible=False, key=keys["reg_frame"]),
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

sql_statements = [
    """CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER NOT NULL PRIMARY KEY, 
    username TEXT NOT NULL,
    pw_hash TEXT NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS categories (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userdata (id)
    );""",
    """CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER NOT NULL PRIMARY KEY,
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
    id INTEGER NOT NULL PRIMARY KEY,
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

    def __init__(self, username, pw_hash):
        self.logged_in = False

        self.user_id = 0
        self.username = username
        self.pw_hash = pw_hash

    def save(self, connection, cursor):
        cursor.execute("INSERT INTO userdata (username, pw_hash) VALUES (?, ?)",(self.username, self.pw_hash))
        connection.commit()

    def debug_print(self):
        print(f"""User Id:    {self.user_id}
Username:   {self.username}
Pw Hash:    {self.pw_hash}""")


def login(userdata, username, pw_hash):
    for data in userdata:
        data_user_id = data[0]
        data_username = data[1]
        data_pw_hash = data[2]
        if data_username == username and data_pw_hash == pw_hash:
            return True, data_user_id
    return False, 0





def main(connection, cursor):

    window = sg.Window(title="Finanzplaner", layout=layout)

    user = User(None, None)

    # Mainloop
    while True:
        event, value = window.read()

        # Beende Main Loop wenn das Fenster geschlossen wird
        if event == sg.WIN_CLOSED:
            break

        # Zeige den Registrierungsbereich
        if event == keys["reg_btn"]:
            window[keys["reg_frame"]].update(visible=True)
            window[keys["reg_ok_btn"]].update(visible=True)
            window[keys["reg_btn"]].update(visible=False)
            window[keys["login_btn"]].update(visible=False)

        # Zeige den Loginbereich
        if event == keys["login_btn"]:
            window[keys["login_frame"]].update(visible=True)
            window[keys["login_ok_btn"]].update(visible=True)
            window[keys["reg_btn"]].update(visible=False)
            window[keys["login_btn"]].update(visible=False)

        # Registrierungslogick
        if event == keys["reg_ok_btn"]:
            reg_pw = value[keys["reg_pw"]]
            reg_pw_conf = value[keys["reg_pw_confirm"]]
            username = value[keys["reg_username"]]

            if username == "":
                sg.popup_error("Username ist leer")
                continue

            if reg_pw != reg_pw_conf:
                sg.popup_error("Passwort ist nicht gleich.")
                continue

            user.username = username
            user.pw_hash = hashlib.sha512(str.encode(reg_pw)).hexdigest()
            user.save(connection, cursor)

            user.debug_print()

            window[keys["reg_frame"]].update(visible=False)
            window[keys["reg_ok_btn"]].update(visible=False)
            window[keys["login_frame"]].update(visible=True)
            window[keys["login_ok_btn"]].update(visible=True)

        # Anmeldelogick
        if event == keys["login_ok_btn"]:
            userdata = cursor.execute("SELECT * FROM userdata").fetchall()
            username = value[keys["login_username"]]
            pw_hash = hashlib.sha512(str.encode(value[keys["login_pw"]])).hexdigest()

            success, user_id = login(userdata, username, pw_hash)
            if not success:
                sg.popup_ok(f"Anmeldung fehlgeschlagen.\nBenutzername oder Passwort falsch?")
                continue
            user.user_id = user_id
            user.username = username
            user.pw_hash = pw_hash

            window[keys["login_frame"]].update(visible=False)
            window[keys["login_ok_btn"]].update(visible=False)
            window[keys["init_frame"]].update(f"Benutzer: {user.username}")
            user.debug_print()


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
        sys.exit(1)