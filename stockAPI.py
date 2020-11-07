from flask import Flask, request, jsonify
app = Flask(__name__)

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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print("Received ", request.json)
    return jsonify(payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
