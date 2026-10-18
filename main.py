import sqlite3
from datetime import date, datetime

DATABASE = "expenses.db"

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Other"
]


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                description TEXT
            )
        """)


def add_expense():
    try:
        amount = float(input("Enter amount: Rs. "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        print("\nCategories:")
        for i, category in enumerate(CATEGORIES, 1):
            print(f"{i}. {category}")

        choice = int(input("Choose category number: "))

        if choice < 1 or choice > len(CATEGORIES):
            print("Invalid category.")
            return

        category = CATEGORIES[choice - 1]

        expense_date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if not expense_date:
            expense_date = date.today().isoformat()
        else:
            datetime.strptime(expense_date, "%Y-%m-%d")

        description = input("Enter description: ").strip()

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO expenses
                (amount, category, expense_date, description)
                VALUES (?, ?, ?, ?)
                """,
                (amount, category, expense_date, description)
            )

        print("Expense added successfully!")

    except ValueError:
        print("Invalid input. Please try again.")


def view_expenses():
    with get_connection() as connection:
        expenses = connection.execute(
            "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- ALL EXPENSES ---")

    for expense in expenses:
        print(
            f"ID: {expense['id']} | "
            f"Amount: Rs. {expense['amount']:.2f} | "
            f"Category: {expense['category']} | "
            f"Date: {expense['expense_date']} | "
            f"Description: {expense['description'] or '-'}"
        )


def show_total():
    with get_connection() as connection:
        result = connection.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses"
        ).fetchone()

    print(f"\nTotal expenses: Rs. {result['total']:.2f}")


def filter_by_category():
    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"{i}. {category}")

    try:
        choice = int(input("Choose category number: "))

        if choice < 1 or choice > len(CATEGORIES):
            print("Invalid category.")
            return

        category = CATEGORIES[choice - 1]

        with get_connection() as connection:
            expenses = connection.execute(
                """
                SELECT * FROM expenses
                WHERE category = ?
                ORDER BY expense_date DESC
                """,
                (category,)
            ).fetchall()

        if not expenses:
            print("No expenses found in this category.")
            return

        total = 0

        for expense in expenses:
            total += expense["amount"]
            print(
                f"ID: {expense['id']} | "
                f"Rs. {expense['amount']:.2f} | "
                f"{expense['expense_date']} | "
                f"{expense['description'] or '-'}"
            )

        print(f"Category total: Rs. {total:.2f}")

    except ValueError:
        print("Please enter a valid number.")


def delete_expense():
    try:
        expense_id = int(input("Enter expense ID to delete: "))

        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM expenses WHERE id = ?",
                (expense_id,)
            )

        if cursor.rowcount > 0:
            print("Expense deleted successfully!")
        else:
            print("Expense ID not found.")

    except ValueError:
        print("Please enter a valid ID.")


def main():
    create_table()

    while True:
        print("\n====== EXPENSE TRACKER ======")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Total Expenses")
        print("4. Filter by Category")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Select 1 to 6.")


if __name__ == "__main__":
    main()
