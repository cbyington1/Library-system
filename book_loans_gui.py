import tkinter as tk
from tkinter import ttk, messagebox
from book_loans import checkout, find_loans, checkin


class LoansGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # checkout/checkin tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Checkout tab
        checkout_frame = ttk.Frame(notebook)
        notebook.add(checkout_frame, text="Check Out")
        self.create_checkout_tab(checkout_frame)
        
        # Checkin tab
        checkin_frame = ttk.Frame(notebook)
        notebook.add(checkin_frame, text="Check In")
        self.create_checkin_tab(checkin_frame)
    
    def create_checkout_tab(self, parent):
        # Title
        tk.Label(parent, text="Check Out Book", font=("Helvetica", 14, "bold")).pack(pady=15)
        
        # Input frame
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=20, padx=20)
        
        tk.Label(input_frame, text="ISBN:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.checkout_isbn = tk.Entry(input_frame, width=30)
        self.checkout_isbn.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="Card Number:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.checkout_card = tk.Entry(input_frame, width=30)
        self.checkout_card.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Check Out", command=self.do_checkout, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_checkout, width=15).pack(side="left", padx=5)
        
        # Status
        self.checkout_status = tk.Label(parent, text="Ready", relief="sunken", anchor="w")
        self.checkout_status.pack(fill="x", padx=10, pady=10)
    
    def create_checkin_tab(self, parent):
        # Title
        tk.Label(parent, text="Check In Book", font=("Helvetica", 14, "bold")).pack(pady=15)
        
        # Search frame
        search_frame = tk.Frame(parent)
        search_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(search_frame, text="Search Active Loans:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        tk.Label(search_frame, text="ISBN:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.search_isbn = tk.Entry(search_frame, width=25)
        self.search_isbn.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(search_frame, text="Card Number:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.search_card = tk.Entry(search_frame, width=25)
        self.search_card.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(search_frame, text="Borrower Name:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.search_name = tk.Entry(search_frame, width=25)
        self.search_name.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        tk.Button(search_frame, text="Find Active Loans", command=self.do_find_loans, width=20).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Results frame
        results_frame = tk.Frame(parent)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview for results
        cols = ("loan_id", "isbn", "title", "card_no", "borrower", "date_out", "due_date")
        self.loans_tree = ttk.Treeview(results_frame, columns=cols, show="headings", height=10)
        
        self.loans_tree.heading("loan_id", text="Loan ID")
        self.loans_tree.heading("isbn", text="ISBN")
        self.loans_tree.heading("title", text="Title")
        self.loans_tree.heading("card_no", text="Card No")
        self.loans_tree.heading("borrower", text="Borrower")
        self.loans_tree.heading("date_out", text="Date Out")
        self.loans_tree.heading("due_date", text="Due Date")
        
        self.loans_tree.column("loan_id", width=70, anchor="center")
        self.loans_tree.column("isbn", width=120)
        self.loans_tree.column("title", width=200)
        self.loans_tree.column("card_no", width=70, anchor="center")
        self.loans_tree.column("borrower", width=150)
        self.loans_tree.column("date_out", width=100, anchor="center")
        self.loans_tree.column("due_date", width=100, anchor="center")
        
        self.loans_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.loans_tree.yview)
        self.loans_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Check in button
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Check In Selected", command=self.do_checkin, width=20).pack()
        
        # Status
        self.checkin_status = tk.Label(parent, text="Ready", relief="sunken", anchor="w")
        self.checkin_status.pack(fill="x", padx=10, pady=10)
    
    def do_checkout(self):
        isbn = self.checkout_isbn.get().strip()
        card_no = self.checkout_card.get().strip()
        
        if not isbn or not card_no:
            messagebox.showerror("Error", "Both ISBN and Card Number are required.")
            return
        
        try:
            card_no = int(card_no)
            result = checkout(isbn, card_no)
            
            if result.startswith("SUCCESS"):
                messagebox.showinfo("Success", result)
                self.checkout_status.config(text=result)
                self.clear_checkout()
            else:
                messagebox.showerror("Checkout Failed", result)
                self.checkout_status.config(text=result)
        except ValueError:
            messagebox.showerror("Error", "Card Number must be a number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_checkout(self):
        self.checkout_isbn.delete(0, tk.END)
        self.checkout_card.delete(0, tk.END)
    
    def do_find_loans(self):
        isbn = self.search_isbn.get().strip() or None
        card_no = self.search_card.get().strip() or None
        name = self.search_name.get().strip() or None
        
        if card_no:
            try:
                card_no = int(card_no)
            except ValueError:
                messagebox.showerror("Error", "Card Number must be a number.")
                return
        
        try:
            self.checkin_status.config(text="Searching...")
            self.update_idletasks()
            
            results = find_loans(isbn=isbn, card_no=card_no, name=name)
            
            # Clear existing results
            self.loans_tree.delete(*self.loans_tree.get_children())
            
            # Populate results
            for loan in results:
                self.loans_tree.insert("", "end", values=(
                    loan["loan_id"],
                    loan["isbn"],
                    loan["title"],
                    loan["card_no"],
                    loan["bname"],
                    loan["date_out"],
                    loan["due_date"]
                ))
            
            self.checkin_status.config(text=f"Found {len(results)} active loan(s)")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.checkin_status.config(text="Ready")
    
    def do_checkin(self):
        selection = self.loans_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a loan to check in.")
            return
        
        # Get selected loan IDs 
        loan_ids = [self.loans_tree.item(item)["values"][0] for item in selection]
        
        if len(loan_ids) > 3:
            messagebox.showwarning("Too Many", "You can only check in up to 3 books at once.")
            return
        
        try:
            for loan_id in loan_ids:
                result = checkin(loan_id)
                if not result.startswith("SUCCESS"):
                    messagebox.showerror("Error", f"Failed to check in Loan {loan_id}: {result}")
                    return
            
            messagebox.showinfo("Success", f"Successfully checked in {len(loan_ids)} book(s).")
            self.checkin_status.config(text=f"Checked in {len(loan_ids)} book(s)")
            
            # Refresh the list
            self.do_find_loans()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library System - Book Loans")
    root.geometry("900x600")
    
    LoansGUI(root).pack(fill="both", expand=True)
    
    root.mainloop()