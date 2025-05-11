import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to connect to MySQL database
def connect():
    try:
        con = mysql.connector.connect(
            host='localhost',
            database='prj',
            user='root',
            password='MySQL123!'
        )
        if con.is_connected():
            print('Connected to MySQL database')
            return con
    except Error as e:
        print(e)
    return None


# Function to add a category
def add_category(con, name):
    try:
        cursor = con.cursor()
        sql = "INSERT INTO categories (name) VALUES (%s)"
        cursor.execute(sql, (name,))
        con.commit()
        messagebox.showinfo("Success", "Category added successfully!")
    except Error as e:
        messagebox.showerror("Error", f"Failed to add category: {e}")


# Function to add a transaction
def add_transaction(con, date, description, amount, category_id):
    try:
        cursor = con.cursor()
        sql = """INSERT INTO transactions	
        (date, description, amount, category_id)	
        VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (date, description, amount, category_id))
        con.commit()
        messagebox.showinfo("Success", "Transaction added successfully!")
    except Error as e:
        messagebox.showerror("Error", f"Failed to add transaction: {e}")


# Function to fetch all transactions
def get_transactions(con):
    try:
        query = """	
        SELECT t.id, t.date, t.description, t.amount, c.name as category	
        FROM transactions t	
        JOIN categories c ON t.category_id = c.id	
        """

        df = pd.read_sql(query, con)
        return df
    except Error as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return None


# Function to visualize transactions
def visualize_transactions(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly_expenses = df.groupby('month')['amount'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='month', y='amount', data=monthly_expenses)
    plt.title('Total Expenses Per Month')
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.show()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='category', y='amount', data=df)
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.show()


# GUI Setup
def setup_gui(con):
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("500x400")

    # Add Category Section
    tk.Label(root, text="Add Category").pack(pady=5)
    category_entry = tk.Entry(root, width=30)
    category_entry.pack(pady=5)

    def add_category_gui():
        category = category_entry.get()

        if category:
            add_category(con, category)
        else:
            messagebox.showwarning("Input Error", "Please enter a category name.")
    tk.Button(root, text="Add Category", command=add_category_gui).pack(pady=5)

    # Add Transaction Section
    tk.Label(root, text="Add Transaction").pack(pady=10)
    date_entry = tk.Entry(root, width=30)
    date_entry.insert(0, "YYYY-MM-DD")
    date_entry.pack(pady=5)
    description_entry = tk.Entry(root, width=30)
    description_entry.insert(0, "Description")
    description_entry.pack(pady=5)
    amount_entry = tk.Entry(root, width=30)
    amount_entry.insert(0, "Amount")
    amount_entry.pack(pady=5)
    category_id_entry = tk.Entry(root, width=30)
    category_id_entry.insert(0, "Category ID")
    category_id_entry.pack(pady=5)

    def add_transaction_gui():
        date = date_entry.get()
        description = description_entry.get()
        amount = amount_entry.get()
        category_id = category_id_entry.get()
        if date and description and amount and category_id:
            try:
                amount = float(amount)
                category_id = int(category_id)
                add_transaction(con, date, description, amount, category_id)
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter valid data types.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            tk.Button(root, text="Add Transaction", command=add_transaction_gui).pack(pady=5)

    # Display and Visualize Transactions
    def show_transactions():
        df = get_transactions(con)
        if df is not None:
            print(df)
            visualize_transactions(df)
        tk.Button(root, text="Show Transactions", command=show_transactions).pack(pady=10)
        # Run the GUI loop
        root.mainloop()


# Main Function
def main():
    con = connect()
    if con:
        setup_gui(con)
        con.close()


if __name__ == "__main__":
    main()
