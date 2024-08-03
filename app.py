from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['chatbot']
qa_collection = db['qa']
products_collection = db['products']

@app.route('/api/handle_message', methods=['POST'])
def handle_message():
    try:
        user_message = request.json.get('message')
        logger.info(f"Received message: {user_message}")
        if user_message.lower() == "produk":
            products = list(products_collection.find())  # Convert cursor to list
            if len(products) > 0:
                product_list = [{"name": product['name'], "description": product['description'], "price": product['price']} for product in products]
                return jsonify({"products": product_list})
            else:
                return jsonify({"message": "Maaf, tidak ada produk yang tersedia."})
        else:
            response = qa_collection.find_one({"question": {"$regex": user_message, "$options": "i"}})
            if response:
                return jsonify({"answer": response['answer']})
            else:
                return jsonify({"message": "Maaf, saya tidak mengerti."})
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"message": "Terjadi kesalahan pada server."})

if __name__ == '__main__':
    app.run(port=5000)