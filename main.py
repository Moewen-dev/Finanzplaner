# Finanzplaner von Tom und Caspar
import sys
import sqlite3
import hashlib
import FreeSimpleGUI as sg
from FreeSimpleGUI import TITLE_LOCATION_TOP_LEFT

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
    "main_frame"        : "-MAIN_FRAME-",
    "budget_frame"      : "-BUDGET_FRAME-",
    "category_frame"    : "-CATEGORY-FRAME-",
    "tr_act_frame"      : "-TR_ACT_FRAME-", # tr_act = transaction
    "budget_fr_btn"     : "-BUDGET_FR_BTN-",
    "category_fr_btn"   : "-CATEGORY_FR_BTN-",
    "tr_act_fr_btn"     : "-TR_ACT_FR_BTN-",
    "exit_btn"          : "-EXIT_BTN-",
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

budget_frame = [
    [],
]

category_frame = [
    [],
]

tr_act_frame = [
    [],
]

main_frame = [
    [
        sg.Frame(title="Budgets", title_location=TITLE_LOCATION_TOP_LEFT, layout=budget_frame, key=keys["budget_frame"], visible=False),
        sg.Frame(title="Transaktionen", title_location=TITLE_LOCATION_TOP_LEFT, layout=category_frame, key=keys["category_frame"], visible=False),
        sg.Frame(title="Kategorien", title_location=TITLE_LOCATION_TOP_LEFT, layout=tr_act_frame, key=keys["tr_act_frame"], visible=False)
    ],
    [
        sg.B(button_text="Budgets", key=keys["budget_fr_btn"]),
        sg.B(button_text="Transaktionen", key=keys["tr_act_fr_btn"]),
        sg.B(button_text="Kategorien", key=keys["category_fr_btn"]),
    ]
]

layout = [
    [
        sg.Frame(title="", layout=initial_window, visible=True, key=keys["init_frame"]),
        sg.Frame(title="", layout=main_frame, visible=False, key=keys["main_frame"]),
    ],
    [sg.Button(button_text="Exit", key=keys["exit_btn"])]
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


class Transaction:

    note = ""

    def __init__(self, transaction_id, user_id, category_id, amount, date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.date = date

    def debug_print(self):
        print(f'''Transaction Id  :   {self.transaction_id}
User Id         :   {self.user_id}
Category Id     :   {self.category_id}
Amount          :   {self.amount}
Date            :   {self.date}
Note            :   {self.note}''')


class Budget:

    def __init__(self, budget_id, user_id, category_id, name, amount, start_date, end_date):
        self.budget_id = budget_id
        self.user_id = user_id
        self.category_id = category_id
        self.name = name
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date

    def debug_print(self):
        print(f'''Budget Id       :   {self.budget_id}
User Id         :   {self.user_id}
Category Id     :   {self.category_id}
Name            :   {self.name}
Amount          :   {self.amount}
Start Date      :   {self.start_date}
End Date        :   {self.end_date}''')


class Category:

    def __init__(self, category_id, user_id, name):
        self.category_id = category_id
        self.user_id = user_id
        self.name = name

    def debug_print(self):
        print(f'''Category Id     :   {self.category_id}
User Id         :   {self.user_id}
Name            :   {self.name}''')


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

        print(event)

        # Beende den Mainloop, wenn das Fenster geschlossen wird
        if event == sg.WIN_CLOSED or event == keys["exit_btn"]:
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

        # Registrierungslogik
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

        # Anmeldelogik
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

            window[keys["init_frame"]].update(visible=False)
            window[keys["main_frame"]].update(visible=True)
            window[keys["main_frame"]].update(f"Benutzer: {user.username}")


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