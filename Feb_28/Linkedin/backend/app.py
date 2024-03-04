from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required.'}), 400

    try:
        # Store the URL in a variable
        fetched_url = url
        # Make the request to fetch data
        # Here you would typically use the 'requests' library
        # For the sake of simplicity, we're not making an actual request in this example
        # response = requests.get(url)
        
        # If data is fetched successfully, return success message with URL
        return jsonify({'message': 'Data fetched successfully.', 'url': fetched_url}), 200
    except Exception as e:
        # If an exception occurs during fetching data, return error message
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
