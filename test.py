import unittest
import pandas as pd
from datetime import datetime, timedelta
import os
import tkinter as tk
from main import ExpenseTrackerApp  
class TestExpenseTrackerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.app = ExpenseTrackerApp(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        # Clear existing data before each test
        self.app.expenses_df = pd.DataFrame(columns=['Date', 'Amount', 'Category'])
        if os.path.exists(self.app.data_file):
            os.remove(self.app.data_file)
        # Remove any backup files
        for file in os.listdir():
            if file.startswith(f"{self.app.data_file}.bak"):
                os.remove(file)

    def test_submit_expense(self):
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "2023-08-23")
        self.app.amount_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "50.00")
        self.app.category_entry.set("Food")
        
        self.app.submit_expense()
        
        self.assertEqual(len(self.app.expenses_df), 1)
        self.assertEqual(self.app.expenses_df.iloc[0]['Amount'], 50.00)
        self.assertEqual(self.app.expenses_df.iloc[0]['Category'], "Food")

    def test_invalid_expense_submission(self):
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "invalid_date")
        self.app.amount_entry.delete(0, tk.END)
        self.app.amount_entry.insert(0, "not_a_number")
        self.app.category_entry.set("Food")
        
        with self.assertRaises(Exception):  # We're now catching any exception
            self.app.submit_expense()
        
        self.assertEqual(len(self.app.expenses_df), 0)

    def test_update_dashboard(self):
        # Add some test data
        test_data = pd.DataFrame({
            'Date': [datetime.now() - timedelta(days=i) for i in range(5)],
            'Amount': [100, 200, 150, 300, 250],
            'Category': ['Food', 'Transport', 'Utilities', 'Food', 'Entertainment']
        })
        self.app.expenses_df = test_data
        
        self.app.update_dashboard()
        
        # Check if graphs are created (this is a basic check, as we can't easily inspect the graph content in a unit test)
        self.assertGreater(len(self.app.graphs_frame.winfo_children()), 0)

    def test_load_expenses(self):
        # Create a test CSV file
        test_data = pd.DataFrame({
            'Date': ['2023-08-23', '2023-08-24'],
            'Amount': [100, 200],
            'Category': ['Food', 'Transport']
        })
        test_data.to_csv(self.app.data_file, index=False)
        
        loaded_df = self.app.load_expenses()
        
        self.assertEqual(len(loaded_df), 2)
        self.assertEqual(set(loaded_df.columns), set(['Date', 'Amount', 'Category']))

    def test_load_expenses_with_invalid_file(self):
        # Create an invalid CSV file
        with open(self.app.data_file, 'w') as f:
            f.write("Invalid,CSV,File,Format\n1,2,3,4")
        
        loaded_df = self.app.load_expenses()
        
        self.assertTrue(any(file.startswith(f"{self.app.data_file}.bak") for file in os.listdir()))
        self.assertEqual(len(loaded_df), 0)  # Should return an empty DataFrame

if __name__ == '__main__':
    unittest.main()