from quart import Blueprint, request, jsonify, make_response, redirect
import json
from datetime import datetime
from core.database import init_db
from config.settings import Settings
from services.email.payment_email import paymentEmail
from services.payment.easebuzz.easebuzz_payment_gateway import Easebuzz
from services.utils.generate_id import generateTxnId
import asyncio
from core.exceptions import UserNotFoundError, PaymentError

payment_bp = Blueprint('payment', __name__)
db = init_db()
settings = Settings()

@payment_bp.route('/checkStatus', methods=['POST'])
async def check_payment_status():
    data = await request.get_json()
    munarchy_id = data["munarchy_id"]
    
    try:
        user = await db.registration_records.find_one({"MUNARCHY_ID": munarchy_id})
        if not user:
            return jsonify({"Error": "User not found"}), 404
        
        return await make_response(jsonify({
            "pay_status": user.get("pay_status", False),
            "sex": user.get("sex", False)
        }), 201)
    
    except Exception as e:
        return jsonify({
            "Error": f"Error Processing your request. {e}",
        }), 400

@payment_bp.route('/payments', methods=['POST'])
async def easebuzz_initiate_payment():
    data = await request.get_json()
    munarchy_id = data["munarchy_id"]
    accomodation_status = data['accomodation_status']

    accom_dict = {
        "yes": "3195.00",
        "no": "1704.00"
    }

    amount = accom_dict[accomodation_status]

    user = await db.registration_records.find_one({"MUNARCHY_ID": munarchy_id})
    
    if not user:
        raise UserNotFoundError("User not found")

    easebuzz_obj = Easebuzz(settings.MERCHANT_KEY, settings.SALT, settings.ENV)
    txn_id = generateTxnId()

    post_dict = {
        'txnid': txn_id,
        'firstname': str(user["name"]).split(" ")[0],
        'phone': user["number"],
        'email': user["email_id"],
        'amount': amount,
        'productinfo': 'Munarchy Registrations',
        'surl': settings.SURL,  
        'furl': settings.FURL,
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

    if result["status"] != 1:
        raise PaymentError("Payment initiation failed")

    return result['data']

@payment_bp.route('/payment_success', methods=['POST'])
async def payment_success():
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
        await db.registration_records.update_one(
            {"MUNARCHY_ID": responseDict['MUNARCHY_ID']},
            {"$set": {"pay_status": True}}
        )
        await db.payment_records.insert_one(responseDict)
        asyncio.create_task(paymentEmail(
            responseDict['firstname'],
            responseDict['email'],
        ))
        return redirect(f"{settings.BASE_URL}/successful")
    except Exception as e:
        return make_response(jsonify({"Error":"Failed in updating data. Please try again"}),500)

@payment_bp.route('/payment_failure', methods=['POST'])
async def payment_failure():
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
        await db.failed_transaction.insert_one(responseDict)
        return redirect(f"{settings.BASE_URL}/unsuccessful")
    except Exception as e:
        return make_response(jsonify({"Error":"Failed in updating data. Please try again"}),500)

@payment_bp.route('/ping', methods=["GET"])
def get_status():
    return jsonify({"status": "OK"}), 200 