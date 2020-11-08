from flask import Flask, request, jsonify

from objects import Customer, Order, Product
from app import app, db
from db_init import db_init

db_init()

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


def process_order(customer_id, product_id, quantity):
    order = Order(customer_id=customer_id, product_id=product_id,
                    quantity=quantity)
    db.session.add(order)
    db.session.commit()


@app.route('/order/<id>', methods=['GET'])
def get_order(id):
    print(db.session.query(Order).all())
    order = db.session.query(Order).filter_by(id=id).first()
    if order:
        return jsonify({'orderId': order.id})
    else:
        return jsonify({'error_code': 404, 'message': "Order not found"})


@app.route('/order', methods=['POST'])
def post_order():
    body = request.get_json()
    customer_id = body['customerId']
    product_id = body['itemId']
    needed_quantity = body['quantity']

    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    product = db.session.query(Product).filter_by(id=product_id).first()

    if customer:
        if product:
            available = False
            if product.quantityAvailable >= needed_quantity:
                available = True
                product.quantityAvailable = Product.quantityAvailable - needed_quantity
                db.session.commit()
                process_order(customer_id, product_id, needed_quantity)
            return jsonify({"customerId":customer_id, 
                            "customerName": customer.name,
                            "customerEmail": customer.email, 
                            "customerAddress":customer.address,
                            "itemId": product_id,
                            "itemDescription": product.productDescription,
                            "quantity": needed_quantity,
                            "pricePerUnit": product.pricePerUnit,
                            "currency": product.currency,
                            "available": available})         
        else:
            return jsonify({'error_code': 404, 'message': "Product not found"})
    else:
        return jsonify({'error_code': 404, 'message': "Customer not found"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
