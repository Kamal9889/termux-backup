import requests
from datetime import datetime

def get_crypto_data():
    # Fetching more coins to filter out stablecoins and keep top 20 high-value ones
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'price_desc', # দাম অনুযায়ী বড় থেকে ছোট সাজানো
        'per_page': 50,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }

    # বাদ দেওয়ার জন্য স্টেবলকয়েন বা কম দামি কয়েনের লিস্ট
    exclude_list = ['usdc', 'usdt', 'busd', 'dai', 'ust', 'tusd', 'pyusd']

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # বর্তমান সময় এবং তারিখ ১২ ঘণ্টা ফরম্যাটে (AM/PM)
        now = datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')
        
        print(f"\n--- Crypto Market Report ---")
        print(f"Date & Time: {now}")
        # Table Header
        print(f"{'#':<3} {'Coin':<18} {'Current':<12} {'24h Ago':<12} {'Change'}")
        print("-" * 62)

        count = 1
        for coin in data:
            if count > 20: # টপ ২০টি দেখাবে
                break
            
            symbol = coin['symbol'].lower()
            # স্টেবলকয়েন বাদ দেওয়া এবং অন্তত ১ ডলারের নিচের কয়েনগুলো ফিল্টার করা
            if symbol in exclude_list or coin['current_price'] < 1.0:
                continue

            name = coin['symbol'].upper()
            current_price = coin['current_price']
            change_pct = coin['price_change_percentage_24h']
            
            # Calculating price 24h ago
            if change_pct is not None:
                old_price = current_price / (1 + (change_pct / 100))
                change_str = f"{'+' if change_pct > 0 else ''}{change_pct:.2f}%"
                old_price_str = f"${old_price:,.2f}"
            else:
                change_str = "N/A"
                old_price_str = "N/A"

            current_price_str = f"${current_price:,.2f}"
            coin_display = f"{coin['name'][:10]} ({name})"

            print(f"{count:<3} {coin_display:<18} {current_price_str:<12} {old_price_str:<12} {change_str}")
            count += 1
            
    except Exception as e:
        print("Error: Could not fetch data. Check your connection.")

if __name__ == "__main__":
    get_crypto_data()

