import csv
import os

def search_yarn():
    path = "/storage/emulated/0/Download/yarn.csv"

    if not os.path.exists(path):
        print(f"\n[!] Error: '{path}' খুঁজে পাওয়া যায়নি!")
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
                    
                    # কলাম থেকে ডেটা নেওয়া
                    qty_str = row.get('BALANCE QTY. (kg)', '0').strip()
                    weight_and_cone_val = row.get('Weight & Cone', '0').strip()
                    
                    avg_weight = 0.0
                    
                    # আপনার দেওয়া উদাহরণ (50.10/18) অনুযায়ী ভাগ করার লজিক
                    if "/" in weight_and_cone_val:
                        try:
                            parts = weight_and_cone_val.split("/")
                            w_part = float(parts[0]) # স্লাশের আগের টুকু (ওজন)
                            c_part = float(parts[1]) # স্লাশের পরের টুকু (কোণ)
                            
                            if c_part > 0:
                                avg_weight = w_part / c_part
                        except:
                            avg_weight = 0.0
                    else:
                        # যদি স্লাশ না থাকে তবে আগের মতো সরাসরি ভাগ করবে
                        try:
                            q = float(qty_str) if qty_str else 0.0
                            c = float(weight_and_cone_val) if weight_and_cone_val else 0.0
                            avg_weight = q / c if c > 0 else 0.0
                        except:
                            avg_weight = 0.0

                    print(f"\n--- RESULT #{found_count} ---")
                    print("-" * 45)
                    print(f"1. LOT NUMBER      : {row.get('LOT#')}")
                    print(f"2. BRAND NAME      : {row.get('BRAND NAME')}")
                    print(f"3. COUNT & TYPE    : {row.get('YARN COUNT')} {row.get('YARN TYPE')}")
                    print(f"4. BALANCE QTY(kg) : {qty_str}")
                    print(f"5. WEIGHT & CONE   : {weight_and_cone_val}")
                    print(f"6. AVG CONE WEIGHT : {avg_weight:.3f} kg") 
                    print(f"7. LOCATION        : {row.get('LOCATION')}")
                    print(f"8. ROW & COLUMN    : {row.get('LOCATION  ROW &COLUMN ')}")
                    print(f"9. RACK NO         : {row.get('RACK')}")
                    print(f"10. REMARKS        : {row.get('REMARKS')}")
                    print("-" * 45)

            if found_count > 0:
                print(f"\n[Total {found_count} matching results found.]\n")
            else:
                print(f"\n[?] No matching result for '{query.upper()}'.\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_yarn()

