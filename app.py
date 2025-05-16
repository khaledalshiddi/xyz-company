from flask import Flask
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Import and register routes
from routes.crud_routes import crud_blueprint
from routes.query_routes import query_blueprint

app.register_blueprint(crud_blueprint, url_prefix="/api/crud")
app.register_blueprint(query_blueprint, url_prefix="/api/query")

# Home route (optional)
@app.route('/')
def hello_world():
    return 'XYZ Company API is running!'

if __name__ == '__main__':
    app.run(debug=True)
