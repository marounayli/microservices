from flask import Flask, request, jsonify

from objects import Customer, Order, Product
from app import app, db

payload = {"customerId": "marounayli",
           "customerEmail": "marounayle@gmail.com",
           "customerAddress": "Bsaba, Mtoll Street Anibal Abi Antoun Bdlg",
           "unitDimensions": "2x2",
           "unitWeight": 400,
           "itemId": "afsaa-eqwrqw-dwewww-ewewrewr",
           "quantity": 2,
           "itemDescription": "Nvidia Geforce RTX 3090",
           "pricePerUnit": 700,
           "currency": "USD",
           "available": True
           }


@app.route('/order/<id>', methods=['GET'])
def get_order(id):
    print(db.session.query(Order).all())
    order = db.session.query(Order).filter_by(id=id).first()
    if order:
        return jsonify({'orderId': order.id})
    else:
        return jsonify({'error_code': 404, 'message': "Order not found"})

@app.route('/order', methods=['POST'])
def hello_world():
    print("Received ", request.json)
    return jsonify(payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
