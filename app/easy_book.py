# coding: utf-8
import datetime
from flask import Flask, request, render_template, jsonify, send_from_directory
import itertools
import json
import os
import sys

import db
import sprite

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))


app = CustomFlask(__name__)

HOST = "0.0.0.0"
PORT = "5000"


@app.route('/cm', methods=["POST"])
def cm():
    ct = db.get_all_member()
    # 当月の表を作成
    if len(ct) == 0:
        db.init_current_month()

    ct = db.get_all_member()
    checked = db.get_checked_member()

    result = {
        'ct': ct,
        'checked': checked
    }
    return jsonify(result)


@app.route('/uc', methods=['POST'])
def uc():
    before = json.loads(request.data)["checked"]
    after = db.get_checked_member()

    diff_num = len(before) - len(after)
    if diff_num == 0:
        return ''

    diff = list(set(after) ^ set(before))[0]

    # 削除
    if diff_num < 0:
        db.update_check(diff, 0)
    # 追加
    if diff_num > 0:
        db.update_check(diff, 1)

    return ''


@app.route('/am', methods=["POST"])
def am():
    name = json.loads(request.data)["name"]
    db.add_member(name)
    ct = db.get_all_member()
    result = {
        'ct': ct
    }
    return jsonify(result)


@app.route('/dm', methods=["POST"])
def delete_member():
    del_id = json.loads(request.data)["id"]
    db.delete_member(del_id)
    ct = db.get_all_member()
    result = {
        'ct': ct
    }
    return jsonify(result)


@app.route('/lb', methods=['POST'])
def lb():
    accounts = db.get_all_accounts()

    for row in accounts:
        row['kept'] = row['kept'].strftime('%Y/%m/%d')

    results = {
        "book": accounts,
    }
    return jsonify(results)


@app.route('/aa', methods=['POST'])
def add_account():
    to_add = json.loads(request.data)

    summary = to_add["summary"]
    incomes = int(to_add["incomes"]) if to_add["incomes"] is not None else 0
    expenses = int(to_add["expenses"]) if to_add["expenses"] is not None else 0

    db.insert_accounts(summary, incomes, expenses)

    return lb()


@app.route('/da', methods=['POST'])
def delete_account():
    to_delete_id = json.loads(request.data)["id"]
    db.delete_account(to_delete_id)
    return lb()


@app.route('/gb', methods=['POST'])
def get_total_balance():
    book_balance = db.get_book_sum()
    date = sprite.get_before_month()
    sql = "SELECT * FROM collection WHERE (DATE_FORMAT(`month`, '%Y-%m') = '{0}');".\
        format(date)
    result = db.execute_select(sql)
    checked = [row['id'] for row in result if row['check'] == 1]
    coll = len(db.get_checked_member()) * 500
    total_balance = book_balance + coll

    results = {
        "balance": total_balance
    }
    return jsonify(results)


def check_admin(user, password):
    tmp = db.get_account_info(user, password)

    if len(tmp) == 0:
        return False

    account_info = tmp[0]

    if user == account_info["name"] and password == account_info["password"]:
        return True

    return False


@app.route('/ia', methods=['POST'])
def ia():
    user = json.loads(request.data)["user"]
    password = json.loads(request.data)["password"]

    is_admin = check_admin(user, password)

    results = {
        "isAdmin": is_admin
    }

    return jsonify(results)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
def index():
    today = datetime.date.today()
    title = today.strftime("%Y-%m")
    return render_template("index.html", title=title)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
