import os
import smtplib
import uuid
import json
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_pymongo import PyMongo
from datetime import datetime
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
MERCHANT_KEY = os.getenv('MERCHANT_KEY')
SALT = os.getenv('SALT')
ENV = os.getenv('ENV')
registration_records = mongo.db.registration_records
payment_records = mongo.db.payment_records


@app.route('/api/register', methods=["POST"])
def handleRegistrations():
    data = request.get_json()

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
    try:
        _id = registration_records.insert_one(data).inserted_id
        SENDER_EMAIL = os.getenv("SENDER_EMAIL")
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
            server.login(SENDER_EMAIL, os.getenv("EMAIL_SECRET_KEY"))

            server.sendmail(SENDER_EMAIL, RECIEVER_EMAIL, message.as_string())
    except Exception as e:
        return jsonify({
            "Error": f"A new record with the given data could not be created. The following exception occured\n{e}"
        }), 500

    response = make_response(jsonify({
        "message": f"New user registered successfully.",
        "MUNARCHY_ID": f"{data["MUNARCHY_ID"]}"
    }),201)
    return response

@app.route('/api/checkStatus', methods=['POST'])
def checkPaymentStatus():
    munarchyId = request.get_json()["munarchy_id"]
    try:
        paymentStatus = registration_records.find_one({"MUNARCHY_ID":munarchyId})["pay_status"]
        response = make_response(jsonify({
            "pay_status": paymentStatus,
        }),201)
        return response
    except TypeError as e:
        response = make_response(jsonify({
            "Error": f"Error Processing your request. {e}",
        }),400)
        return response

@app.route('/api/payments', methods=['POST'])
def easebuzzInitiatePayment():
    data = request.get_json()
    munarchyId = data["munarchy_id"]
    accomodation_status = data['accomodation_status']

    accomDict = {
        "yes": "3000.00",
        "no": "1600.00"
    }

    amount = accomDict[accomodation_status]

    user = registration_records.find_one({"MUNARCHY_ID":munarchyId})
    easebuzzObj = Easebuzz(MERCHANT_KEY,SALT,ENV)
    txnId = f'IRMUN{str(uuid.uuid4()).replace('-','')}'

    postDict = {
        'txnid': txnId,
        'firstname': user["name"],
        'phone': user["number"],
        'email': user["email_id"],
        'amount': amount,
        'productinfo': 'Munarchy Registrations',
        'surl': os.getenv("SURL"),  
        'furl': os.getenv("FURL"),
        'city': 'Roorkee',
        'zipcode': '247667',
        'address1': 'Roorkee - Haridwar Highway, Roorkee, Uttarakhand 247667',
        'state': 'Uttarakhand',
        'country': 'India'
    }

    final_response = easebuzzObj.initiatePaymentAPI(postDict)
    result = json.loads(final_response)


    if result["status"]==1:
        return result['data']
    else: 
        return make_response(jsonify({
            "Error": "Failed to process, please try again !"
        }))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
