import interbase

DB_CONFIG = {
    "dsn": r"localhost/instance2:C:\Descargas\proyectoTBD\PROYECTOTB1.IB",
    "user": "SYSDBA",
    "password": "masterkey",
    "charset": "NONE"
}


def get_conn():
    return interbase.connect(
        dsn=DB_CONFIG["dsn"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        charset=DB_CONFIG["charset"]
    )
