from flask import Flask, request, jsonify
from flask import json
from datetime import datetime

from objects import Customer, Order, Shipment
from app import app, db

response = {
    "customerId": "marounayli",
    "customerEmail": "marounayle@gmail.com",
    "customerAddress": "Bsaba, Mtoll Street Anibal Abi Antoun Bdlg",
    "unitDimensions": "2x2",
    "unitWeight": 400,
    "itemId": "afsaa-eqwrqw-dwewww-ewewrewr",
    "quantity": 2,
    "itemDescription": "Nvidia Geforce RTX 3090",
    "initiated": True,
    "estimatedTimeOfArrival": "15-08-2020",
}


@app.route("/shipment", methods=["POST"])
def create_shipment():
    body = request.get_json()
    order_id = body.get("orderId")
    unitWeight = body.get("unitWeight")
    unitDimension = body.get("unitDimention")

    if order_id and unitWeight and unitDimension:
        order = db.session.query(Order).filter_by(id=order_id).first()
        print(order)
        shipment = Shipment(
            order_id=order_id,
            unitWeight=unitWeight,
            unitDimension=unitDimension,
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
                    "unitWeight": shipment.unitWeight,
                    "unitDimension": shipment.unitDimension,
                    "estimatedArrival": shipment.estimatedArrival,
                    "initiatedTime": shipment.initiatedTime,
                    "initiated": shipment.initiated,
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
