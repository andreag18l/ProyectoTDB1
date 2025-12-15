from db import get_conn

def main():
    con = get_conn()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM USUARIO")
    total = cur.fetchone()[0]
    print("Usuarios:", total)

    cur.close()
    con.close()

if __name__ == "__main__":
    main()
from db import get_conn

