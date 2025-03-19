from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/stock-return', methods=['POST'])
def calculate_stock_return():
    try:
        data = request.json
        company = data['company']
        monthly_investment = float(data['monthly_investment'])
        investment_period = int(data['investment_period'])

        stock = yf.Ticker(company)

        # Get today's date and the date from 'investment_period' months ago
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=30 * investment_period)

        # Fetch historical stock data
        history = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        if history.empty:
            return jsonify({"error": "No historical data available for this company."}), 404

        # Get the earliest and latest closing prices
        initial_price = history['Close'].iloc[0]
        final_price = history['Close'].iloc[-1]

        # Calculate expected return rate
        expected_return_percentage = ((final_price - initial_price) / initial_price) * 100

        total_investment = monthly_investment * investment_period
        wealth_gained = total_investment * (expected_return_percentage / 100)
        total_return = total_investment + wealth_gained

        return jsonify({
            "company": company,
            "monthly_investment": monthly_investment,
            "investment_period": investment_period,
            "expected_return_percentage": expected_return_percentage,
            "total_investment": total_investment,
            "wealth_gained": wealth_gained,
            "total_return": total_return
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
