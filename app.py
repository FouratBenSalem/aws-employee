import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask import Response, send_file
from config import custombucket, customregion
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import logging
from datetime import datetime

app = Flask(__name__)

import rds_db as db


bucket = custombucket
region = customregion


@app.route('/')
def index():
    employees = db.get_details()
    print(employees)
    
    return render_template('index.html', employees=employees)

@app.route("/about", methods=['POST'])
def about():
    return render_template('about.html')

@app.route('/insert', methods = ['post'])
def insert():
    if request.method== 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        pri_skill = request.form['pri_skill']
        location = request.form['location']
        phone = request.form['phone']
        email = request.form['email']
        image = request.files['file'] # file upload check

        if image.filename == "":
            return "Please select a file"
        
        try:
            filename = image.filename
            filename = secure_filename(filename)
            print("Inserting data to MySQL RDS.. uploading image to S3 Bucket..")
            """Upload a file to an S3 bucket

            :param file_name: File to upload
            :param bucket: Bucket to upload to
            :param object_name: S3 object name. If not specified then file_name is used
            :return: True if file was uploaded, else False
            """

            # If S3 object_name was not specified, use file_name
            #if object_name is None:
            object_name = os.path.basename(filename)

            # Upload the file
            s3_client = boto3.client('s3')
            try:
                response = s3_client.upload_file(filename,bucket, object_name)
                print(response)
            except ClientError as e:
                logging.error(e)
                return False


            db.insert_details(fname, lname, pri_skill, location, phone, email, filename)

        except Exception as e:
            return str(e)
        
        employees = db.get_details()
        
        return render_template('index.html', employees = employees)
    

if __name__=="__main__":
    #app.run(host="0.0.0.0", debug=True)
    app.run(host="localhost",debug=True)
