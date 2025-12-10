import tkinter as tk
from tkinter import messagebox
from borrower_management import create_borrower


def on_create_borrower():
    """Handle Create Borrower button click."""
    name = entry_name.get().strip()
    ssn = entry_ssn.get().strip()
    address = entry_address.get().strip()
    phone = entry_phone.get().strip()

    # Basic validation for required fields
    if not name or not ssn or not address:
        messagebox.showerror(
            "Missing Information",
            "Name, SSN, and Address are required."
        )
        return

    # Call backend function from borrower_management.py
    result = create_borrower(ssn, name, address, phone or None)

    # In this repo, create_borrower returns:
    #   card_no (on success)
    #   "Error: message" (on failure)
    if isinstance(result, str) and result.startswith("Error"):
        messagebox.showerror("Error Creating Borrower", result)
    else:
        messagebox.showinfo(
            "Success",
            f"Borrower created successfully!\nCard Number: {result}"
        )
        clear_fields()


def clear_fields():
    """Clear all input fields."""
    entry_name.delete(0, tk.END)
    entry_ssn.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone.delete(0, tk.END)


# --- GUI BUILD ---

root = tk.Tk()
root.title("Library System - Borrower Management")
root.geometry("450x260")

# Title
label_title = tk.Label(
    root,
    text="Create New Borrower",
    font=("Helvetica", 14, "bold")
)
label_title.grid(row=0, column=0, columnspan=2, pady=(10, 10))

# Name
label_name = tk.Label(root, text="Name*:")
label_name.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=5)
entry_name = tk.Entry(root, width=35)
entry_name.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)

# SSN
label_ssn = tk.Label(root, text="SSN*:")
label_ssn.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=5)
entry_ssn = tk.Entry(root, width=35)
entry_ssn.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)

# Address
label_address = tk.Label(root, text="Address*:")
label_address.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=5)
entry_address = tk.Entry(root, width=35)
entry_address.grid(row=3, column=1, sticky="w", padx=(0, 10), pady=5)

# Phone
label_phone = tk.Label(root, text="Phone (optional):")
label_phone.grid(row=4, column=0, sticky="e", padx=(10, 5), pady=5)
entry_phone = tk.Entry(root, width=35)
entry_phone.grid(row=4, column=1, sticky="w", padx=(0, 10), pady=5)

# Buttons
button_create = tk.Button(
    root,
    text="Create Borrower",
    command=on_create_borrower,
    width=18
)
button_create.grid(row=5, column=0, padx=10, pady=(15, 10), sticky="e")

button_clear = tk.Button(
    root,
    text="Clear",
    command=clear_fields,
    width=10
)
button_clear.grid(row=5, column=1, padx=10, pady=(15, 10), sticky="w")

label_required = tk.Label(root, text="* required fields", fg="gray")
label_required.grid(row=6, column=0, columnspan=2, pady=(0, 10))

if __name__ == "__main__":
    root.mainloop()
