import requests
from datetime import datetime

def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 150,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }

    exclude_list = [
        'usdc', 'usdt', 'busd', 'dai', 'ust', 'tusd', 'pyusd', 'fdusd',
        'usds', 'usdp', 'eusdc', 'usdd', 'frax', 'ldo', 'steth', 'wbtc', 'weth'
    ]

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # বিটকয়েন (BTC) ডেটা আলাদা করা স্ট্যাটাসের জন্য
        btc_data = next((item for item in data if item["symbol"] == "btc"), None)

        now = datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')

        # --- উপরের স্ট্যাটাস সেকশন ---
        print(f"\n{'='*60}")
        if btc_data:
            btc_price = btc_data['current_price']
            btc_change = btc_data.get('price_change_24h', 0) or 0
            btc_status = "✅ Strong Buy" if btc_data['price_change_percentage_24h'] > 2 else "⚖️ Neutral"
            print(f" STATUS: BTC ${btc_price:,.2f} | Change: {btc_change:+,.2f} | {btc_status}")
        else:
            print(" STATUS: Network Online | Fetching BTC...")
        print(f"{'='*60}")

        print(f"   🚀 TOP 100 CRYPTO REPORT (Date: {now})")
        print(f"{'-'*60}")
        print(f"{'#':<4} {'Coin':<8} {'Price':<12} {'USD Change':<12} {'Signal'}")
        print(f"{'-'*60}")

        count = 1
        for coin in data:
            if count > 100: break
            symbol = coin['symbol'].lower()
            if symbol in exclude_list: continue

            name_upper = coin['symbol'].upper()
            current_price = coin['current_price']
            usd_change = coin.get('price_change_24h', 0) or 0
            change_percent = coin.get('price_change_percentage_24h', 0) or 0

            # সিগন্যাল লজিক
            if change_percent > 7: signal = "🚀 Overbought"
            elif 2 < change_percent <= 7: signal = "✅ Strong Buy"
            elif -2 <= change_percent <= 2: signal = "⚖️ Neutral"
            elif -7 <= change_percent < -2: signal = "🛒 Discount"
            else: signal = "⚠️ Panic Sell"

            # গোল্ড এবং বিটিসি ফরম্যাটিং
            coin_display = name_upper
            if symbol == 'paxg': coin_display = "🏆 PAXG"
            if symbol == 'btc': coin_display = "⭐ BTC"

            price_str = f"${current_price:,.2f}" if current_price >= 1 else f"${current_price:.4f}"
            change_str = f"{'+' if usd_change > 0 else ''}${abs(usd_change):,.2f}"
            if current_price < 1:
                change_str = f"{'+' if usd_change > 0 else ''}${abs(usd_change):.4f}"

            print(f"{count:<4} {coin_display:<8} {price_str:<12} {change_str:<12} {signal}")
            count += 1

    except Exception as e:
        print(f"\n{'='*60}")
        print(" STATUS: Network Offline (Check Connection)")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    get_crypto_data()





