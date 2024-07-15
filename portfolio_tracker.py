import requests
import sqlite3
import pandas as pd
from tabulate import tabulate

API_KEY = input('YOUR_ALPHA_VANTAGE_API_KEY')
BASE_URL = 'https://www.alphavantage.co/query'

# Set up the database
conn = sqlite3.connect('portfolio.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS portfolio (
             symbol TEXT PRIMARY KEY,
             shares INTEGER,
             purchase_price REAL)''')
conn.commit()

def add_stock(symbol, shares, purchase_price):
    with conn:
        c.execute("INSERT OR REPLACE INTO portfolio (symbol, shares, purchase_price) VALUES (?, ?, ?)",
                  (symbol.upper(), shares, purchase_price))

def remove_stock(symbol):
    with conn:
        c.execute("DELETE FROM portfolio WHERE symbol = ?", (symbol.upper(),))

def get_stock_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    last_refreshed = data['Meta Data']['3. Last Refreshed']
    price = data['Time Series (1min)'][last_refreshed]['4. close']
    return float(price)

def track_portfolio():
    c.execute("SELECT * FROM portfolio")
    rows = c.fetchall()
    portfolio = []
    for row in rows:
        symbol, shares, purchase_price = row
        current_price = get_stock_price(symbol)
        current_value = shares * current_price
        purchase_value = shares * purchase_price
        change = (current_value - purchase_value) / purchase_value * 100
        portfolio.append([symbol, shares, purchase_price, current_price, current_value, change])
    
    df = pd.DataFrame(portfolio, columns=['Symbol', 'Shares', 'Purchase Price', 'Current Price', 'Current Value', 'Change (%)'])
    print(tabulate(df, headers='keys', tablefmt='pretty'))

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ")
            shares = int(input("Enter number of shares: "))
            purchase_price = float(input("Enter purchase price: "))
            add_stock(symbol, shares, purchase_price)
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ")
            remove_stock(symbol)
        elif choice == '3':
            track_portfolio()
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
