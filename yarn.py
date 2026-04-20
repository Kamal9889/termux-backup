import csv
import os

def search_yarn():
    path = '/storage/emulated/0/Download/stock.csv'
    if not os.path.exists(path):
        print("\n[!] Error: 'stock.csv' not found in Download folder!")
        return

    # আপনি লটের যতটুকু টাইপ করবেন তা এখানে ইনপুট হিসেবে নেবে
    query = input("\nEnter Lot Number (Partial or Full): ").strip().lower()

    if not query:
        print("Please enter something to search.")
        return

    try:
        with open(path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            found_count = 0
            
            for row in reader:
                file_lot = str(row.get('LOT', '')).strip().lower()
                
                # এখানে চেক করা হচ্ছে আপনার টাইপ করা অংশটি লট নাম্বারের ভেতরে আছে কি না
                if query in file_lot:
                    found_count += 1
                    print(f"\n--- RESULT #{found_count} ---")
                    print("-" * 45)
                    print(f"1. LOT NUMBER     : {row.get('LOT')}")
                    print(f"2. BRAND NAME     : {row.get('BRAND NAME')}")
                    print(f"3. COUNT & TYPE   : {row.get('YARN COUNT')} {row.get('YARN TYPE')}")
                    print(f"4. TOTAL QTY (kg) : {row.get('TOTAL QTY. (kg)')}")
                    print(f"5. LOCATION       : {row.get('LOCATION')}")
                    print(f"6. ROW & COLUMN   : {row.get('LOCATION  ROW &COLUMN ')}")
                    print(f"7. RACK NO        : {row.get('RACK')}")
                    print(f"8. WEIGHT & CONE  : {row.get('Weight & Cone')}")
                    print(f"9. REMARKS       : {row.get('REMARKS')}")
                    print("-" * 45)
            
            if found_count > 0:
                print(f"\n[Total {found_count} matching results found.]\n")
            else:
                print(f"\n[?] No Lot found matching with '{query.upper()}'.\n")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_yarn()
