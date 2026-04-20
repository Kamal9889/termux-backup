import csv
import os
import sys

# টার্মিনালে ইউনিকোড ক্যারেক্টার সাপোর্ট নিশ্চিত করার জন্য
sys.stdout.reconfigure(encoding='utf-8')

def search_yarn_updated_view():
    file_path = '/sdcard/Download/YD.csv'

    if not os.path.exists(file_path):
        print(f"\nভুল: {file_path} ফাইলটি পাওয়া যায়নি!")
        return

    print("\n--- Yarn Search (Fixing Unicode & Search) ---")
    search_query = input("Enter Store Ref or Batch No: ").strip().lower()

    if not search_query:
        print("অনুগ্রহ করে কিছু লিখে সার্চ করুন।")
        return

    found = False
    try:
        # utf-8-sig ব্যবহার করা হয়েছে যাতে এক্সেল ফরমেট সাপোর্ট করে
        with open(file_path, mode='r', encoding='utf-8-sig', errors='replace') as file:
            reader = csv.DictReader(file)
            
            # সলিড বর্ডারের বদলে আরও সেফ ক্যারেক্টার ব্যবহার (এরর এড়াতে)
            t = "─"
            top    = f"┌{t*15}┬{t*10}┬{t*15}┬{t*15}┬{t*9}┬{t*9}┬{t*9}┬{t*12}┬{t*12}┐"
            mid    = f"├{t*15}┼{t*10}┼{t*15}┼{t*15}┼{t*9}┼{t*9}┼{t*9}┼{t*12}┼{t*12}┤"
            bottom = f"└{t*15}┴{t*10}┴{t*15}┴{t*15}┴{t*9}┴{t*9}┴{t*9}┴{t*12}┴{t*12}┘"
            
            header = f"│ {'Store Ref':<13} │ {'Batch':<8} │ {'Color':<13} │ {'Yarn Count':<13} │ {'O.Fin':<7} │ {'R.Fin':<7} │ {'Ready':<7} │ {'Deliv.Date':<10} │ {'Party':<10} │"
            
            print("\n" + top)
            print(header)
            print(mid)

            for row in reader:
                # কলামগুলোর নাম চেক করা হচ্ছে (কেস সেনসিটিভ সমস্যা এড়াতে)
                # get() এর ভেতরে আপনার ফাইলের সঠিক নামগুলো দেওয়া হয়েছে
                batch = str(row.get('Batch No', '') or '').strip()
                store_ref = str(row.get('STORE REF/FB', '') or '').strip()
                
                # যদি সার্চ কোয়েরি ব্যাচ বা স্টোর রিফ-এ মিলে যায়
                if search_query in batch.lower() or search_query in store_ref.lower():
                    s_ref  = store_ref[:13]
                    b_no   = batch[:8]
                    clr    = str(row.get('COLOUR', '') or '')[:13]
                    y_count= str(row.get('Yarn Count', '') or '')[:13]
                    o_fin  = str(row.get('Order Qty Finish (KG)', '0') or '0')[:7]
                    r_fin  = str(row.get('Store Rcv:Fin:Kgs', '0') or '0')[:7]
                    r_bal  = str(row.get('Store Ready Balance kg', '0') or '0')[:7]
                    d_date = str(row.get('Delivery Date:', row.get('Delivery Date', 'N/A')) or 'N/A')[:10]
                    party  = str(row.get('party', '') or '')[:10]

                    # অন্তত ব্যাচ বা স্টোর রিফ থাকলে তবেই প্রিন্ট হবে
                    if b_no or s_ref:
                        print(f"│ {s_ref:<13} │ {b_no:<8} │ {clr:<13} │ {y_count:<13} │ {o_fin:<7} │ {r_fin:<7} │ {r_bal:<7} │ {d_date:<10} │ {party:<10} │")
                        print(mid)
                        found = True

            if not found:
                print("│" + " No Matching Data Found ".center(len(mid)-2) + "│")
                print(bottom)

    except Exception as e:
        print(f"\nসমস্যা হয়েছে: {e}")

if __name__ == "__main__":
    search_yarn_updated_view()
