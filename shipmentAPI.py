from flask import Flask, request, jsonify
from flask import json
from datetime import datetime

from objects import Customer, Order, Shipment, Product
from app import app, db


@app.route("/shipment", methods=["POST"])
def create_shipment():
    body = request.get_json()
    orderId = body.get("orderId")

    if orderId:
        order = db.session.query(Order).filter_by(id=orderId).first()
        product = db.session.query(Product).filter_by(
            id=order.productId).first()
        print(order)
        shipment = Shipment(
            orderId=orderId,
            estimatedArrival=datetime.now(),
            initiatedTime=datetime.now(),
            initiated=True,
        )
        db.session.add(shipment)
        db.session.commit()
        shipment_verification = (
            db.session.query(Shipment).filter_by(id=shipment.id).first()
        )
        return (
            jsonify(
                {
                    "orderId": shipment.id,
                    "unitWeight": product.unitWeight,
                    "estimatedArrival": shipment.estimatedArrival,
                    "initiatedTime": shipment.initiatedTime,
                    "initiated": shipment.initiated,
                    "totalWeight": product.unitWeight*order.quantity
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {"error_code": 400, "message": "Shipment not created - missing field"}
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
