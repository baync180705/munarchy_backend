import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_pymongo import PyMongo
from datetime import datetime


app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://budhayan:Shom_2005@db-cluster.4qhq9.mongodb.net/MUNARCHY?retryWrites=true&w=majority&appName=db-cluster"
mongo = PyMongo(app)

@app.route('/api/register', methods=["POST"])
def handleRegistrations():
    data = request.get_json()

    registration_records = mongo.db.registration_records

    if registration_records.find_one({"name": data["name"]}) and registration_records.find_one({"email_id": data["email_id"]}):
        return jsonify({
            "message": "user with the given username or email already exists"
        }), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salt=f"{timestamp[11:13]}{timestamp[14:16]}{timestamp[17:19]}"
    data.update({
        "pay_status":False,
        "MUNARCHY_ID":f"{data["name"][0:4]}{data["number"][0:4]}{salt}{data["experience"]}",
        "timeStamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    print(data)
    try:
        _id = registration_records.insert_one(data).inserted_id

        print("Successfully inserted to mongodb")

        SENDER_EMAIL = "budhayanc2005@gmail.com"
        RECIEVER_EMAIL = data["email_id"]
        subject = "Your MUNARCHY ID has been successfully generated"
        body = f"Dear {data["name"]}, your MUNARCHY ID is {data["MUNARCHY_ID"]}. Happy munning !"

        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECIEVER_EMAIL
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))


        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, "syoqgmwiaokuihvc")

            server.sendmail(SENDER_EMAIL, RECIEVER_EMAIL, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        return jsonify({
            "Error": f"A new record with the given data could not be created. The following exception occured\n{e}"
        }), 500

    response = make_response(jsonify({
        "message": f"New user registered successfully.",
        "MUNARCHY_ID": f"{data["MUNARCHY_ID"]}"
    }),201)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
