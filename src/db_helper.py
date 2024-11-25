from sqlalchemy import text
from config import db, app

def table_exists(name):
    sql_table_existence = text(
        "SELECT EXISTS ("
        "  SELECT 1"
        "  FROM information_schema.tables"
        f" WHERE table_name = '{name}'"
        ")"
    )

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def setup_db():
    if table_exists("refs"):
        sql = text("DROP TABLE refs;")
        db.session.execute(sql)
        db.session.commit()

    sql = text("SELECT 1;")
    with open('schema.sql', 'r', encoding="utf-8") as file:
        sql = text(file.read())

    db.session.execute(sql)
    test_data_sql = text("SELECT 1;")
    with open('test_data.sql', 'r', encoding="utf-8") as file:
        test_data_sql = text(file.read())

    db.session.execute(test_data_sql)
    db.session.commit()

def reset_db():
    setup_db()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
