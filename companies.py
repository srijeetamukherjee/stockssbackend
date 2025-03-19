import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Use Google Sheets CSV export link
sheet_url = "https://docs.google.com/spreadsheets/d/1VS0jGIWW7oK35dhbgQHkrCdHr1nFvSAS/export?format=csv"
df = pd.read_csv(sheet_url)  # Read CSV instead of Excel

# ✅ Convert to dictionary for quick lookup
company_mapping = dict(zip(df['Symbol'], df['Name']))  # Use 'df' instead of company_data
companies = df.to_dict(orient='records')

@app.route('/api/get_company_name', methods=['GET'])
def get_company_name():
    symbol = request.args.get('symbol')
    full_name = company_mapping.get(symbol, "Unknown Company")
    return jsonify({"full_name": full_name})

@app.route('/api/all-companies', methods=['GET'])
def get_all_companies():
    return jsonify(companies)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
