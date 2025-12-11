import tkinter as tk
from tkinter import ttk

from book_search_gui import BookSearchGUI
from borrower_management_gui import BorrowerGUI
from finesPage import FinesGUI
from book_loans_gui import LoansGUI

def main():
    root = tk.Tk()
    root.title("Library Management System - CS 4347")
    root.geometry("1000x700")
    
    # Create tabbed interface
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Add  tabs
    notebook.add(BookSearchGUI(notebook), text="📚 Book Search")
    notebook.add(LoansGUI(notebook), text="📖 Check Out / Check In")
    notebook.add(BorrowerGUI(notebook), text="👤 New Borrower")
    notebook.add(FinesGUI(notebook), text="💰 Fines")
    
    # Footer
    footer = tk.Label(root, text="Library Management System", 
                     font=("Helvetica", 9), fg="gray")
    footer.pack(side="bottom", pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()