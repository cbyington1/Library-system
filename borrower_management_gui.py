import tkinter as tk
from tkinter import ttk, messagebox 
from borrower_management import create_borrower


class BorrowerGUI(ttk.Frame): 
    def __init__(self, parent):  
        super().__init__(parent)
        
        # Title
        label_title = tk.Label(
            self,  
            text="Create New Borrower",
            font=("Helvetica", 14, "bold")
        )
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 10))

        # Name
        label_name = tk.Label(self, text="Name*:")
        label_name.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=5)
        self.entry_name = tk.Entry(self, width=35)  
        self.entry_name.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)

        # SSN
        label_ssn = tk.Label(self, text="SSN*:")
        label_ssn.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=5)
        self.entry_ssn = tk.Entry(self, width=35)  
        self.entry_ssn.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)

        # Address
        label_address = tk.Label(self, text="Address*:")
        label_address.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=5)
        self.entry_address = tk.Entry(self, width=35)  
        self.entry_address.grid(row=3, column=1, sticky="w", padx=(0, 10), pady=5)

        # Phone
        label_phone = tk.Label(self, text="Phone (optional):")
        label_phone.grid(row=4, column=0, sticky="e", padx=(10, 5), pady=5)
        self.entry_phone = tk.Entry(self, width=35)  
        self.entry_phone.grid(row=4, column=1, sticky="w", padx=(0, 10), pady=5)

        # Buttons
        button_create = tk.Button(
            self,
            text="Create Borrower",
            command=self.on_create_borrower, 
            width=18
        )
        button_create.grid(row=5, column=0, padx=10, pady=(15, 10), sticky="e")

        button_clear = tk.Button(
            self,
            text="Clear",
            command=self.clear_fields, 
            width=10
        )
        button_clear.grid(row=5, column=1, padx=10, pady=(15, 10), sticky="w")

        label_required = tk.Label(self, text="* required fields", fg="gray")
        label_required.grid(row=6, column=0, columnspan=2, pady=(0, 10))

    def on_create_borrower(self):  
        """Handle Create Borrower button click."""
        name = self.entry_name.get().strip() 
        ssn = self.entry_ssn.get().strip()
        address = self.entry_address.get().strip()
        phone = self.entry_phone.get().strip()

        if not name or not ssn or not address:
            messagebox.showerror(
                "Missing Information",
                "Name, SSN, and Address are required."
            )
            return

        result = create_borrower(ssn, name, address, phone or None)

        if isinstance(result, str) and result.startswith("Error"):
            messagebox.showerror("Error Creating Borrower", result)
        else:
            messagebox.showinfo(
                "Success",
                f"Borrower created successfully!\nCard Number: {result}"
            )
            self.clear_fields()

    def clear_fields(self):  
        """Clear all input fields."""
        self.entry_name.delete(0, tk.END)
        self.entry_ssn.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library System - Borrower Management")
    root.geometry("450x260")
    BorrowerGUI(root).pack(fill="both", expand=True)  
    root.mainloop()