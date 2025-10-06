#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import re

IDENT_RE = re.compile(r'^[A-Za-z0-9_]+$')

def valid_ident(name: str) -> bool:
    return bool(name) and bool(IDENT_RE.match(name))

def quote_ident(name: str) -> str:
    return f"`{name.replace('`','``')}`"

class CreateTableGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Create Table Designer")
        self.geometry("860x560")
        self.resizable(True, True)

        self.columns = []
        self.selected_index = None

        self.db_user = None
        self.db_password = None
        self.db_name = None

        self._build_ui()
        self._build_right_and_finish()

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)

        tk.Label(top, text="Table name:").grid(row=0, column=0, sticky="w")
        self.table_var = tk.StringVar()
        tk.Entry(top, textvariable=self.table_var, width=28).grid(row=0, column=1, sticky="w", padx=(6,12))

        left = tk.LabelFrame(self, text="Column Editor", padx=8, pady=8)
        left.pack(side="left", fill="both", expand=True, padx=(10,5), pady=10)

        row = tk.Frame(left)
        row.pack(fill="x", pady=(0,6))
        tk.Label(row, text="Col name:").grid(row=0, column=0, sticky="w")
        self.col_name_var = tk.StringVar()
        tk.Entry(row, textvariable=self.col_name_var, width=22).grid(row=0, column=1, padx=6)

        tk.Label(row, text="Type:").grid(row=0, column=2, sticky="w", padx=(8,0))
        self.col_type_var = tk.StringVar(value="VARCHAR(255)")
        types = ["INT", "BIGINT", "VARCHAR(255)", "TEXT", "DATE", "DATETIME", "FLOAT", "DOUBLE", "BOOLEAN"]
        ttk.Combobox(row, values=types, textvariable=self.col_type_var, width=20).grid(row=0, column=3, padx=6)

        flags = tk.Frame(left)
        flags.pack(fill="x", pady=(0,6))
        self.notnull_var = tk.BooleanVar(value=False)
        self.ai_var = tk.BooleanVar(value=False)
        self.pk_var = tk.BooleanVar(value=False)
        tk.Checkbutton(flags, text="NOT NULL", variable=self.notnull_var).pack(side="left", padx=6)
        tk.Checkbutton(flags, text="AUTO_INCREMENT", variable=self.ai_var).pack(side="left", padx=6)
        tk.Checkbutton(flags, text="PRIMARY KEY", variable=self.pk_var).pack(side="left", padx=6)

        dv_frame = tk.Frame(left)
        dv_frame.pack(fill="x", pady=(0,6))
        tk.Label(dv_frame, text="Default (optional):").pack(side="left")
        self.default_var = tk.StringVar()
        tk.Entry(dv_frame, textvariable=self.default_var, width=26).pack(side="left", padx=6)

        ctrl = tk.Frame(left)
        ctrl.pack(fill="x", pady=(6,8))
        self.confirm_btn = tk.Button(ctrl, text="Confirm (Add/Update)", command=self.on_confirm)
        self.confirm_btn.pack(side="left", padx=6)
        tk.Button(ctrl, text="Add New (clear)", command=self.on_add_new).pack(side="left", padx=6)
        tk.Button(ctrl, text="Delete Selected", command=self.on_delete_selected).pack(side="left", padx=6)

        list_frame = tk.Frame(left)
        list_frame.pack(fill="both", expand=True, pady=(6,0))
        self.cols_listbox = tk.Listbox(list_frame, exportselection=False)
        self.cols_listbox.pack(side="left", fill="both", expand=True)
        self.cols_listbox.bind("<<ListboxSelect>>", self.on_list_select)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.cols_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.cols_listbox.config(yscrollcommand=scrollbar.set)

    def _build_right_and_finish(self):
        right = tk.LabelFrame(self, text="Preview & Actions", padx=8, pady=8)
        right.pack(side="right", fill="both", expand=True, padx=(5,10), pady=10)

        tk.Label(right, text="Generated SQL Preview:").pack(anchor="w")
        self.preview = tk.Text(right, height=18, wrap="word")
        self.preview.pack(fill="both", expand=True, pady=(6,8))

        btn_row = tk.Frame(right)
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="Preview SQL", command=self.refresh_preview).pack(side="left", padx=6)
        tk.Button(btn_row, text="Clear Preview", command=lambda: self.preview.delete("1.0", "end")).pack(side="left", padx=6)

        tk.Button(btn_row, text="Finish (print SQL & exit)", fg="white", bg="#2E8B57",
                  command=self.on_finish).pack(side="right", padx=6)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(right, textvariable=self.status_var, anchor="w").pack(fill="x", pady=(8,0))

    # ----------------- Handlers -----------------
    def on_confirm(self):
        name = self.col_name_var.get().strip()
        if not name:
            messagebox.showwarning("Input", "Column name required", parent=self); return
        if not valid_ident(name):
            if not messagebox.askyesno("Non-standard name", "Column name contains non-alnum/underscore characters. Continue?"):
                return

        typ = self.col_type_var.get().strip() or "VARCHAR(255)"
        notnull = bool(self.notnull_var.get())
        ai = bool(self.ai_var.get())
        pk = bool(self.pk_var.get())
        default = self.default_var.get().strip()
        if default == "":
            default = None

        # AUTO_INCREMENT requires integer types
        if ai and not typ.upper().startswith(("INT", "BIGINT")):
            messagebox.showwarning("Type error", "AUTO_INCREMENT requires INT/BIGINT type", parent=self); return

        entry = {"name": name, "type": typ, "notnull": notnull, "ai": ai, "pk": pk, "default": default}

        if self.selected_index is None:
            # add new (append)
            self.columns.append(entry)
            self.cols_listbox.insert("end", self._col_display_text(entry))
            self.status_var.set(f"Added column: {name}")
        else:
            # update existing
            idx = self.selected_index
            old = self.columns[idx]
            self.columns[idx] = entry
            self.cols_listbox.delete(idx)
            self.cols_listbox.insert(idx, self._col_display_text(entry))
            self.cols_listbox.select_set(idx)
            self.status_var.set(f"Updated column {old['name']} → {name}")

        # keep selection behavior: after confirm, deselect (treat as finished)
        self.on_add_new()

    def on_add_new(self):
        self.selected_index = None
        self.cols_listbox.selection_clear(0, "end")
        self.col_name_var.set("")
        self.col_type_var.set("VARCHAR(255)")
        self.notnull_var.set(False)
        self.ai_var.set(False)
        self.pk_var.set(False)
        self.default_var.set("")
        self.col_name_var.get()  # noop: keep focus
        self.focus_entry()

    def on_delete_selected(self):
        sel = self.cols_listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete", "No selection to delete", parent=self); return
        idx = sel[0]
        val = self.columns.pop(idx)
        self.cols_listbox.delete(idx)
        self.selected_index = None
        self.status_var.set(f"Deleted column {val['name']}")
        self.on_add_new()

    def on_list_select(self, event=None):
        sel = self.cols_listbox.curselection()
        if not sel:
            self.selected_index = None
            return
        idx = sel[0]
        self.selected_index = idx
        entry = self.columns[idx]
        self.col_name_var.set(entry["name"])
        self.col_type_var.set(entry["type"])
        self.notnull_var.set(entry["notnull"])
        self.ai_var.set(entry["ai"])
        self.pk_var.set(entry["pk"])
        self.default_var.set(entry["default"] or "")
        self.status_var.set(f"Editing column {idx+1}: {entry['name']}")
        self.focus_entry()

    def focus_entry(self):
        self.after(5, lambda: (self.focus_force(), self.nametowidget(self.children['!labelframe'].children['!frame'].children['!entry']).focus_set()) if False else None)
        for child in self.winfo_children():
            for sub in child.winfo_children():
                if isinstance(sub, tk.Entry):
                    sub.focus_set()
                    try:
                        sub.selection_range(0, "end")
                    except Exception:
                        pass
                    return

    def _col_display_text(self, entry):
        txt = f"{entry['name']}  {entry['type']}"
        flags = []
        if entry['notnull']: flags.append("NOT NULL")
        if entry['ai']: flags.append("AUTO_INCREMENT")
        if entry['pk']: flags.append("PK")
        if entry['default'] is not None:
            flags.append(f"DEFAULT={entry['default']}")
        if flags:
            txt += "  [" + ", ".join(flags) + "]"
        return txt

    # Build SQL
    def build_create_sql(self):
        tbl = self.table_var.get().strip()
        if not tbl:
            return ""
        if not valid_ident(tbl):
            if not messagebox.askyesno("Table name", "Table name contains unusual chars. Continue?"):
                return ""
        parts = []
        pk_cols = []
        for c in self.columns:
            name = quote_ident(c["name"])
            typ = c["type"]
            seq = f"{name} {typ}"
            if c["notnull"]:
                seq += " NOT NULL"
            if c["ai"]:
                seq += " AUTO_INCREMENT"
            if c["default"] is not None:
                pv = c["default"]
                if pv.upper() == "NULL":
                    seq += " DEFAULT NULL"
                elif re.match(r'^[0-9.\-]+$', pv):
                    seq += f" DEFAULT {pv}"
                else:
                    seq += f" DEFAULT '{pv.replace("'","''")}'"
            parts.append(seq)
            if c["pk"]:
                pk_cols.append(quote_ident(c["name"]))
        if pk_cols:
            parts.append(f"PRIMARY KEY ({', '.join(pk_cols)})")
        if not parts:
            return ""
        full = ",\n  ".join(parts)
        qualified = quote_ident(tbl) if not self.db_name else f"{quote_ident(self.db_name)}.{quote_ident(tbl)}"
        sql = f"CREATE TABLE {qualified} (\n  {full}\n) ENGINE=InnoDB;"
        return sql

    def refresh_preview(self):
        sql = self.build_create_sql()
        self.preview.delete("1.0", "end")
        if not sql:
            self.preview.insert("end", "-- SQL couldn't be built (missing table name or columns)\n")
        else:
            self.preview.insert("end", sql)
        self.status_var.set("Preview refreshed")

    def on_finish(self):
        sql = self.build_create_sql()
        if not sql:
            if not messagebox.askyesno("No SQL", "No SQL was generated. Do you want to output an empty string and exit?"):
                return
            sql = ""
        try:
            sys.stdout.write(sql + "\n")
            sys.stdout.flush()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print SQL: {e}", parent=self)
        finally:
            self.destroy()
            sys.exit(0)

if __name__ == "__main__":
    app = CreateTableGUI()
    app.mainloop()
