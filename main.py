import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")
        self.master.geometry("800x600")

        # Initialize data
        self.expenses_df = pd.DataFrame(columns=['Date', 'Amount', 'Category'])

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


    
    def setup_data_entry(self):
        # Date Entry
        ttk.Label(self.data_entry_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.data_entry_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Amount Entry
        ttk.Label(self.data_entry_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.data_entry_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category Entry
        ttk.Label(self.data_entry_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = ttk.Combobox(self.data_entry_frame, values=["Food", "Transport", "Utilities", "Entertainment", "Other"])
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = ttk.Button(self.data_entry_frame, text="Submit", command=self.submit_expense)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()