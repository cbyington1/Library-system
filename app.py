from book_search import search
import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library — Book Search")
        self.geometry("900x600")

        top = ttk.Frame(self, padding=12)
        top.pack(fill="x")
        ttk.Label(top, text="Search (ISBN, Title, or Author):").pack(side="left")
        self.q = tk.StringVar()
        ent = ttk.Entry(top, textvariable=self.q, width=50)
        ent.pack(side="left", padx=8)
        ent.bind("<Return>", lambda _e: self.do_search())
        ttk.Button(top, text="Search", command=self.do_search).pack(side="left")

        mid = ttk.Frame(self, padding=(12, 0, 12, 12))
        mid.pack(fill="both", expand=True)

        cols = ("isbn", "title", "authors", "status")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", height=18)
        for col in cols:
            self.tree.heading(col, text=col.upper())
        self.tree.column("isbn", width=160, anchor="w")
        self.tree.column("title", width=280, anchor="w")
        self.tree.column("authors", width=260, anchor="w")
        self.tree.column("status", width=80, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")

        self.status = tk.StringVar(value="Ready")
        sb = ttk.Label(self, textvariable=self.status, anchor="w", relief="groove")
        sb.pack(fill="x")

    def do_search(self):
        q = (self.q.get() or "").strip()
        if not q:
            messagebox.showinfo("Search", "Type something (ISBN, title, or author).")
            return
        try:
            self.status.set("Searching…")
            self.update_idletasks()
            rows = search(q)  # <-- call Milestone-2 directly
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                isbn = r.get("isbn", "")
                title = r.get("title", "")
                authors = r.get("authors", "") or ""
                status = "IN" if r.get("available", True) else "OUT"
                self.tree.insert("", "end", values=(isbn, title, authors, status))
            self.status.set(f"Found {len(rows)} result(s)")
        except Exception as e:
            self.status.set("Ready")
            messagebox.showerror("Search failed", str(e))

if __name__ == "__main__":
    App().mainloop()


