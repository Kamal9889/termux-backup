import csv
import os
import sys

# Ensure Unicode support for terminal
sys.stdout.reconfigure(encoding='utf-8')

def search_pro():
    file_path = '/sdcard/Download/program.csv'

    if not os.path.exists(file_path):
        print(f"\nError: {file_path} file not found!")
        return

    print("\n" + "="*55)
    print("      PRODUCTION & YARN TRACKER (pro.py)")
    print("="*55)
    print(" 1. Search by Program/Booking No")
    print(" 2. Search by Lot Number")
    print(" 3. Search by Style/Color/Party (Individual)")
    print(" 4. Party Wise Detailed Yearly Summary")
    print("-" * 55)
    
    choice = input("Select Search Option (1, 2, 3 or 4): ").strip()

    if choice == '1':
        query = input("\nEnter Program or Booking No: ").strip().lower()
        search_cols = ['Program No', 'Fabirc Booking No']
    elif choice == '2':
        query = input("\nEnter Lot Number: ").strip().lower()
        search_cols = ['Lot']
    elif choice == '3':
        query = input("\nEnter Style, Color or Party Name: ").strip().lower()
        search_cols = ['Style', 'Fabric Color', 'Party Name']
    elif choice == '4':
        query = input("\nEnter Party Name for Detailed Summary: ").strip().lower()
        search_cols = ['Party Name']
    else:
        print("Invalid Option! Please try again.")
        return

    if not query: return

    try:
        with open(file_path, mode='r', encoding='utf-8-sig', errors='replace') as file:
            reader = csv.DictReader(file)
            results = []
            
            for row in reader:
                match = False
                for col in search_cols:
                    if query in str(row.get(col, '')).lower():
                        match = True
                        break
                if match:
                    results.append(row)

            if not results:
                print("\nNo matching data found.")
                return

            # Option 4: Detailed Yearly Summary
            if choice == '4':
                total_prog = 0.0
                total_issue = 0.0
                total_knit = 0.0
                
                print(f"\n[ DETAILED YEARLY SUMMARY FOR: {results[0].get('Party Name')} ]")
                print("="*75)
                # Table Header
                print(f"{'SL':<4} | {'Booking No':<18} | {'Issue':<10} | {'Knit':<10} | {'Balance':<10}")
                print("-" * 75)
                
                for i, row in enumerate(results, 1):
                    try:
                        issue = float(row.get('Yarn Issue Qnty', 0) or 0)
                        knit  = float(row.get('Knitting Qnty', 0) or 0)
                        bal   = issue - knit
                        
                        total_issue += issue
                        total_knit  += knit
                        total_prog  += float(row.get('Program Qnty', 0) or 0)
                        
                        b_no = str(row.get('Fabirc Booking No', 'N/A'))[:18]
                        print(f"{i:<4} | {b_no:<18} | {issue:>10.2f} | {knit:>10.2f} | {bal:>10.2f}")
                    except: continue
                
                total_balance = total_issue - total_knit
                
                print("-" * 75)
                print(f"{'GRAND TOTAL':<23} | {total_issue:>10.2f} | {total_knit:>10.2f} | {total_balance:>10.2f}")
                print("="*75)
                print(f"Total Programs: {len(results)} | Total Program Qnty: {total_prog:.2f} KG")
                
            else:
                # Regular Search Display
                print(f"\nTotal {len(results)} record(s) found:")
                print("="*55)

                for i, row in enumerate(results, 1):
                    try:
                        req_qty = float(row.get('Req. Qnty', 0) or 0)
                        prog_qty = float(row.get('Program Qnty', 0) or 0)
                        issue = float(row.get('Yarn Issue Qnty', 0) or 0)
                        knit = float(row.get('Knitting Qnty', 0) or 0)
                        balance = issue - knit
                    except:
                        req_qty, prog_qty, issue, knit, balance = 0, 0, 0, 0, 0

                    print(f" SL No: {i} | [ BOOKING: {row.get('Fabirc Booking No')} ]")
                    print("-" * 50)
                    print(f"Program No    : {row.get('Program No')}")
                    print(f"Req No        : {row.get('Req. No')}")
                    print(f"Party         : {row.get('Party Name')}")
                    print(f"Lot           : {row.get('Lot')}")
                    print("-" * 50)
                    print(f"Program Qnty  : {prog_qty:>10.2f} KG")
                    print(f"Req. Qnty     : {req_qty:>10.2f} KG")
                    print(f"Yarn Issue    : {issue:>10.2f} KG")
                    print(f"Knitting Qnty : {knit:>10.2f} KG")
                    print(f"Balance Qnty  : {balance:>10.2f} KG")
                    print("=" * 55)

            print(f"\nSearch Finished.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_pro()

