import sys

def gsm_calculator():
    WHITE, GREEN, CYAN, YELLOW, BOLD, END = '\033[97m', '\033[92m', '\033[96m', '\033[93m', '\033[1m', '\033[0m'
    print(f"\n{CYAN}[ 1. COLLAR YARN CONSUMPTION BY GSM ]{END}")
    try:
        L = float(input(f"{WHITE}Enter Length (cm) : {END}"))
        W = float(input(f"{WHITE}Enter Width (cm)  : {END}"))
        G = float(input(f"{WHITE}Enter GSM         : {END}"))
        Q = int(input(f"{WHITE}Enter Quantity    : {END}"))
        
        # ক্যালকুলেশন
        single_pc_gm = (L * W * G) / 10000
        net_kg = (single_pc_gm * Q) / 1000
        total_with_5_wst = net_kg * 1.05

        # রেজাল্ট ডিসপ্লে
        print(f"\n{GREEN}{BOLD}--- CONSUMPTION REPORT ---{END}")
        print(f"─" * 40)
        print(f"{WHITE}Single Pc Weight : {YELLOW}{BOLD}{single_pc_gm:.2f} grams{END}")
        print(f"{WHITE}Net Total Weight : {GREEN}{net_kg:.3f} kg{END}")
        print(f"{WHITE}Total (+5% Wst) : {GREEN}{total_with_5_wst:.3f} kg{END}")
        print(f"─" * 40 + "\n")
        
    except ValueError: print(f"{BOLD}Invalid Input!{END}")

def time_calculator():
    WHITE, GREEN, CYAN, YELLOW, BOLD, END = '\033[97m', '\033[92m', '\033[96m', '\033[93m', '\033[1m', '\033[0m'
    print(f"\n{CYAN}[ 2. KNIT TIME CALCULATOR ]{END}")
    try:
        cpi = float(input(f"{WHITE}Enter CPI         : {END}"))
        height = float(input(f"{WHITE}Enter Collar Height: {END}"))
        final_time = (((cpi / 2.54) * height) / 2) - 4
        print(f"─" * 40)
        print(f"{GREEN}Calculation Result: {final_time:.2f} Min{END}")
        print(f"─" * 40)
    except ValueError: print(f"{BOLD}Invalid Input!{END}")

def knitting_price():
    WHITE, GREEN, CYAN, YELLOW, RED, BOLD, END = '\033[97m', '\033[92m', '\033[96m', '\033[93m', '\033[91m', '\033[1m', '\033[0m'
    print(f"\n{CYAN}[ 3. KNITTING PRICE CALCULATOR ]{END}")
    try:
        pc_time = float(input(f"{WHITE}Time per PC (Min)   : {END}"))
        daily_target_tk = float(input(f"{WHITE}Daily Target (Amount): {END}"))
        working_hours = float(input(f"{WHITE}Working Hours/Day    : {END}"))
        price_per_min = daily_target_tk / (working_hours * 60)
        single_price = price_per_min * pc_time
        print(f"\n{YELLOW}{BOLD}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{END}")
        print(f"{YELLOW}{BOLD}┃          FINAL PRICE CALCULATION          ┃{END}")
        print(f"{YELLOW}{BOLD}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{END}")
        print(f" {RED}{BOLD}>>> UNIT PRICE: {GREEN}{single_price:.2f} TK <<<{END}")
        print(f"{YELLOW}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{END}\n")
    except ValueError: print(f"{BOLD}Invalid Input!{END}")

