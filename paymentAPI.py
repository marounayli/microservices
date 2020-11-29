from flask import Flask, request, jsonify
from flask import json
from datetime import datetime
import random

from objects import Customer, Order, Shipment, Product, Payment, PaymentType
from app import app, db


@app.route("/payment", methods=["POST"])
def create_product():
    body = request.get_json()
    print(body)
    customerId = body.get("customerId")
    customerEmail = body.get("customerEmail")
    orderId = body.get("orderId")
    paymentType = body.get("paymentType")
    cardNumber = body.get("cardNumber")
    order = db.session.query(Order).filter_by(id=orderId).first()
    product = db.session.query(Product).filter_by(id=order.productId).first()
    if None not in [customerId, customerEmail, orderId, paymentType, cardNumber]:
        flag = True
        if checkPayment(customerId, cardNumber):
            payment = Payment(orderId=orderId, paymentType=PaymentType(
                paymentType), paymentSuccessful=True)
        else:
            payment = Payment(orderId=orderId, paymentType=PaymentType(
                paymentType), paymentSuccessful=False)
            flag = False
        db.session.add(payment)
        db.session.commit()
        payment = db.session.query(
            Product).filter_by(id=payment.id).first()
        return (
            jsonify(
                {
                    "orderId": orderId,
                    "customerId": customerId,
                    "customerEmail": customerEmail,
                    "paymentType": paymentType,
                    "cardNumber": cardNumber,
                    "productId": product.id,
                    "quantity": order.quantity,
                    "pricePerUnit": product.pricePerUnit,
                    "accepted": flag,
                    "productDescription": product.productDescription,
                    "finalPrice": order.quantity*product.pricePerUnit,
                    "currency": product.currency
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {"error_code": 400, "message": "Payment not created - missing field"}
            ),
            400,
        )


@app.route("/payments/all", methods=["GET"])
def get_customer():
    payments = db.session.query(Payment).all()
    if payments:
        return (
            jsonify(
                [
                    {
                        "paymentId": payment.id,
                        "orderId": payment.orderId,
                        "paymentType": payment.paymentType.name,
                        "paymentSuccessful": payment.paymentSuccessful
                    }
                    for payment in payments
                ]
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "Customer not found"}), 404


@app.route("/payment/by_order/<id>", methods=["GET"])
def get_shipment(id):
    payment = db.session.query(Payment).filter_by(id=id).first()
    if payment:
        return (
            jsonify(
                {
                    "id": payment.id,
                    "orderId": payment.orderId,
                    "paymentType": payment.paymentType.name,
                    "paymentSuccessful": payment.paymentSuccessful
                }
            ),
            200,
        )
    else:
        return jsonify({"error_code": 404, "message": "Shipment not found"}), 404


def checkPayment(customerId, CardNumber):
    return random.random() > 0.5


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
