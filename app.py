import os
import uuid
import json
import asyncio
import uvicorn
from dotenv import load_dotenv
from models.registration_model import registrationModel
from email_services.registration_email import registrationEmail
from email_services.payment_email import paymentEmail
from email_services.allotment_email import allotmentEmail
from quart import Quart, request, jsonify, make_response, redirect
from quart_cors import cors
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow import ValidationError
from datetime import datetime
from utils.generate_id import generateTxnId, generateMunarchyId
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz 

load_dotenv()
app = Quart(__name__)
CORS = cors(app)

client = AsyncIOMotorClient(os.getenv('MONGO_URI'))
db = client.get_default_database()
registration_records = db.registration_records
payment_records = db.payment_records
allotment_records = db.allotment_records
failed_transaction = db.failed_transaction

MERCHANT_KEY = os.getenv('MERCHANT_KEY')
SALT = os.getenv('SALT')
ENV = os.getenv('ENV')
sequence_number = 0

@app.route('/api/register', methods=["POST"])
async def handle_registrations():
    try:
        data = await request.get_json()
        registrationData = registrationModel.load(data)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    existing_user = await registration_records.find_one({
        "name": data['name'],
        "email_id": data['email_id']
    })


    if existing_user:
        return jsonify({
            "message": "user with the given username or email already exists"
        }), 400
    global sequence_number
    sequence_number+=1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.update({
        "pay_status": False,
        "MUNARCHY_ID": generateMunarchyId(data['sex'],data['experience'],data['qualification']),
        "timeStamp": timestamp
    })

    try:
        result = await registration_records.insert_one(data)
        
        asyncio.create_task(registrationEmail(data["name"], data["email_id"], data["MUNARCHY_ID"]))

        response = await make_response(jsonify({
            "message": "New user registered successfully.",
            "MUNARCHY_ID": data["MUNARCHY_ID"]
        }), 201)
        return response

    except Exception as e:
        return jsonify({
            "Error": f"A new record with the given data could not be created. The following exception occurred\n{e}"
        }), 500

@app.route('/api/checkStatus', methods=['POST'])
async def check_payment_status():
    data = await request.get_json()
    munarchy_id = data["munarchy_id"]
    
    try:
        user = await registration_records.find_one({"MUNARCHY_ID": munarchy_id})
        if not user:
            return jsonify({"Error": "User not found"}), 404
        
        return await make_response(jsonify({
            "pay_status": user.get("pay_status", False),
        }), 201)
    
    except Exception as e:
        return jsonify({
            "Error": f"Error Processing your request. {e}",
        }), 400

@app.route('/api/payments', methods=['POST'])
async def easebuzz_initiate_payment():
    data = await request.get_json()
    munarchy_id = data["munarchy_id"]
    accomodation_status = data['accomodation_status']

    accom_dict = {
        "yes": "0.50",
        "no": "0.50"
    }

    amount = accom_dict[accomodation_status]

    user = await registration_records.find_one({"MUNARCHY_ID": munarchy_id})
    
    if not user:
        return jsonify({"Error": "User not found"}), 404

    easebuzz_obj = Easebuzz(MERCHANT_KEY, SALT, ENV)
    txn_id = generateTxnId()

    post_dict = {
        'txnid': txn_id,
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
        'country': 'India',
        'udf1': accomodation_status,
        'udf2': munarchy_id
    }

    final_response = easebuzz_obj.initiatePaymentAPI(post_dict)
    result = json.loads(final_response)

    if result["status"] == 1:
        return result['data']
    else: 
        return jsonify({
            "Error": "Failed to process, please try again!"
        }), 400

@app.route('/api/ping', methods=["GET"])
def get_status():
    return jsonify({"status": "OK"}), 200