def rate_chart():
    CYAN, YELLOW, BOLD, GREEN, WHITE, END = '\033[96m', '\033[93m', '\033[1m', '\033[92m', '\033[97m', '\033[0m'
    rates = [
        ["Solid Collar Cuff", "6", "4", "Set"], ["Tipping Collar Cuff", "8", "6", "Set"],
        ["Solid Lycra Collar Cuff", "10", "8", "Set"], ["Tipping Lycra Collar Cuff", "12", "10", "Set"],
        ["Solid Double Part Collar Cuff", "28", "20", "Set"], ["Tipping Double Part Collar Cuff", "30", "20", "Set"],
        ["Solid Birdseye Collar Cuff", "25", "14-15", "Set"], ["Tipping Birdseye Collar Cuff", "25", "14", "Set"],
        ["Solid Emboss Collar Cuff", "10", "7", "Set"], ["Tipping Emboss Collar Cuff", "12", "8", "Set"],
        ["Solid Neck", "10", "8", "Pcs"], ["Solid Lycra Neck", "12", "10", "Pcs"],
        ["Tipping Neck", "12", "8", "Pcs"], ["Tipping Lycra Neck", "14", "10", "Pcs"],
        ["Solid Double Part Neck", "18", "12", "Pcs"], ["Tipping Double Part Neck", "20", "14", "Pcs"],
        ["Pin Stripe Collar Cuff", "10", "8", "Set"], ["Tipping Collar Cuff (2 tone)", "15", "12", "Set"],
        ["Bottom 2x2", "35", "10-30", "Pcs"], ["YD Big Cuff", "3", "2", "Pcs"],
        ["Solid Big Cuff", "3", "2", "Pcs"], ["Lycra Birdseye", "30", "18", "Set"],
        ["Polyester Collar (Filament)", "10", "8", "Set"], ["Normal Racking Collar", "12", "10", "Set"],
        ["Jacquard 7 Feeder Birdseye", "30", "17", "Set"], ["Jacquard Racking Collar Cuff", "25", "15-20", "Set"],
        ["Jacquard Tipping Racking", "28", "15-20", "Set"], ["Jacquard Solid Transfer", "45", "30", "Set"],
        ["Jacquard Tipping Transfer", "48", "30", "Set"], ["Jacquard Solid Placket (KAN)", "30", "20", "Pcs"],
        ["Jacquard Solid Lycra Placket", "35", "20", "Pcs"], ["Jacquard Tipping Placket", "38", "25", "Pcs"],
        ["Jacquard Tipping Lycra Placket", "40", "25", "Pcs"]
    ]
    print(f"\n{CYAN}{BOLD}┌─────────────────────────────────────────────────────┐")
    print(f"│      FLAT KNITTING CHARGE (Rev: 24/07/2025)       │")
    print(f"└─────────────────────────────────────────────────────┘{END}")
    search = input(f"{WHITE}Search Item or Enter for all: {END}").lower()
    print(f"\n{BOLD}{'TYPE':<32} {'BUYER':<8} {'INHOUSE':<10}{END}")
    print(f"─" * 55)
    for row in rates:
        if search in row[0].lower():
            print(f"{YELLOW}{row[0]:<32}{END} {WHITE}{row[1]:<8}{END} {GREEN}{BOLD}{row[2]} Tk/{row[3]}{END}")
    print(f"─" * 55 + "\n")

def main():
    CYAN, YELLOW, BOLD, END = '\033[96m', '\033[93m', '\033[1m', '\033[0m'
    print(f"\n{CYAN}{BOLD}┌───────────────────────────────────────────┐")
    print(f"│      GARMENTS PRODUCTION TOOLKIT V8       │")
    print(f"└───────────────────────────────────────────┘{END}")
    print(f"{YELLOW}1. Collar Yarn Consumption (GSM Based)")
    print(f"2. Knit Time Calculator")
    print(f"3. Knitting Price Calculator")
    print(f"4. Flat Knitting Charge (New Rate List){END}")
    choice = input(f"\n{BOLD}Select Option (1-4): {END}")
    if choice == '1': gsm_calculator()
    elif choice == '2': time_calculator()
    elif choice == '3': knitting_price()
    elif choice == '4': rate_chart()
    else: print("Invalid Selection!")

if __name__ == "__main__":
    main()

