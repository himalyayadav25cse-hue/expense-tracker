import json, os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food","Transport","Shopping","Entertainment","Education","Health","Other"]

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f: return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE,"w") as f: json.dump(expenses,f,indent=2)

def add_expense(expenses):
    print("\n ADD NEW EXPENSE\n" + "-"*40)
    try: amount = float(input("  Enter amount (Rs): "))
    except: print("  Invalid!"); return
    print("\n  Categories:")
    for i,c in enumerate(CATEGORIES,1): print(f"    {i}. {c}")
    try:
        ch = int(input("  Choose (1-7): "))
        if ch<1 or ch>7: raise ValueError
        category = CATEGORIES[ch-1]
    except: print("  Invalid!"); return
    desc = input("  Description: ").strip() or category
    expenses.append({"amount":amount,"category":category,"description":desc,"date":datetime.now().strftime("%Y-%m-%d")})
    save_expenses(expenses)
    print(f"\n  Added: Rs{amount:.0f} for {desc} ({category})")

def view_summary(expenses):
    if not expenses: print("\n  No expenses yet!"); return
    print("\n SPENDING SUMMARY\n" + "-"*40)
    totals = {}
    total = 0
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"],0) + e["amount"]
        total += e["amount"]
    for cat,amt in sorted(totals.items(),key=lambda x:-x[1]):
        pct = (amt/total)*100
        bar = "█" * int(pct/5)
        print(f"  {cat:<15} Rs{amt:>6.0f}  {bar} {pct:.1f}%")
    print(f"\n  TOTAL: Rs{total:.0f}")

def ai_tips(expenses):
    if not expenses: print("\n  Add expenses first!"); return
    print("\n AI SMART TIPS\n" + "-"*40)
    totals = {}
    total = 0
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"],0) + e["amount"]
        total += e["amount"]
    food = totals.get("Food",0)
    shopping = totals.get("Shopping",0)
    if food/total>0.4 if total else 0: print(f"\n  Tip: You spend too much on Food ({food/total*100:.0f}%)! Try cooking at home.")
    else: print("\n  Tip: Food spending looks good!")
    if shopping/total>0.3 if total else 0: print(f"  Tip: Shopping is high! Set a monthly limit.")
    else: print("  Tip: Shopping is under control!")
    print(f"  Tip: Try to save Rs{total*0.2:.0f} this month (20% of spending).")
    top = max(totals,key=totals.get)
    print(f"  Tip: Biggest expense is {top} (Rs{totals[top]:.0f}). Focus here first!")

def main():
    print("\n" + "="*45)
    print("   💰 AI EXPENSE TRACKER")
    print("   Built by Himalya Yadav")
    print("="*45)
    while True:
        expenses = load_expenses()
        print(f"\n  Expenses recorded: {len(expenses)}")
        print("\n  1. Add expense\n  2. View summary\n  3. AI tips\n  4. Exit")
        ch = input("\n  Choice (1-4): ").strip()
        if ch=="1": add_expense(expenses)
        elif ch=="2": view_summary(expenses)
        elif ch=="3": ai_tips(expenses)
        elif ch=="4": print("\n  Goodbye! Keep saving! 💰\n"); break
        else: print("  Enter 1-4 only!")

if __name__=="__main__": main()
