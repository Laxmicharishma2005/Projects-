from expense import Expense
from login_system import login_user, register_user, logout_user
import calendar
import datetime


def main():
    print("💼 Welcome to the Personal Expense Tracker")

    while True:
        choice = input("1. Login\n2. Register\n3. Exit\nChoose: ")
        if choice == "1":
            username = login_user()
            if username:
                run_expense_tracker(username)
                logout_user(username)
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.\n")


def run_expense_tracker(username):
    print(f"\n🎯 Running Enhanced Expense Tracker for {username}!")
    expense_file_path = f"{username}_expenses.csv"
    monthly_budget = 20000  # set your monthly budget in ₹

    expenses = get_user_expenses()
    for expense in expenses:
        save_expense_to_file(expense, expense_file_path)

    summarize_expenses(expense_file_path, monthly_budget)


def get_user_expenses():
    print(f"\n📝 Enter Your Expenses :")
    expense_categories = ["🍔 Food", "🏠 Home", "💼 Work", "🎉 Fun", "✨ Misc"]
    expenses = []

    while True:
        expense_name = input("Enter expense name : ").strip()
        if expense_name.lower() == 'done':
            break

        try:
            expense_amount = float(input("Enter expense amount : "))
            expense_day = int(input("Enter day of the month (1-31): "))
        except ValueError:
            print("❌ Invalid number. Try again.")
            continue

        print("Select a category:")
        for i, category in enumerate(expense_categories):
            print(f"  {i+1}. {category}")

        try:
            category_index = int(input("Enter category number [1-5]: ")) - 1
            if category_index not in range(len(expense_categories)):
                raise ValueError
        except ValueError:
            print("❌ Invalid category number. Try again.")
            continue

        category = expense_categories[category_index]
        expense = Expense(expense_name, category, expense_amount, expense_day)
        expenses.append(expense)

    return expenses


def save_expense_to_file(expense: Expense, filepath):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.day}\n")


def summarize_expenses(filepath, monthly_budget):
    print("\n📊 Expense Summary")
    expenses = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            name, amount, category, day = parts
            try:
                expenses.append(Expense(name, category, float(amount), int(day)))
            except:
                continue

    if not expenses:
        print("❌ No valid expenses.")
        return

    total_by_category = {}
    total_by_item = {}
    total_by_week = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for exp in expenses:
        total_by_category[exp.category] = total_by_category.get(exp.category, 0) + exp.amount
        total_by_item[exp.name] = total_by_item.get(exp.name, 0) + exp.amount
        week = (exp.day - 1) // 7 + 1
        total_by_week[week] += exp.amount

    total_spent = sum(exp.amount for exp in expenses)
    remaining_budget = monthly_budget - total_spent

    print("\n📂 Expenses by Category:")
    for k, v in total_by_category.items():
        print(f"  {k}: ₹{v:.2f}")

    print("\n🛒 Expenses by Item:")
    for k, v in total_by_item.items():
        print(f"  {k}: ₹{v:.2f}")

    print("\n📅 Weekly Spend:")
    for week in total_by_week:
        print(f"  Week {week}: ₹{total_by_week[week]:.2f}")

    print(f"\n💸 Total Spent: ₹{total_spent:.2f}")
    print(f"✅ Remaining Budget: ₹{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        per_day_budget = remaining_budget / remaining_days
        print(green(f"📈 Daily Budget Left: ₹{per_day_budget:.2f}"))
    else:
        print("📆 No days remaining.")

    usage_percent = total_spent / monthly_budget

    if usage_percent > 1.0:
        print(red("🚨 RED: You've overspent. Cut down expenses!"))
    elif usage_percent > 0.75:
        print(yellow("⚠️ YELLOW: Spending high. Be cautious."))
    else:
        print(green("✅ GREEN: You're on track!"))


def green(text): return f"\033[92m{text}\033[0m"
def red(text): return f"\033[91m{text}\033[0m"
def yellow(text): return f"\033[93m{text}\033[0m"


if __name__ == "__main__":
    main()
