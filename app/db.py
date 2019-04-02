# coding: utf-8
import mysql.connector
from flask import jsonify
import sys

import sprite

# データベースの設定
config = {
    "user": "root",
    "password": "root",
    "host": "eb-db",
    "database": "cashbook"
}


def create_connector_and_cursor():
    """
    データベースとの接続をつくる
    """
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True, dictionary=True)
    return cnx, cursor


def execute_sql(sql):
    """
    select以外のsqlを実行する
    """
    cnx, cursor = create_connector_and_cursor()
    try:
        cursor.execute(sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        cnx.rollback()
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")


def execute_select(sql):
    cnx, cursor = create_connector_and_cursor()
    result = ""
    try:
        cursor.execute(sql)
        cnx.commit()
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        cnx.rollback()
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")
    return result


def get_all_member():
    date = sprite.get_current_month()
    sql = "SELECT * FROM collection WHERE (DATE_FORMAT(`month`, '%Y-%m') = '{0}');".\
        format(date)
    return execute_select(sql)


def get_checked_member():
    result = get_all_member()
    checked = [row['id'] for row in result if row['check'] == 1]
    return checked


def delete_member(id):
    sql = "DELETE FROM collection WHERE id = {0};".format(id)
    execute_sql(sql)


def add_member(name):
    sql = "INSERT INTO collection (`name`, `check`) VALUES ('{0}', 0);".\
        format(name)
    execute_sql(sql)


def init_current_month():
    date = sprite.get_before_month()
    sql = "SELECT * FROM collection WHERE (DATE_FORMAT(`month`, '%Y-%m') = '{0}');".\
        format(date)
    now = execute_select(sql)

    for row in now:
        add_member(row['name'])

    return True


def update_check(id, action):
    sql = "UPDATE collection SET `check` = {0} WHERE `id` = {1};".format(action, id)
    execute_sql(sql)


def get_all_accounts():
    date = sprite.get_current_month()
    sql = "SELECT * FROM book WHERE (DATE_FORMAT(`kept`, '%Y-%m') = '{0}');".\
        format(date)
    return execute_select(sql)


def insert_accounts(summary, income, expenses):
    sql = "INSERT INTO book (`summary`, `incomes`, `expenses`)" \
          "VALUES ('{0}', {1}, {2});".\
          format(summary,
                 income,
                 expenses)
    execute_sql(sql)


def delete_account(id):
    sql = "DELETE FROM book WHERE `id` = {0};".\
        format(id)
    execute_sql(sql)


def get_book_sum():
    sql = "SELECT SUM(incomes) FROM book;"
    total_incomes = int(list(execute_select(sql)[0].values())[0])

    sql = "SELECT SUM(expenses) FROM book;"
    total_expenses = int(list(execute_select(sql)[0].values())[0])

    balance = total_incomes - total_expenses
    return balance


def get_account_info(user, password):
    sql = "SELECT * FROM admin WHERE `name` = '{0}' AND `password` = '{1}'".format(user, password)
    return execute_select(sql)
