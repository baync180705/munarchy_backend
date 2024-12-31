from quart import Quart
from quart_cors import cors
from dotenv import load_dotenv
from config.settings import Settings
from core.database import init_db
from api.routes.registration import registration_bp
from api.routes.payment import payment_bp
from api.routes.allotment import allotment_bp

load_dotenv()
settings = Settings()

app = Quart(__name__)
CORS = cors(app)

db = init_db()

app.register_blueprint(registration_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(allotment_bp, url_prefix='/api')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,
        ssl_certfile=settings.SSL_CERTFILE,
        ssl_keyfile=settings.SSL_KEYFILE
    )