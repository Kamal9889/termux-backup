import csv
import os

def search_yarn():
    # সরাসরি ডাউনলোড ফোল্ডারের পাথ
    path = "/storage/emulated/0/Download/yarn.csv" 

    if not os.path.exists(path):
        print(f"\n[!] Error: '{path}' খুঁজে পাওয়া যায়নি!")
        print("টার্মাক্সে 'termux-setup-storage' কমান্ডটি দিয়ে পারমিশন চেক করুন।")
        return

    query = input("\nEnter Lot Number (Partial or Full): ").strip().lower()

    if not query:
        print("Please enter something to search.")
        return

    try:
        with open(path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            found_count = 0

            for row in reader:
                file_lot = str(row.get('LOT#', '')).strip().lower()

                if query in file_lot:
                    found_count += 1
                    print(f"\n--- RESULT #{found_count} ---")
                    print("-" * 45)
                    print(f"1. LOT NUMBER     : {row.get('LOT#')}")
                    print(f"2. BRAND NAME     : {row.get('BRAND NAME')}")
                    print(f"3. COUNT & TYPE   : {row.get('YARN COUNT')} {row.get('YARN TYPE')}")
                    print(f"4. BALANCE QTY(kg): {row.get('BALANCE QTY. (kg)')}")
                    print(f"5. LOCATION       : {row.get('LOCATION')}")
                    # লোকেশন রো এবং কলাম এখানে যোগ করা হয়েছে
                    print(f"6. ROW & COLUMN   : {row.get('LOCATION  ROW &COLUMN ')}")
                    print(f"7. RACK NO        : {row.get('RACK')}")
                    print(f"8. REMARKS        : {row.get('REMARKS')}")
                    print("-" * 45)

            if found_count > 0:
                print(f"\n[Total {found_count} matching results found.]\n")
            else:
                print(f"\n[?] No Lot found matching with '{query.upper()}'.\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_yarn()