@app.route('/api/payment_success', methods=['POST'])
async def paymentSuccess():
    data = str(await request.get_data())
    responseDict = {}
    dataList = data.split('&')
    for item in dataList:
        itemList = item.split('=')
        responseDict[f'{itemList[0]}'] = itemList[1]
    
    popKeys = ['udf3','udf4','udf5','udf6','udf7','udf8','udf9','udf10']
    for key in popKeys:
        responseDict.pop(key)
    responseDict.update({
        "accomodation": responseDict.pop('udf1'),
        "MUNARCHY_ID": responseDict.pop('udf2'),
        "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    responseDict['email'] = responseDict['email'].replace('%40','@')
    try:
        await registration_records.update_one({"MUNARCHY_ID":responseDict['MUNARCHY_ID']},{"$set":{"pay_status":True}})
        await payment_records.insert_one(responseDict)
        asyncio.create_task(paymentEmail(responseDict['firstname'],responseDict['email'],responseDict['net_amount_debit'],responseDict['accomodation']))
        return redirect(f"{os.getenv('BASE_URL')}/successful")
    except Exception as e:
        return make_response(jsonify({"Error":"Failed in updating data. Please try again"}),500)

@app.route('/api/payment_failture', methods=['POST'])
async def paymentFailture():
    data = str(await request.get_data())
    responseDict = {}
    dataList = data.split('&')
    for item in dataList:
        itemList = item.split('=')
        responseDict[f'{itemList[0]}'] = itemList[1]
    
    popKeys = ['udf3','udf4','udf5','udf6','udf7','udf8','udf9','udf10']
    for key in popKeys:
        responseDict.pop(key)
    responseDict.update({
        "accomodation": responseDict.pop('udf1'),
        "MUNARCHY_ID": responseDict.pop('udf2'),
        "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    responseDict['email'] = responseDict['email'].replace('%40','@')
    try:
        await failed_transaction.insert_one(responseDict)
        return redirect(f"{os.getenv('BASE_URL')}/unsuccessful")
    except Exception as e:
        return make_response(jsonify({"Error":"Failed in updating data. Please try again"}),500)


@app.route('/api/easebuzz_webhook', methods=['POST'])
async def easebuzz_webhook():
    data = await request.get_json
    if data['status'] == 'success':
        popKeys = ['udf3','udf4','udf5','udf6','udf7','udf8','udf9','udf10']
        for key in popKeys:
            data.pop(key)
        data.update({
            "accomodation": responseDict.pop('udf1'),
            "MUNARCHY_ID": responseDict.pop('udf2'),
            "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        data['email'] = responseDict['email'].replace('%40','@')
        try:
            await registration_records.update_one({"MUNARCHY_ID":data['MUNARCHY_ID']},{"$set":{"pay_status":True}})
            await payment_records.insert_one(data)
            asyncio.create_task(paymentEmail(responseDict['firstname'],responseDict['email'],responseDict['net_amount_debit'],responseDict['accomodation']))
            return make_response(jsonify({
                'Message':'Payment processed successfully'
            }),200)
        except Exception as e:
            return make_response(jsonify({"Error":"Failed in updating data. Please try again"}),500)
    return make_response(jsonify({
        'ERROR':'Your payment has failed'
    }),400)
@app.route('/api/allotment', methods=['POST'])
async def portfolioAllotments():
    #expects the following keys: MUNARCHY_ID, name, email_id, committee, portfolio
    data = await request.get_json()
    data.update({
        "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    existing_user = await allotment_records.find_one({
        "MUNARCHY_ID": data['MUNARCHY_ID']
    })

    if existing_user:
        return jsonify({
            "message": "Allotment for the given participant has already been done"
        }), 400
    
    try:
        await allotment_records.insert_one(data)
        asyncio.create_task(allotmentEmail(data['name'],data['email_id'],data['committee'],data['portfolio']))
        return make_response(jsonify({"Message":"Allotments completed successfully"}),201)
    except Exception as e:
        return make_response(jsonify({"Error":"Error in processing allotments.\n{e}"}),400)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False, ssl_certfile=os.getenv("SSL_CERTFILE"), ssl_keyfile=os.getenv("SSL_KEYFILE"))