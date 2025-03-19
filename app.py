from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)

        # Check if the stock exists by verifying if `info` has meaningful data
        info = stock.info
        if not info or "shortName" not in info:
            logging.error(f"Invalid stock ticker: {symbol}")
            return {"error": f"Invalid stock ticker: {symbol}. Please check and try again."}

        # Fetch historical data (1 month)
        hist = stock.history(period="1mo")
        if hist.empty:
            logging.warning(f"No historical data found for {symbol}")
            return {"error": f"No historical data available for {symbol}."}

        # Convert Date to ISO format (YYYY-MM-DD) for consistency
        historical_data = hist.reset_index()
        historical_data['Date'] = historical_data['Date'].dt.strftime('%Y-%m-%d')
        historical_data = historical_data[['Date', 'Open', 'High', 'Low', 'Close']].to_dict(orient="records")

        # Prepare stock details
        stock_details = {
            "CompanyName": info.get("shortName", symbol),
            "Market Cap": info.get("marketCap", "N/A"),
            "Current Price": info.get("currentPrice", "N/A"),
            "High / Low": f"{info.get('dayHigh', 'N/A')} / {info.get('dayLow', 'N/A')}",
            "Stock P/E": info.get("trailingPE", "N/A"),
            "Book Value": info.get("bookValue", "N/A"),
            "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get("dividendYield") else "N/A",
            "ROE": f"{info.get('returnOnEquity', 0) * 100:.2f}%" if info.get("returnOnEquity") else "N/A",
            "Face Value": info.get("faceValue", "N/A"),
        }

        return {"details": stock_details, "historical_data": historical_data}

    except Exception as e:
        logging.error(f"Error fetching stock data for {symbol}: {str(e)}")
        return {"error": f"Unable to fetch data for {symbol}. Please try again later."}

@app.route('/api/get_stock_data', methods=['GET'])
def get_stock_data():
    company_name = request.args.get('company_name')
    if not company_name:
        return jsonify({'error': 'Company name is required'}), 400

    stock_data = fetch_stock_data(company_name)
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
