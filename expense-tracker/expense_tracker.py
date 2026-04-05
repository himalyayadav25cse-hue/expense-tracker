# ============================================
#   💰 AI Expense Tracker
#   Built by: Himalya Yadav
#   GitHub  : himalyayadav25cse-hue
# ============================================

import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Education",
    "Health",
    "Other"
]

# ── Load / Save Data ─────────────────────────

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

# ── Add Expense ──────────────────────────────

def add_expense(expenses):
    print("\n➕ ADD NEW EXPENSE")
    print("-" * 40)

    try:
        amount = float(input("  Enter amount (₹): "))
    except ValueError:
        print("  ❌ Invalid amount! Please enter a number.")
        return

    print("\n  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")

    try:
        choice = int(input("  Choose category (1-7): "))
        if choice < 1 or choice > 7:
            raise ValueError
        category = CATEGORIES[choice - 1]
    except ValueError:
        print("  ❌ Invalid choice!")
        return

    description = input("  Description (e.g. lunch, uber): ").strip()
    if not description:
        description = category

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M")
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"\n  ✅ Added: ₹{amount:.0f} for {description} ({category})")

# ── View All Expenses ────────────────────────

def view_expenses(expenses):
    if not expenses:
        print("\n  📭 No expenses recorded yet!")
        return

    print("\n📋 ALL EXPENSES")
    print("-" * 55)
    print(f"  {'Date':<12} {'Category':<15} {'Amount':>8}  Description")
    print("-" * 55)

    total = 0
    for e in expenses:
        print(f"  {e['date']:<12} {e['category']:<15} ₹{e['amount']:>7.0f}  {e['description']}")
        total += e['amount']

    print("-" * 55)
    print(f"  {'TOTAL':<28} ₹{total:>7.0f}")
    print("-" * 55)

# ── Summary by Category ──────────────────────

def view_summary(expenses):
    if not expenses:
        print("\n  📭 No expenses recorded yet!")
        return

    print("\n📊 SPENDING SUMMARY BY CATEGORY")
    print("-" * 40)

    category_totals = {}
    total = 0

    for e in expenses:
        cat = e['category']
        category_totals[cat] = category_totals.get(cat, 0) + e['amount']
        total += e['amount']

    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    for cat, amount in sorted_cats:
        percent = (amount / total) * 100
        bar = "█" * int(percent / 5)
        print(f"  {cat:<15} ₹{amount:>7.0f}  {bar} {percent:.1f}%")

    print("-" * 40)
    print(f"  {'TOTAL':<15} ₹{total:>7.0f}")

# ── AI Tips ─────────────────────────────────

def get_ai_tips(expenses):
    if not expenses:
        print("\n  📭 Add some expenses first to get AI tips!")
        return

    print("\n🤖 AI SMART TIPS FOR YOU")
    print("-" * 45)

    category_totals = {}
    total = 0

    for e in expenses:
        cat = e['category']
        category_totals[cat] = category_totals.get(cat, 0) + e['amount']
        total += e['amount']

    tips = []

    # ── Rule-based AI Tips ───────────────────
    food = category_totals.get("Food", 0)
    transport = category_totals.get("Transport", 0)
    shopping = category_totals.get("Shopping", 0)
    entertainment = category_totals.get("Entertainment", 0)
    education = category_totals.get("Education", 0)
    health = category_totals.get("Health", 0)

    # Food tip
    if food > 0:
        food_pct = (food / total) * 100
        if food_pct > 40:
            tips.append("🍔 You are spending too much on Food ({:.0f}% of total)! Try cooking at home to save ₹{:.0f}/month.".format(food_pct, food * 0.3))
        elif food_pct > 25:
            tips.append("🍱 Food spending is moderate. Try meal prepping to cut costs by 20%.")
        else:
            tips.append("✅ Great job keeping Food expenses low!")

    # Transport tip
    if transport > 0:
        transport_pct = (transport / total) * 100
        if transport_pct > 25:
            tips.append("🚗 Transport is costing you a lot ({:.0f}%). Try carpooling or public transport to save ₹{:.0f}.".format(transport_pct, transport * 0.4))
        else:
            tips.append("✅ Your transport spending looks reasonable!")

    # Shopping tip
    if shopping > 0:
        shopping_pct = (shopping / total) * 100
        if shopping_pct > 30:
            tips.append("🛍️ Shopping is {:.0f}% of your spending! Wait 24 hours before any purchase over ₹500.".format(shopping_pct))
        else:
            tips.append("🛒 Shopping is under control. Keep it up!")

    # Entertainment tip
    if entertainment > 0:
        ent_pct = (entertainment / total) * 100
        if ent_pct > 20:
            tips.append("🎮 Entertainment is {:.0f}% of total. Set a monthly limit of ₹{:.0f}.".format(ent_pct, total * 0.1))
        else:
            tips.append("✅ Entertainment spending is balanced. Enjoy!")

    # Education tip
    if education > 0:
        tips.append("📚 Investing in Education is always smart! Keep learning and growing.")

    # Health tip
    if health > 0:
        tips.append("💊 You spent on Health. Remember — prevention is cheaper than cure. Exercise daily!")

    # General saving tip
    savings_goal = total * 0.2
    tips.append("💡 Try to save at least 20% of your income. Based on your spending, aim to save ₹{:.0f} this month.".format(savings_goal))

    # Biggest spender tip
    if category_totals:
        top_cat = max(category_totals, key=category_totals.get)
        top_amount = category_totals[top_cat]
        tips.append("📌 Your biggest expense is {} (₹{:.0f}). Focus on reducing this first!".format(top_cat, top_amount))

    # Print all tips
    for i, tip in enumerate(tips, 1):
        print(f"\n  Tip {i}: {tip}")

    print("\n" + "-" * 45)
    print("  🤖 Keep tracking your expenses every day!")
    print("     Small savings = Big results over time! 💪")

# ── Delete All Data ──────────────────────────

def clear_data():
    confirm = input("\n  ⚠️  Are you sure you want to delete ALL expenses? (yes/no): ")
    if confirm.lower() == "yes":
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        print("  ✅ All data cleared!")
    else:
        print("  ❌ Cancelled.")

# ── Main Menu ────────────────────────────────

def main():
    print("\n" + "="*50)
    print("   💰 AI EXPENSE TRACKER")
    print("   Built by Himalya Yadav 🤖")
    print("="*50)

    while True:
        expenses = load_expenses()

        print(f"\n  Total expenses recorded: {len(expenses)}")
        print("\n  What do you want to do?")
        print("  1. ➕ Add new expense")
        print("  2. 📋 View all expenses")
        print("  3. 📊 View spending summary")
        print("  4. 🤖 Get AI smart tips")
        print("  5. 🗑️  Clear all data")
        print("  6. 🚪 Exit")

        choice = input("\n  Enter choice (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_summary(expenses)
        elif choice == "4":
            get_ai_tips(expenses)
        elif choice == "5":
            clear_data()
        elif choice == "6":
            print("\n  👋 Goodbye! Keep saving money! 💰")
            print("  Built by Himalya Yadav 🤖\n")
            break
        else:
            print("\n  ❌ Invalid choice! Enter 1-6.")

if __name__ == "__main__":
    main()
