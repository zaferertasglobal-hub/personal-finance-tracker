import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

File = 'transactions.csv'

def file_exist():
    if not os.path.exists(File):
        bos_df=pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount', 'Description'])
        bos_df.to_csv(File, index=False, encoding='utf-8')
        print("New file created:", File)

def load_transactions():
    file_exist()
    return pd.read_csv(File, encoding='utf-8')

def add_transaction():
    df = load_transactions()

    print("\n--- Add new transaction ---")
    type = input("Type (income / expense): ").lower()
    while type not in ['income', 'expense']:
        print(" Please enter 'income' or 'expense'.")
        type = input("Type (income / expense): ").lower()

    category = input("Category (e.g., salary, rent, food, entertainment): ").capitalize()
    try:
        amount = float(input("Amount (€): "))
        if amount <= 0:
            print("Amount must be greater than zero !")
            return
    except:
        print("Please enter a valid number!")
        return

    description = input("Description (optional): ")

    new_transaction = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Type': 'income' if type == 'income' else 'expense',
        'Category': category,
        'Amount': amount,
        'Description': description
    }

    df = pd.concat([df, pd.DataFrame([new_transaction])], ignore_index=True)
    df.to_csv(File, index=False, encoding='utf-8')
    print("✓ Transaction added successfully!")


def show_transactions():
    df = load_transactions()
    if df.empty:
        print("No transactions found.")
    else:
        print("\n--- All Transactions ---")
        print(df.to_string(index=False))


def monthly_summary():
    df = load_transactions()
    if df.empty:
        print("No data available for summary.")
        return


    bu_ay = datetime.now().strftime("%Y-%m")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Ay'] = df['Date'].dt.strftime("%Y-%m")

    ay_df = df[df['Ay'] == bu_ay]

    total_income = ay_df[ay_df['Type'] == 'income']['Amount'].sum()
    total_expense = ay_df[ay_df['Type'] == 'expense']['Amount'].sum()
    balance = total_income - total_expense

    print(f"\n--- {bu_ay} Ayı Özeti ---")
    print(f"Total Income:  {total_income:.2f} €")
    print(f"Total Expense:  {total_expense:.2f} €")
    print(f"Balance:        {balance:.2f} €")


    if not ay_df[ay_df['Type'] == 'expense'].empty:
        expense_category = ay_df[ay_df['Type'] == 'expense'].groupby('Category')['Amount'].sum()
        plt.figure(figsize=(8, 6))
        expense_category.plot(kind='pie', autopct='%1.1f%%', title=f'{bu_ay} Expense Distribution by Category')
        plt.ylabel('')
        plt.show()

# Ana menü
def menu():
    while True:
        print("\n" + "="*40)
        print("  Personal Finance Tracker ")
        print("="*40)
        print("1. Add new transaction")
        print("2. Show all transactions")
        print("3. Show monthly summary and chart")
        print("4. Exit")

        secim = input("\nYour choice (1-4): ")
        if secim == '1':
            add_transaction()
        elif secim == '2':
            show_transactions()
        elif secim == '3':
            monthly_summary()
        elif secim == '4':
            print("Goodbye! Don't forget to track your finances :)")
            break
        else:
            print("Invalid choice, please enter a number between 1-4.")

# Programı başlat
if __name__ == "__main__":
    menu()
