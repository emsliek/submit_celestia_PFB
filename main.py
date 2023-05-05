from flask import *
import datetime
import requests
import os

app = Flask(__name__)

@app.route('/submit_pfb', methods=['POST'])
def submit_pfb():
    """ Create transaction
    """
    try:
        data = request.get_json(force=True)
        node_url = 'http://127.0.0.1:26659'

        if (
            not data['message'] or
            not data['gas_limit'] or
            not data['fee']
        ):
           raise Exception('Insufficient data')

        random_bytes = os.urandom(8)
        namespace_id = random_bytes.hex()
        data_hex = data['message'].encode('utf-8').hex()

        tx_submit = requests.post(
            node_url + '/submit_pfb',
            json={'namespace_id': namespace_id, 'data': data_hex, 'gas_limit': int(data['gas_limit']), "fee": int(data['fee'])}
        )
        tx_submit_data = tx_submit.json()

        print(tx_submit_data)

        if not tx_submit_data['txhash']: 
            raise Exception('Transaction decline')

        txhash = tx_submit_data['txhash']
        height = tx_submit_data['height']
        gas_used = tx_submit_data['gas_used']

        return jsonify({
                'txhash': txhash,
                'namespace_id': namespace_id,
                "data_hex": data,
                'gas_used': gas_used,
                'height': height,
                'code': '200',
                'date': datetime.datetime.now()
               })

    except Exception as e:
        return jsonify({'error': 500, 'message': str(e)}), 500

@app.route('/')
def index():
    """ Home page
    """
    return render_template('index.html', gas_limit=80000, fee=2000, node_url='http://127.0.0.1:26659')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
