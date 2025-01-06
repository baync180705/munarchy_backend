from quart import Blueprint, request, jsonify, make_response
from datetime import datetime
from core.database import init_db
from services.email.allotment_email import allotmentEmail
import asyncio

allotment_bp = Blueprint('allotment', __name__)
db = init_db()

@allotment_bp.route('/allotment', methods=['POST'])
async def portfolio_allotments():
    #expects the following keys: MUNARCHY_ID, committee, portfolio
    data = await request.get_json()
    existing_user = await db.allotment_records.find_one({
        "MUNARCHY_ID": data['MUNARCHY_ID']
    })

    if existing_user:
        return jsonify({
            "message": "Allotment for the given participant has already been done"
        }), 400
    
    existing_user = await db.registration_records.find_one({
        "MUNARCHY_ID": data['MUNARCHY_ID']
    })

    if not existing_user:
        return jsonify({
            "message": "No such participant exists"
        }), 400

    data.update({
        "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": existing_user["name"],
        "email_id": existing_user["email_id"],
    })
    
    try:
        await db.allotment_records.insert_one(data)
        asyncio.create_task(allotmentEmail(
            data['name'],
            data['email_id'],
            data['committee'],
            data['portfolio']
        ))
        return await make_response(jsonify({"Message":"Allotments completed successfully"}),201)
    except Exception as e:
        return await make_response(jsonify({"Error":f"Error in processing allotments.\n{e}"}),400) 