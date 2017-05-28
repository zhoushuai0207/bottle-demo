#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sqlite3
import uuid

from bottle import Bottle, request, run, response

app = Bottle()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


DB_FILE = 'chinac.db'
dbfile = os.path.join(os.path.dirname(__file__), DB_FILE)

conn = sqlite3.connect(dbfile)
conn.row_factory = dict_factory
cursor = conn.cursor()


def get_uuid():
    """生成数据库主键"""
    return uuid.uuid1().get_hex()


def sql_create_table():
    '''创建数据库表测试'''
    _create_table_sql = """
        CREATE TABLE `host` (
        `id`  TEXT(36) NOT NULL,
        `hostname`  TEXT(128) NOT NULL,
        `mac`  TEXT(24) NOT NULL,
        `cpu`  INTEGER,
        `mem`  INTEGER
        );
    """


def sql_get_single_host_info(host_id=None):
    """获取单个主机信息"""
    try:
        sql = "SELECT id, hostname, mac, cpu, mem FROM host WHERE id = '%s'" % (host_id,)
        print sql
        cursor.execute(sql)
        values = json.dumps(cursor.fetchone())
        return True, values
    except Exception as e:
        print "获取单个主机信息失败 %s" % str(e)
        return False, str(e)


def sql_get_all_host_info(filter=None):
    """获取所有的主机信息"""
    try:
        if filter:
            sql = "SELECT id, hostname, mac, cpu, mem FROM host WHERE hostname like '%{filter}%' or mac  like '%{filter}%'".format(
                    **{"filter": filter})
        else:
            sql = "SELECT id, hostname, mac, cpu, mem FROM host"
        print sql
        cursor.execute(sql)
        values = json.dumps(cursor.fetchall())
        return True, values
    except Exception as e:
        print "获取主机信息失败 %s" % str(e)
        return False, str(e)


def sql_update_host_info(host_id, host_infos=None):
    """更新主机信息"""
    try:
        sql = "UPDATE host set {} WHERE id = '{}'"
        t = []
        if "hostname" in host_infos and len(host_infos["hostname"]):
            t.append(" hostname = '%s' " % (host_infos["hostname"],))
        if "mac" in host_infos and len(host_infos["mac"]):
            t.append(" mac = '%s' " % (host_infos["mac"],))
        if "cpu" in host_infos:
            t.append(" cpu = %s " % (host_infos["cpu"],))
        if "mem" in host_infos:
            t.append(" mem = %s " % (host_infos["mem"],))
        sql = sql.format(",".join(t), host_id)
        print sql
        cursor.execute(sql)
        conn.commit()
        return True, "ok"
    except Exception as e:
        print "更新主机信息 失败 %s" % str(e)
        return False, str(e)


def sql_delete_host_info(host_id=None):
    """删除主机信息"""
    try:
        sql = "DELETE FROM host WHERE id = '{}'".format(host_id)
        print sql
        cursor.execute(sql)
        conn.commit()
        return True, "ok"
    except Exception as e:
        print "删除主机信息失败 %s" % str(e)
        return False, str(e)


def sql_create_host_info(hosts_info):
    """新增主机信息"""
    try:
        sql = "INSERT INTO host (id, hostname, mac, cpu, mem) values ('{id}', '{hostname}', '{mac}', {cpu}, {mem}) ".format(
                **hosts_info)
        print sql
        cursor.execute(sql)
        conn.commit()
        return True, "ok"
    except Exception as e:
        print str(e)
        return False, str(e)


@app.route("/hosts/<host_id>", method="GET")
def get_host_info(host_id):
    """获取单个主机信息"""
    is_ok, msg = sql_get_single_host_info(host_id)
    if is_ok:
        response.status = 200
    else:
        response.status = 400
    return msg


@app.route("/hosts/<host_id>", method="PUT")
def update_host_info(host_id):
    """修改主机信息"""
    r_data = {}
    try:
        body = json.loads(request.body.read())
    except ValueError:
        r_data["msg"] = "参数不是一个有效的 json 字符串"
        response.status = 400
        return r_data
    is_ok, msg = sql_update_host_info(host_id, body)
    if is_ok:
        response.status = 200
        _, msg = sql_get_single_host_info(host_id)
        r_data = msg
    else:
        response.status = 400
        r_data["msg"] = "更新数据失败 失败原因 %s" % msg
    return r_data


@app.route("/hosts", method="GET")
def get_hosts_info():
    """获取所有主机信息"""
    _filter = request.GET.get('filter', None)
    is_ok, msg = sql_get_all_host_info(filter=_filter)
    if is_ok:
        response.status = 201
    else:
        response.status = 400
    return msg


@app.route("/hosts", method="POST")
def add_host_info():
    """增加主机信息"""
    r_data = {"msg": "success"}
    try:
        body = json.loads(request.body.read())
    except ValueError:
        r_data["msg"] = "参数不是一个有效的 json 字符串"
        response.status = 400
        return r_data
    if "hostname" not in body or not body["hostname"]:
        r_data["msg"] = "参数 hostname 必须传并且不能为空"
        response.status = 400
        return r_data
    if "mac" not in body or not body["mac"]:
        r_data["msg"] = "参数 mac 必须传并且不能为空"
        response.status = 400
        return r_data
    host_info = {
        "id": get_uuid(),
        "hostname": body["hostname"],
        "mac": body["mac"],
        "cpu": body.get("cpu", 0),
        "mem": body.get("mem", 0)
    }
    is_ok, msg = sql_create_host_info(host_info)
    if is_ok:
        response.status = 201
        r_data = host_info
    else:
        response.status = 400
        r_data["msg"] = "新增失败 失败原因 %s" % msg
    return r_data


@app.route("/hosts/<host_id>", method="DELETE")
def delete_host_info(host_id):
    """删除主机信息"""
    is_ok, msg = sql_get_single_host_info(host_id)
    print msg
    if is_ok and msg != "null":
        is_ok, msg = sql_delete_host_info(host_id)
        if is_ok:
            response.status = 204
            msg = ""
        else:
            response.status = 400
    else:
        response.status = 400
        msg = {"msg": "删除资源，没有发现对应的资源 %s" % host_id}
    return msg


if __name__ == "__main__":
    run(app, host='0.0.0.0', port=9090, debug=True)
