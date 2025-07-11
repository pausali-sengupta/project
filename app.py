from flask import Flask
from beckn.routes import beckn_bp
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.register_blueprint(beckn_bp, url_prefix='/api')

@app.route('/')
def home():
    return "SevaSetu Flask Backend Running"

if __name__ == '__main__':
    app.run(debug=True)