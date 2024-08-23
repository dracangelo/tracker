import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import os

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")
        self.master.geometry("900x700")

        # Initialize data
        self.data_file = 'expenses.csv'
        self.expenses_df = self.load_expenses()

        # Create tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Data Entry Tab
        self.data_entry_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_entry_frame, text="Data Entry")
        self.setup_data_entry()

        # Dashboard Tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.setup_dashboard()

    def load_expenses(self):
        if os.path.exists(self.data_file):
            try:
                df = pd.read_csv(self.data_file, parse_dates=['Date'])
                # Ensure the DataFrame has the correct columns
                if set(df.columns) != set(['Date', 'Amount', 'Category']):
                    raise ValueError("CSV file has incorrect columns")
                return df
            except (pd.errors.ParserError, ValueError) as e:
                messagebox.showwarning("File Error", f"Error reading {self.data_file}. Starting with empty data. Error: {str(e)}")
                # If there's an error, rename the problematic file
                os.rename(self.data_file, f"{self.data_file}.bak")
                messagebox.showinfo("Backup Created", f"The problematic file has been renamed to {self.data_file}.bak")
        
        # If file doesn't exist or there was an error, return an empty DataFrame
        return pd.DataFrame(columns=['Date', 'Amount', 'Category'])
    def setup_data_entry(self):
        # Date Entry
        ttk.Label(self.data_entry_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = ttk.Entry(self.data_entry_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Amount Entry
        ttk.Label(self.data_entry_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = ttk.Entry(self.data_entry_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category Entry
        ttk.Label(self.data_entry_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = ttk.Combobox(self.data_entry_frame, values=["Food", "Transport", "Utilities", "Entertainment", "Other"])
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = ttk.Button(self.data_entry_frame, text="Submit", command=self.submit_expense)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Expense List
        self.expense_tree = ttk.Treeview(self.data_entry_frame, columns=('Date', 'Amount', 'Category'), show='headings')
        self.expense_tree.heading('Date', text='Date')
        self.expense_tree.heading('Amount', text='Amount')
        self.expense_tree.heading('Category', text='Category')
        self.expense_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Scrollbar for Expense List
        scrollbar = ttk.Scrollbar(self.data_entry_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        scrollbar.grid(row=4, column=2, sticky='ns')
        self.expense_tree.configure(yscroll=scrollbar.set)

        # Configure grid weights
        self.data_entry_frame.grid_columnconfigure(1, weight=1)
        self.data_entry_frame.grid_rowconfigure(4, weight=1)

        self.update_expense_list()

    def setup_dashboard(self):
        # Filters
        filter_frame = ttk.LabelFrame(self.dashboard_frame, text="Filters")
        filter_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(filter_frame, text="Date Range:").grid(row=0, column=0, padx=5, pady=5)
        self.date_range = ttk.Combobox(filter_frame, values=["Last 30 days", "Last 3 months", "Last 6 months", "Last year", "All time"])
        self.date_range.grid(row=0, column=1, padx=5, pady=5)
        self.date_range.set("Last 30 days")

        ttk.Label(filter_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_filter = ttk.Combobox(filter_frame, values=["All"] + ["Food", "Transport", "Utilities", "Entertainment", "Other"])
        self.category_filter.grid(row=0, column=3, padx=5, pady=5)
        self.category_filter.set("All")

        apply_filter_button = ttk.Button(filter_frame, text="Apply Filters", command=self.update_dashboard)
        apply_filter_button.grid(row=0, column=4, padx=5, pady=5)

        # Graphs
        self.graphs_frame = ttk.Frame(self.dashboard_frame)
        self.graphs_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_dashboard()

    def submit_expense(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        try:
            amount = float(amount)
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or amount format")
            return

        new_expense = pd.DataFrame({'Date': [date], 'Amount': [amount], 'Category': [category]})
        self.expenses_df = pd.concat([self.expenses_df, new_expense], ignore_index=True)
        self.expenses_df.to_csv(self.data_file, index=False)

        messagebox.showinfo("Success", "Expense added successfully")
        self.clear_entries()
        self.update_expense_list()
        self.update_dashboard()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.set('')

    def update_expense_list(self):
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        for _, row in self.expenses_df.iterrows():
            self.expense_tree.insert('', 'end', values=(row['Date'].strftime("%Y-%m-%d"), f"${row['Amount']:.2f}", row['Category']))

    def update_dashboard(self):
        # Apply filters
        date_range = self.date_range.get()
        category = self.category_filter.get()

        filtered_df = self.expenses_df.copy()

        if date_range != "All time":
            end_date = datetime.now()
            if date_range == "Last 30 days":
                start_date = end_date - timedelta(days=30)
            elif date_range == "Last 3 months":
                start_date = end_date - timedelta(days=90)
            elif date_range == "Last 6 months":
                start_date = end_date - timedelta(days=180)
            elif date_range == "Last year":
                start_date = end_date - timedelta(days=365)
            
            filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

        if category != "All":
            filtered_df = filtered_df[filtered_df['Category'] == category]

        # Clear previous graphs
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()

        if filtered_df.empty:
            ttk.Label(self.graphs_frame, text="No data available for the selected filters").pack()
            return

        # Create new graphs
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Pie chart for expense distribution
        expense_distribution = filtered_df.groupby('Category')['Amount'].sum()
        ax1.pie(expense_distribution, labels=expense_distribution.index, autopct='%1.1f%%')
        ax1.set_title('Expense Distribution by Category')

        # Bar chart for monthly trends
        monthly_expenses = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Amount'].sum()
        ax2.bar(monthly_expenses.index.astype(str), monthly_expenses.values)
        ax2.set_title('Monthly Expense Trends')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Total Expenses')
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Display summary statistics
        total_expenses = filtered_df['Amount'].sum()
        avg_monthly_expenses = monthly_expenses.mean() if not monthly_expenses.empty else 0
        summary_text = f"Total Expenses: ${total_expenses:.2f}\nAverage Monthly Expenses: ${avg_monthly_expenses:.2f}"
        summary_label = ttk.Label(self.graphs_frame, text=summary_text, font=('Arial', 12, 'bold'))
        summary_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()