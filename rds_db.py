from flask import Flask, render_template, request
import pymysql
import os
from config import *


db_conn = pymysql.connect(
    host = customhost,
    port= 3306,
    user = customuser,
    password= custompass,
    db=customdb
)

def insert_details( fname, lname,pri_skill,location, phone, email, image=""):
    cur = db_conn.cursor()
    cur.execute("insert into employee (fname, lname, pri_skill, location, phone, email, image) values (%s,%s,%s,%s,%s,%s,%s)", (fname, lname,pri_skill, location, phone, email, image))
    db_conn.commit()
    

def get_details():
    cur = db_conn.cursor()
    cur.execute("select * from employee")
    details = cur.fetchall()
    return details

def update(id, fname, lname,pri_skill,location, phone, email, image=""):
    cur = db_conn.cursor()
    cur.execute("update employee set fname=%s, lname=%s, pri_skill=%s,location=%s, phone=%s, email=%s, image=%s where empid=%s", (fname, lname,pri_skill,location, phone, email, image,id))
    db_conn.commit()

