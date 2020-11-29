from flask import Flask, request, jsonify
from flask import json
from objects import Customer, Order, Product, Shipment
from app import app, db
from db_init import db_init

# db_init()


def process_order(customerId, productId, quantity):
    order = Order(customerId=customerId,
                  productId=productId, quantity=quantity)
    db.session.add(order)
    db.session.commit()
    return order


@app.route("/customer/<id>", methods=["GET"])
def get_customer(id):
    customer = db.session.query(Customer).filter_by(id=id).first()
    if customer:
        return (
            jsonify(
                {
                    "customerId": customer.id,
                    "name": customer.name,
                    "address": customer.address,
                    "countryCode": customer.countryCode,
                    "email": customer.email,
                }
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "Customer not found"}), 404


@app.route("/customer", methods=["POST"])
def create_customer():
    body = request.get_json()
    name = body.get("name")
    address = body.get("address")
    countryCode = body.get("countryCode")
    email = body.get("email")
    if name and address and countryCode and email:
        customer = Customer(
            name=name, address=address, countryCode=countryCode, email=email
        )
        db.session.add(customer)
        db.session.commit()
        customer = db.session.query(Customer).filter_by(id=customer.id).first()
        return (
            jsonify(
                {
                    "customerId": customer.id,
                    "name": customer.name,
                    "address": customer.address,
                    "countryCode": customer.countryCode,
                    "email": customer.email,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {"error_code": 400, "message": "Customer not created - missing field"}
            ),
            400,
        )


@app.route("/customers", methods=["GET"])
def get_all_customers():
    customers = db.session.query(Customer).all()
    if customers:
        return (
            jsonify(
                [
                    {
                        "customerId": customer.id,
                        "name": customer.name,
                        "address": customer.address,
                        "countryCode": customer.countryCode,
                        "email": customer.email,
                    }
                    for customer in customers
                ]
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "No customers found"}), 404


@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = db.session.query(Product).filter_by(id=id).first()
    if product:
        return jsonify(
            {
                "productId": product.id,
                "productDescription": product.productDescription,
                "pricePerUnit": product.pricePerUnit,
                "currency": product.currency,
                "quantity": product.quantity,
            }
        )
    else:
        return jsonify({"error_code": 404, "message": "Product not found"})


@app.route("/product", methods=["POST"])
def create_product():
    body = request.get_json()
    desc = body.get("productDescription")
    price = body.get("pricePerUnit")
    currency = body.get("currency")
    quantity = body.get("quantity")
    if desc and price and currency and quantity:
        product = Product(
            productDescription=desc,
            pricePerUnit=price,
            currency=currency,
            quantity=quantity,
        )
        db.session.add(product)
        db.session.commit()
        product = db.session.query(Product).filter_by(id=product.id).first()
        return (
            jsonify(
                {
                    "message": "Product created succesfully",
                    "productId": product.id,
                    "productDescription": product.productDescription,
                    "pricePerUnit": product.pricePerUnit,
                    "currency": product.currency,
                    "quantity": product.quantity,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {"error_code": 400, "message": "Product not created - missing field"}
            ),
            400,
        )


@app.route("/products", methods=["GET"])
def get_all_products():
    products = db.session.query(Product).all()
    if products:
        return (
            jsonify(
                [
                    {
                        "productId": product.id,
                        "productDescription": product.productDescription,
                        "pricePerUnit": product.pricePerUnit,
                        "currency": product.currency,
                        "quantity": product.quantity,
                    }
                    for product in products
                ]
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "No products found"}), 404


@app.route("/orders", methods=["GET"])
def get_all_orders():
    orders = db.session.query(Order).all()
    orders_list = []
    if orders:
        for order in orders:
            customer = (
                db.session.query(Customer).filter_by(
                    id=order.customerId).first()
            )
            product = db.session.query(Product).filter_by(
                id=order.productId).first()
            orders_list.append(
                {
                    "orderId": order.id,
                    "customerId": customer.id,
                    "customerName": customer.name,
                    "customerEmail": customer.email,
                    "customerAddress": customer.address,
                    "productId": product.id,
                    "itemDescription": product.productDescription,
                    "quantity": order.quantity,
                    "pricePerUnit": product.pricePerUnit,
                    "currency": product.currency,
                }
            )
        return jsonify(orders_list), 200
    else:
        return jsonify({"error_code": 404, "message": "No orders found"}), 404


@app.route("/order/<id>", methods=["GET"])
def get_order(id):
    order = db.session.query(Order).filter_by(id=id).first()
    if order:
        customer = db.session.query(Customer).filter_by(
            id=order.customerId).first()
        product = db.session.query(Product).filter_by(
            id=order.productId).first()
        return (
            jsonify(
                {
                    "customerId": customer.id,
                    "customerName": customer.name,
                    "customerEmail": customer.email,
                    "customerAddress": customer.address,
                    "productId": product.id,
                    "itemDescription": product.productDescription,
                    "quantity": order.quantity,
                    "pricePerUnit": product.pricePerUnit,
                    "currency": product.currency,
                }
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "Order not found"}), 404


@app.route("/order", methods=["POST"])
def post_order():
    body = request.get_json()
    customerId = body.get("customerId")
    productId = body.get("productId")
    quantity = body.get("quantity")

    customer = db.session.query(Customer).filter_by(id=customerId).first()
    product = db.session.query(Product).filter_by(id=productId).first()

    if customerId and productId and quantity:
        if customer:
            if product:
                available = False
                if product.quantity >= quantity:
                    available = True
                    product.quantity = (
                        Product.quantity - quantity
                    )
                    db.session.commit()
                    order = process_order(customerId, productId, quantity)
                return (
                    jsonify(
                        {
                            "customerId": customerId,
                            "customerName": customer.name,
                            "customerEmail": customer.email,
                            "customerAddress": customer.address,
                            "productId": productId,
                            "productDescription": product.productDescription,
                            "quantity": quantity,
                            "pricePerUnit": product.pricePerUnit,
                            "currency": product.currency,
                            "available": available,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error_code": 404, "message": "Product not found"}), 404
        else:
            return jsonify({"error_code": 404, "message": "Customer not found"}), 404
    else:
        return (
            jsonify(
                {"error_code": 400, "message": "Order not created - missing fields"}
            ),
            400,
        )


@app.route("/shipment", methods=["GET"])
def get_all_shipments():
    shipments = db.session.query(Shipment).all()
    if shipments:
        return (
            jsonify(
                [
                    {
                        "orderId": shipment.id,
                        "unitWeight": shipment.unitWeight,
                        "unitDimension": shipment.unitDimension,
                        "estimatedArrival": shipment.estimatedArrival,
                        "initiatedTime": shipment.initiatedTime,
                        "initiated": shipment.initiated,
                    }
                    for shipment in shipments
                ]
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "No shipments found"}), 404


@app.route("/restore-stock", methods=["POST"])
def restore_stock():
    body = request.get_json()
    orderId = body.get("orderId")
    if orderId:
        order = db.session.query(Order).filter_by(id=orderId).first()
        if order:
            product = db.session.query(Product).filter_by(
                id=order.productId).first()
            product.quantity += order.quantity
            db.session.add(product)
            db.session.commit()
            return jsonify({
                "orderId": orderId,
                "productId": product.id,
                "quantity": product.quantity,
                "description": product.productDescription
            }), 200
        else:
            return jsonify({"message": "Stock not restored; Order not found"}), 400
    else:
        return jsonify({"message": "Stock not restored; Missing request parameter : orderId"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
