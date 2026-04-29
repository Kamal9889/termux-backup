import csv
import os
import sys

# টার্মিনালে ইউনিকোড সাপোর্ট নিশ্চিত করার জন্য
sys.stdout.reconfigure(encoding='utf-8')

def search_yarn_updated_view():
    file_path = '/sdcard/Download/YD.csv'

    if not os.path.exists(file_path):
        print(f"\nভুল: {file_path} ফাইলটি পাওয়া যায়নি!")
        return

    print("\n" + "═"*73)
    print("        YARN SEARCH REPORT (COLOR OPTIMIZED)")
    print("═"*73)
    
    search_query = input("Enter Store Ref or Batch No: ").strip().lower()

    if not search_query:
        print("অনুগ্রহ করে কিছু লিখে সার্চ করুন।")
        return

    found = False
    t_order, t_rcv, t_ready = 0.0, 0.0, 0.0

    try:
        with open(file_path, mode='r', encoding='utf-8-sig', errors='replace') as file:
            reader = list(csv.DictReader(file))

            # কালারের জন্য ২৫ ঘর বরাদ্দ করা হয়েছে (─*27)
            top    = f"┌{'─'*11}┬{'─'*7}┬{'─'*27}┬{'─'*9}┬{'─'*9}┬{'─'*9}┬{'─'*9}┐"
            header = f"│ {'S.Ref':<9} │ {'Batch':<5} │ {'Color':<25} │ {'O.Qty':<7} │ {'Rcv':<7} │ {'Ready':<7} │ {'Party':<7} │"
            mid    = f"├{'─'*11}┼{'─'*7}┼{'─'*27}┼{'─'*9}┼{'─'*9}┼{'─'*9}┼{'─'*9}┤"
            bottom = f"└{'─'*11}┴{'─'*7}┴{'─'*27}┴{'─'*9}┴{'─'*9}┴{'─'*9}┴{'─'*9}┘"

            print(top)
            print(header)
            print(mid)

            for row in reader:
                batch = str(row.get('Batch No', '') or '').strip()
                store_ref = str(row.get('STORE REF/FB', '') or '').strip()

                if search_query in batch.lower() or search_query in store_ref.lower():
                    found = True
                    
                    s_ref = store_ref[:9]
                    b_no  = batch[:5]
                    clr   = str(row.get('COLOUR', ''))[:25] # এখন ২৫ অক্ষর দেখাবে
                    pty   = str(row.get('party', ''))[:7]
                    
                    try:
                        o_qty = float(row.get('Order Qty Finish (KG)', 0) or 0)
                        rcv   = float(row.get('Store Rcv:Fin:Kgs', 0) or 0)
                        ready = float(row.get('Store Ready Balance kg', 0) or 0)
                    except:
                        o_qty = rcv = ready = 0.0

                    t_order += o_qty
                    t_rcv += rcv
                    t_ready += ready

                    print(f"│ {s_ref:<9} │ {b_no:<5} │ {clr:<25} │ {o_qty:<7.2f} │ {rcv:<7.2f} │ {ready:<7.2f} │ {pty:<7} │")
                    print(mid)

            if found:
                # গ্র্যান্ড টোটাল সেকশন (২৫ ক্যারেক্টার কালারের সাথে মিলিয়ে স্পেস অ্যাডজাস্ট করা হয়েছে)
                print(f"│ {'TOTAL':<45} │ {t_order:<7.2f} │ {t_rcv:<7.2f} │ {t_ready:<7.2f} │ {'':<7} │")
                print(bottom)
            else:
                print("│" + " No Matching Data Found ".center(len(mid)-2) + "│")
                print(bottom)

    except Exception as e:
        print(f"\nসমস্যা হয়েছে: {e}")

if __name__ == "__main__":
    search_yarn_updated_view()

