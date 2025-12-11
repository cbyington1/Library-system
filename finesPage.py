import tkinter as tk
from tkinter import ttk, messagebox
from fines import get_fines_grouped, update_fines, pay_fines

class FinesGUI(ttk.Frame):  
    def __init__(self, parent):  
        super().__init__(parent)
        
        # ----- Card Number Input -----
        input_frame = tk.Frame(self)  
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Borrower Card No:").grid(row=0, column=0, padx=5)
        self.card_entry = tk.Entry(input_frame)
        self.card_entry.grid(row=0, column=1, padx=5)

        tk.Button(input_frame, text="Load Fines", command=self.load_fines).grid(row=0, column=2, padx=5)
        tk.Button(input_frame, text="Update Fines", command=self.update_fines).grid(row=0, column=3, padx=5)
        tk.Button(input_frame, text="Pay All Fines", command=self.pay_fines).grid(row=0, column=4, padx=5)

        # ----- Fines Table -----
        columns = ("loan_id", "isbn", "fine_amt", "paid", "date_out", "due_date", "date_in")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12) 
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=110)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview) 
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_fines(self):
        card_no = self.card_entry.get()

        if not card_no.isdigit():
            messagebox.showerror("Error", "Card number must be a number.")
            return

        fines = get_fines_grouped(int(card_no), include_paid=True)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for f in fines:
            self.tree.insert("", tk.END, values=(
                f["loan_id"],
                f["isbn"],
                f["fine_amt"],
                "Yes" if f["paid"] else "No",
                f["date_out"],
                f["due_date"],
                f["date_in"]
            ))

        messagebox.showinfo("Done", f"Loaded {len(fines)} fines.")

    def update_fines(self):
        updated = update_fines()
        messagebox.showinfo("Update Complete", f"{updated} fines updated.")
        self.load_fines()

    def pay_fines(self):
        card_no = self.card_entry.get()

        if not card_no.isdigit():
            messagebox.showerror("Error", "Card number must be a number.")
            return

        result = pay_fines(int(card_no))

        if isinstance(result, str):
            messagebox.showinfo("Result", result)
        else:
            messagebox.showinfo("Payment Successful", f"Paid total of ${result}")

        self.load_fines()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Fine Tracker")
    FinesGUI(root).pack(fill="both", expand=True) 
    root.mainloop()