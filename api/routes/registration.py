from quart import Blueprint, request, jsonify, make_response
from datetime import datetime
from models.registration_model import registrationModel
from marshmallow import ValidationError
from core.database import init_db
from services.email.registration_email import registrationEmail
from services.utils.generate_id import generateMunarchyId
import asyncio
from core.exceptions import UserAlreadyExistsError, EmailError

registration_bp = Blueprint('registration', __name__)
db = init_db()

@registration_bp.route('/register', methods=["POST"])
async def handle_registrations():
    try:
        data = await request.get_json()
        data = registrationModel.load(data)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    existing_user = await db.registration_records.find_one({
        "name": data['name'],
        "email_id": data['email_id']
    })

    if existing_user:
        raise UserAlreadyExistsError("User with this email already exists")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.update({
        "pay_status": False,
        "MUNARCHY_ID": generateMunarchyId(data['sex'],data['experience'],data['qualification']),
        "timeStamp": timestamp
    })

    try:
        await db.registration_records.insert_one(data)
        
        asyncio.create_task(registrationEmail(
            data["name"], 
            data["email_id"], 
            data["MUNARCHY_ID"]
        ))

        response = await make_response(jsonify({
            "message": "New user registered successfully.",
            "MUNARCHY_ID": data["MUNARCHY_ID"]
        }), 201)
        return response

    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 409
    except EmailError as e:
        print(f"Warning: {str(e)}")
        return response
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500 