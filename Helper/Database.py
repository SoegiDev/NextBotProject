import mysql.connector
from dotenv import load_dotenv
import os

my_database = mysql.connector.connect()
setting_table = "c_setting"
credential_table = "m_credential"
balance_table = "t_user_balance"
users_table = "m_users"
roles_table = "m_roles"
system_table = "c_system"
orders_table = "t_orders"
binance_orders_table = "t_binance_orders"
session_table = "tbl_sessions"

create_setting = (f"CREATE TABLE {setting_table} (id int(11) NOT NULL AUTO_INCREMENT,"
                  "app_name varchar(50) DEFAULT NULL,"
                  "host_name varchar(50) DEFAULT NULL,"
                  "ip_address varchar(50) NOT NULL,"
                  "default_printer varchar(50) NOT NULL,"
                  "created_date varchar(100) DEFAULT NULL,"
                  "updated_date varchar(100) DEFAULT NULL,"
                  "PRIMARY KEY (id)"
                  ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")
create_credential = (f"CREATE TABLE {credential_table} (id int(11) NOT NULL AUTO_INCREMENT,"
                     "platform_name varchar(20) DEFAULT NULL,"
                     "user_id int(11) NOT NULL,"
                     "api_key text DEFAULT NULL,"
                     "secret_key text DEFAULT NULL,"
                     "created_date varchar(100) DEFAULT NULL,"
                     "updated_date varchar(100) DEFAULT NULL,"
                     "PRIMARY KEY (id)"
                     ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")

create_balance = (f"CREATE TABLE {balance_table} (id int(11) NOT NULL AUTO_INCREMENT,"
                  "asset varchar(20) DEFAULT NULL,"
                  "balance decimal(15,2) DEFAULT 0,"
                  "user_id int(11) NOT NULL,"
                  "account_number text DEFAULT NULL,"
                  "account_name text DEFAULT NULL,"
                  "created_date varchar(100) DEFAULT NULL,"
                  "updated_date varchar(100) DEFAULT NULL,"
                  "PRIMARY KEY (id)"
                  ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")

create_user = (f"CREATE TABLE {users_table} (id int(11) NOT NULL AUTO_INCREMENT,"
               "nick_name varchar(20) DEFAULT NULL,"
               "full_name varchar(25) NOT NULL,"
               "phone_number varchar(50) NOT NULL,"
               "email_address varchar(50) NOT NULL,"
               "password varchar(50) NOT NULL,"
               "password_hash varchar(75) NOT NULL,"
               "designation varchar(100) DEFAULT NULL,"
               "role_id int(11) DEFAULT NULL,"
               "is_login tinyint(1) NOT NULL DEFAULT 1,"
               "PRIMARY KEY (id)"
               ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")

create_roles = (f"CREATE TABLE {roles_table} (id int(11) NOT NULL AUTO_INCREMENT,"
                "role_name varchar(20) DEFAULT NULL,"
                "created_date varchar(100) DEFAULT NULL,"
                "updated_date varchar(100) DEFAULT NULL,"
                "PRIMARY KEY (id)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")

create_system = (f"CREATE TABLE {system_table} (id int(11) NOT NULL AUTO_INCREMENT,"
                 "key_name varchar(20) DEFAULT NULL,"
                 "value_key text DEFAULT NULL,"
                 "created_date varchar(100) DEFAULT NULL,"
                 "updated_date varchar(100) DEFAULT NULL,"
                 "PRIMARY KEY (id)"
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")

create_orders = (f" CREATE TABLE {orders_table}( id int(11) NOT NULL AUTO_INCREMENT,"
                 "order_id  int(11) DEFAULT 0,"
                 "symbol varchar(10) DEFAULT NULL,"
                 "amount	decimal(15,2) DEFAULT 0,"
                 "price decimal(15,2) DEFAULT 0,"
                 "side varchar(5) DEFAULT 'BUY',"
                 "quantity decimal(10,2) DEFAULT 0,"
                 "profit decimal(15,2) DEFAULT 0,"
                 "created_date varchar(100) DEFAULT NULL,"
                 "updated_date varchar(100) DEFAULT NULL,"
                 "PRIMARY KEY (id)"
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")

create_sessions = (f" CREATE TABLE {session_table}( id varchar(128) NOT NULL,"
                   "ip_address  varchar(45) DEFAULT 0,"
                   "timestamp int(11) DEFAULT NULL,"
                   "data	blob DEFAULT NULL,"
                   "PRIMARY KEY (id)"
                   ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci")


class Database:

    @staticmethod
    def connect():
        global my_database
        my_database = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        if my_database.is_connected():
            return my_database
        else:
            return False

    @staticmethod
    def create_table(conn):
        data_tabel = [{"name": users_table, "init": create_user}, {"name": roles_table, "init": create_roles},
                      {"name": credential_table, "init": create_credential},
                      {"name": system_table, "init": create_system}, {"name": balance_table, "init": create_balance},
                      {"name": setting_table, "init": create_setting}, {"name": orders_table, "init": create_orders},
                      {"name": session_table, "init": create_sessions}]
        result = []
        message = {}
        for i, a in enumerate(data_tabel):
            try:
                check = Database.check_table(conn, a['name'])
                if not check:
                    conn.execute(a["init"])
                    message = {"tbl_name": a['name'], "status": "Berhasil Created", "code": 200}
                else:
                    message = {"tbl_name": a['name'], "status": "Table Already Exist", "code": 400}
            except EOFError as e:
                message = {"tbl_name": a, "status": e}
            result.append(message)
        return result

    @staticmethod
    def check_table(conn, table):
        stmt = f"SHOW TABLES LIKE '{table}'"
        conn.execute(stmt)
        result = conn.fetchone()
        if result:
            return True
        else:
            return False
