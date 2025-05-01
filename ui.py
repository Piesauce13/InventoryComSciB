import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry  # You'll need to install this: pip install tkcalendar
import tkinter.font as tkfont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from PIL import  ImageTk, Image



class InventoryUI:
    def __init__(self, auth_system, inventory_manager):
        self.auth_system = auth_system
        self.inventory_manager = inventory_manager

        # Create main window
        self.root = tk.Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("1300x800")

        # Configure colors
        self.colors = {
            'primary': '#2c3e50',  # Dark Blue
            'secondary': '#3498db',  # Light Blue
            'success': '#2ecc71',  # Green
            'warning': '#f1c40f',  # Yellow
            'danger': '#e74c3c',  # Red
            'light': '#ecf0f1',  # Light Gray
            'dark': '#2c3e50',  # Dark Blue
            'white': '#ffffff',
            'bg': '#f5f6fa'  # Background
        }

        # Configure fonts
        self.fonts = {
            'title': ('Helvetica', 24, 'bold'),
            'header': ('Helvetica', 16, 'bold'),
            'normal': ('Helvetica', 12),
            'small': ('Helvetica', 10)
        }

        # Configure styles
        self.setup_styles()

        # Show login screen
        self.show_homepage()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Main.TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['white'])

        # Button styles
        style.configure('Primary.TButton',
                        background=self.colors['primary'],
                        foreground=self.colors['white'],
                        padding=10,
                        font=self.fonts['normal'])

        style.configure('Success.TButton',
                        background=self.colors['success'],
                        foreground=self.colors['white'],
                        padding=10,
                        font=self.fonts['normal'])

        style.configure('Warning.TButton',
                        background=self.colors['warning'],
                        foreground=self.colors['dark'],
                        padding=10,
                        font=self.fonts['normal'])

        style.configure('Danger.TButton',
                        background=self.colors['danger'],
                        foreground=self.colors['white'],
                        padding=10,
                        font=self.fonts['normal'])

    def show_homepage(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load background image 1300x800
        self.background_image = Image.open("./resources/storageBgCartoon.jpg")
        self.background_image = self.background_image.resize((1300, 800))
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        # Create canvas to display background
        self.canvas = tk.Canvas(self.root, width=1300, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Center coordinates
        center_x = 1300 // 2

        # Short description (centered)
        self.canvas.create_text(center_x + 2, 150 + 2,
                                text="Welcome to Inventory Management System",
                                font=('Helvetica', 35, 'bold'),
                                fill="black")
        self.canvas.create_text(center_x, 150,
                                text="Welcome to Inventory Management System",
                                font=('Helvetica', 35, 'bold'),
                                fill="white")

        # Buttons
        login_button = ttk.Button(self.root, text="Login", command=self.show_login_screen)
        signup_button = ttk.Button(self.root, text="Signup", command=self.show_register_screen)
        forget_button = ttk.Button(self.root, text="Forget Password", command=self.show_forget_pass_screen)

        # Place buttons on the canvas (centered below the text)
        self.canvas.create_window(center_x - 120, 300, window=login_button, width=100, height=40)
        self.canvas.create_window(center_x, 300, window=signup_button, width=100, height=40)
        self.canvas.create_window(center_x + 135, 300, window=forget_button, width=130, height=40)

        description = ("Effortless Storage Management. Maximum Efficiency. "
                       "Easily track, organize, and manage all types of storage"
                       " — from closets to warehouses. Quickly find items, keep "
                       "inventory updated, and maintain an organized system. "
                       "Start optimizing space today!")

        self.canvas.create_text(center_x + 1, 600 + 1,
                                width=1000,
                                anchor='center',
                                text=description,
                                font=('Helvetica', 18, 'bold'),
                                fill="black")
        self.canvas.create_text(center_x, 600,
                                width=1000,
                                anchor='center',
                                text=description,
                                font=('Helvetica', 18, 'bold'),
                                fill="white")

    def show_login_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame,
                                text="Inventory Management System",
                                font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=20)

        # Login form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)

        # Username
        ttk.Label(form_frame, text="Username:", font=('Helvetica', 12)).pack()
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.username_var, width=30)
        username_entry.pack(pady=5)

        # Password
        ttk.Label(form_frame, text="Password:", font=('Helvetica', 12)).pack()
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, show="•", width=30)
        password_entry.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="Login",
                   command=self.handle_login).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Back to Home",
                   command=self.show_homepage).pack(side=tk.LEFT, padx=5)
        # ttk.Button(button_frame,
        #            text="Register",
        #            command=self.show_register_screen).pack(side=tk.LEFT, padx=5)

        # ttk.Button(button_frame,
        #            text="Forget Password",
        #            command=self.show_forget_pass_screen).pack(side=tk.LEFT, padx=5)

    def show_main_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create sidebar
        sidebar = ttk.Frame(main_container)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # User info
        ttk.Label(sidebar,
                  text=f"Welcome, {self.auth_system.current_user['username']}",
                  font=('Helvetica', 12, 'bold')).pack(pady=10)

        # Navigation buttons
        ttk.Button(sidebar,
                   text="View Products",
                   command=self.show_products).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Add Product",
                   command=self.show_add_product).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Search Products",
                   command=self.show_search_products).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Low Stock Items",
                   command=self.show_low_stock).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Expired Products",
                   command=self.show_expired_products).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Sort Products",
                   command=self.show_sort_products).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Update Product",
                   command=self.show_update_product).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Delete Product",
                   command=self.show_delete_product).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Show Statistics",
                   command=self.show_statistic).pack(fill=tk.X, pady=20)

        if self.auth_system.is_admin():
            ttk.Button(sidebar,
                       text="Manage Users",
                       command=self.show_manage_users).pack(fill=tk.X, pady=5)

        ttk.Button(sidebar,
                   text="Logout",
                   command=self.handle_logout).pack(fill=tk.X, pady=20)

        # Create main content area
        self.content_area = ttk.Frame(main_container)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Show products by default
        self.show_products()

    def show_products(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Title
        ttk.Label(self.content_area,
                  text="Products",
                  font=('Helvetica', 20, 'bold')).pack(pady=10)

        # Create table
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity', 'Expiry Date', 'Manufacture Date', 'Notes')
        tree = ttk.Treeview(self.content_area, columns=columns, show='headings')

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content_area, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load products
        products = self.inventory_manager.get_all_products()
        for product in products:
            tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['category'],
                f"${product['price']:.2f}",
                product['quantity'],
                product['expiry_date'] if product['expiry_date'] else 'N/A',
                product['mfg_date'] if product['mfg_date'] else 'N/A',
                product['notes'] if product['notes'] else 'N/A'
            ))

    def show_add_product(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Create scrollable frame
        canvas = tk.Canvas(self.content_area, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Title
        title_frame = ttk.Frame(scrollable_frame, style='Main.TFrame')
        title_frame.pack(fill=tk.X, pady=20)

        ttk.Label(title_frame,
                  text="Add New Product",
                  font=self.fonts['title'],
                  background=self.colors['bg']).pack()

        # Form
        form_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        form_frame.pack(padx=20, pady=10, fill=tk.X)

        # Create form fields
        fields = {}

        # Basic Information Section
        basic_info = ttk.LabelFrame(form_frame, text="Basic Information", padding=10)
        basic_info.pack(fill=tk.X, padx=10, pady=5)

        # Name
        ttk.Label(basic_info, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        fields['name'] = ttk.Entry(basic_info, width=40)
        fields['name'].grid(row=0, column=1, padx=5, pady=5)

        # Category
        ttk.Label(basic_info, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        categories = ['Electronics', 'Food', 'Clothing', 'Books', 'Other']  # Add your categories
        fields['category'] = ttk.Combobox(basic_info, values=categories, width=37)
        fields['category'].grid(row=1, column=1, padx=5, pady=5)

        # Stock Information Section
        stock_info = ttk.LabelFrame(form_frame, text="Stock Information", padding=10)
        stock_info.pack(fill=tk.X, padx=10, pady=5)

        # Price
        ttk.Label(stock_info, text="Price ($):").grid(row=0, column=0, padx=5, pady=5)
        fields['price'] = ttk.Entry(stock_info, width=20)
        fields['price'].grid(row=0, column=1, padx=5, pady=5)

        # Quantity
        ttk.Label(stock_info, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)

        # Quantity frame with +/- buttons
        qty_frame = ttk.Frame(stock_info)
        qty_frame.grid(row=1, column=1, padx=5, pady=5)

        fields['quantity'] = ttk.Entry(qty_frame, width=10)
        fields['quantity'].insert(0, "0")
        fields['quantity'].pack(side=tk.LEFT, padx=5)

        def change_quantity(amount):
            try:
                current = int(fields['quantity'].get())
                new_value = max(0, current + amount)
                fields['quantity'].delete(0, tk.END)
                fields['quantity'].insert(0, str(new_value))
            except ValueError:
                fields['quantity'].delete(0, tk.END)
                fields['quantity'].insert(0, "0")

        ttk.Button(qty_frame,
                   text="-",
                   style='Danger.TButton',
                   command=lambda: change_quantity(-1),
                   width=3).pack(side=tk.LEFT, padx=2)

        ttk.Button(qty_frame,
                   text="+",
                   style='Success.TButton',
                   command=lambda: change_quantity(1),
                   width=3).pack(side=tk.LEFT, padx=2)

        # Minimum stock level
        ttk.Label(stock_info, text="Minimum Stock Level:").grid(row=2, column=0, padx=5, pady=5)
        fields['min_stock'] = ttk.Entry(stock_info, width=20)
        fields['min_stock'].insert(0, "5")
        fields['min_stock'].grid(row=2, column=1, padx=5, pady=5)

        # Dates Section
        dates_info = ttk.LabelFrame(form_frame, text="Dates", padding=10)
        dates_info.pack(fill=tk.X, padx=10, pady=5)

        # Manufacturing Date
        ttk.Label(dates_info, text="Manufacturing Date:").grid(row=0, column=0, padx=5, pady=5)
        fields['mfg_date'] = DateEntry(dates_info,
                                       width=20,
                                       background=self.colors['primary'],
                                       foreground=self.colors['white'],
                                       borderwidth=2,
                                       date_pattern='yyyy-mm-dd',
                                       maxdate=datetime.now())  # Can't be future date
        fields['mfg_date'].grid(row=0, column=1, padx=5, pady=5)

        # Has Expiry Date Checkbox
        has_expiry_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(dates_info,
                        text="Product has expiry date",
                        variable=has_expiry_var,
                        command=lambda: fields['expiry_date'].configure(
                            state='normal' if has_expiry_var.get() else 'disabled')).grid(row=1, column=0, columnspan=2,
                                                                                          padx=5, pady=5)

        # Expiry Date
        ttk.Label(dates_info, text="Expiry Date:").grid(row=2, column=0, padx=5, pady=5)
        fields['expiry_date'] = DateEntry(dates_info,
                                          width=20,
                                          background=self.colors['primary'],
                                          foreground=self.colors['white'],
                                          borderwidth=2,
                                          date_pattern='yyyy-mm-dd',
                                          mindate=datetime.now())  # Must be future date
        fields['expiry_date'].grid(row=2, column=1, padx=5, pady=5)

        # Notes Section
        notes_info = ttk.LabelFrame(form_frame, text="Notes", padding=10)
        notes_info.pack(fill=tk.X, padx=10, pady=5)

        # Notes Text Area
        fields['notes'] = tk.Text(notes_info, height=4, width=50)
        fields['notes'].pack(padx=5, pady=5, fill=tk.X)

        def validate_dates():
            if has_expiry_var.get() and not fields['expiry_date'].get():
                messagebox.showerror("Error", "Please select an expiry date")
                return False
            return True

        def save_product():
            try:
                # Validate inputs
                if not fields['name'].get().strip():
                    raise ValueError("Product name is required")

                if not fields['category'].get().strip():
                    raise ValueError("Category is required")

                if not validate_dates():
                    return

                # Get values
                product_data = {
                    'name': fields['name'].get().strip(),
                    'category': fields['category'].get().strip(),
                    'price': float(fields['price'].get()),
                    'quantity': int(fields['quantity'].get()),
                    'min_stock_level': int(fields['min_stock'].get()),
                    'mfg_date': fields['mfg_date'].get_date().strftime('%Y-%m-%d'),
                    'expiry_date': fields['expiry_date'].get_date().strftime(
                        '%Y-%m-%d') if has_expiry_var.get() else None,
                    'notes': fields['notes'].get("1.0", tk.END).strip()
                }

                success, message = self.inventory_manager.add_product(**product_data)

                if success:
                    messagebox.showinfo("Success", "Product added successfully!")
                    self.show_products()
                else:
                    messagebox.showerror("Error", message)

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="Save Product",
                   style='Success.TButton',
                   command=save_product).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Clear Form",
                   style='Warning.TButton',
                   command=lambda: [field.delete(0, tk.END) for field in fields.values() if
                                    isinstance(field, ttk.Entry)]
                   ).pack(side=tk.LEFT, padx=5)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_search_products(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Search frame
        search_frame = ttk.Frame(self.content_area)
        search_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Label(search_frame,
                  text="Search Products",
                  font=('Helvetica', 20, 'bold')).pack(side=tk.LEFT, padx=10)

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        def perform_search():
            query = search_var.get()
            results = self.inventory_manager.search_products(query)
            self.display_products(results)

        ttk.Button(search_frame,
                   text="Search",
                   command=perform_search).pack(side=tk.LEFT, padx=5)

        # Results area
        self.results_frame = ttk.Frame(self.content_area)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    def show_low_stock(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Title frame
        title_frame = ttk.Frame(self.content_area, style='Main.TFrame')
        title_frame.pack(fill=tk.X, pady=20)

        ttk.Label(title_frame,
                  text="Low Stock Products",
                  font=self.fonts['title'],
                  background=self.colors['bg']).pack(side=tk.LEFT, padx=20)

        # Statistics frame
        stats_frame = ttk.Frame(self.content_area, style='Card.TFrame')
        stats_frame.pack(fill=tk.X, padx=20, pady=10)

        # Get low stock products
        low_stock = self.inventory_manager.get_low_stock_products()
        critical_stock = [p for p in low_stock if p['quantity'] == 0]
        warning_stock = [p for p in low_stock if 0 < p['quantity'] < p['min_stock_level']]

        # Stats display
        stats = [
            ("Critical Stock", len(critical_stock), self.colors['danger']),
            ("Low Stock", len(warning_stock), self.colors['warning']),
            ("Total Items", len(low_stock), self.colors['primary'])
        ]

        for title, value, color in stats:
            stat_frame = ttk.Frame(stats_frame, style='Card.TFrame')
            stat_frame.pack(side=tk.LEFT, padx=20, pady=10, expand=True)

            ttk.Label(stat_frame,
                      text=title,
                      font=self.fonts['header']).pack()

            ttk.Label(stat_frame,
                      text=str(value),
                      font=self.fonts['title'],
                      foreground=color).pack()

        # Table frame
        table_frame = ttk.Frame(self.content_area, style='Card.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create table
        columns = ('ID', 'Name', 'Category', 'Current Stock', 'Min Stock', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert data with color tags
        tree.tag_configure('critical', background=self.colors['danger'])
        tree.tag_configure('warning', background=self.colors['warning'])

        for product in low_stock:
            status = "Out of Stock" if product['quantity'] == 0 else "Low Stock"
            tag = 'critical' if product['quantity'] == 0 else 'warning'

            tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['category'],
                product['quantity'],
                product['min_stock_level'],
                status
            ), tags=(tag,))

        # Quick restock button
        def show_restock_dialog():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a product to restock")
                return

            product_id = tree.item(selected_item[0])['values'][0]

            # Create restock dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Restock Product")
            dialog.geometry("300x200")
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(dialog,
                      text="Enter Quantity to Add:",
                      font=self.fonts['header']).pack(pady=20)

            quantity_var = tk.StringVar(value="1")
            quantity_frame = ttk.Frame(dialog)
            quantity_frame.pack(pady=10)

            ttk.Button(quantity_frame,
                       text="-",
                       style='Danger.TButton',
                       command=lambda: quantity_var.set(str(max(1, int(quantity_var.get()) - 1))),
                       width=3).pack(side=tk.LEFT, padx=5)

            ttk.Entry(quantity_frame,
                      textvariable=quantity_var,
                      width=10).pack(side=tk.LEFT, padx=5)

            ttk.Button(quantity_frame,
                       text="+",
                       style='Success.TButton',
                       command=lambda: quantity_var.set(str(int(quantity_var.get()) + 1)),
                       width=3).pack(side=tk.LEFT, padx=5)

            def restock():
                try:
                    quantity = int(quantity_var.get())
                    if quantity <= 0:
                        raise ValueError("Quantity must be positive")

                    product = self.inventory_manager.get_product_by_id(product_id)
                    new_quantity = product['quantity'] + quantity

                    success, message = self.inventory_manager.update_product(
                        product_id,
                        quantity=new_quantity
                    )

                    if success:
                        messagebox.showinfo("Success", f"Added {quantity} items to stock")
                        dialog.destroy()
                        self.show_low_stock()  # Refresh the view
                    else:
                        messagebox.showerror("Error", message)

                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(dialog,
                       text="Restock",
                       style='Success.TButton',
                       command=restock).pack(pady=20)

        button_frame = ttk.Frame(self.content_area, style='Main.TFrame')
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(button_frame,
                   text="Quick Restock",
                   style='Success.TButton',
                   command=show_restock_dialog).pack(side=tk.LEFT, padx=5)

    def show_expired_products(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        ttk.Label(self.content_area,
                  text="Expired Products",
                  font=('Helvetica', 20, 'bold')).pack(pady=10)

        # Create table
        columns = ('ID', 'Name', 'Category', 'Quantity', 'Expiry Date', 'Manufacture Date', 'Notes')
        tree = ttk.Treeview(self.content_area, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(self.content_area, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load expired products
        products = self.inventory_manager.get_expired_products()
        for product in products:
            tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['category'],
                product['quantity'],
                product['expiry_date'],
                product['mfg_date'] if product['mfg_date'] else 'N/A',
                product['notes'] if product['notes'] else 'N/A'
            ))

    def show_sort_products(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Sort options frame
        sort_frame = ttk.Frame(self.content_area)
        sort_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Label(sort_frame,
                  text="Sort Products",
                  font=('Helvetica', 20, 'bold')).pack(pady=10)

        # Sort options
        sort_options = ['name', 'category', 'price', 'quantity', 'expiry_date']
        sort_var = tk.StringVar(value='name')

        ttk.Label(sort_frame, text="Sort by:").pack()
        sort_combo = ttk.Combobox(sort_frame,
                                  textvariable=sort_var,
                                  values=sort_options,
                                  state='readonly')
        sort_combo.pack(pady=5)

        # Ascending/Descending
        ascending_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(sort_frame,
                        text="Ascending order",
                        variable=ascending_var).pack(pady=5)

        def apply_sort():
            products = self.inventory_manager.get_products_sorted(
                sort_by=sort_var.get(),
                ascending=ascending_var.get()
            )
            self.display_products(products)

        ttk.Button(sort_frame,
                   text="Apply Sort",
                   command=apply_sort).pack(pady=10)

        # Results area
        self.results_frame = ttk.Frame(self.content_area)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    def show_update_product(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        ttk.Label(self.content_area,
                  text="Update Product",
                  font=('Helvetica', 20, 'bold')).pack(pady=10)

        # Search frame
        search_frame = ttk.Frame(self.content_area)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        # Search type dropdown
        ttk.Label(search_frame, text="Search by:").pack(side=tk.LEFT, padx=5)
        search_type_var = tk.StringVar(value="id")
        search_type_combo = ttk.Combobox(search_frame,
                                         textvariable=search_type_var,
                                         values=["id", "name", "category"],
                                         state="readonly",
                                         width=10)
        search_type_combo.pack(side=tk.LEFT, padx=5)

        # Search entry
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Results frame
        results_frame = ttk.Frame(self.content_area)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create table for results
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity', 'Notes')
        tree = ttk.Treeview(results_frame, columns=columns, show='headings')

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def perform_search():
            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)

            search_type = search_type_var.get()
            search_term = search_var.get()

            if not search_term:
                messagebox.showwarning("Warning", "Please enter a search term")
                return

            # Get products based on search type
            if search_type == "id":
                try:
                    product_id = int(search_term)
                    product = self.inventory_manager.get_product_by_id(product_id)
                    if product:
                        products = [product]
                    else:
                        products = []
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid ID number")
                    return
            else:
                products = self.inventory_manager.search_products(search_term)
                # Filter by the selected field
                if search_type != "name":  # name is already handled by search_products
                    products = [p for p in products if search_term.lower() in str(p[search_type]).lower()]

            if not products:
                messagebox.showinfo("Info", "No products found matching your search")
                return

            # Display results
            for product in products:
                tree.insert('', 'end', values=(
                    product['id'],
                    product['name'],
                    product['category'],
                    f"${product['price']:.2f}",
                    product['quantity'],
                    product['notes'] if product['notes'] else 'N/A'
                ))

        def show_update_form():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a product to update")
                return

            product_id = tree.item(selected_item[0])['values'][0]
            product = self.inventory_manager.get_product_by_id(product_id)

            if not product:
                messagebox.showerror("Error", "Product not found")
                return

            # Create update form
            form_frame = ttk.Frame(self.content_area)
            form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Form fields
            fields = {}

            # Name
            ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
            fields['name'] = ttk.Entry(form_frame, width=30)
            fields['name'].insert(0, product['name'])
            fields['name'].grid(row=0, column=1, padx=5, pady=5)

            # Category
            ttk.Label(form_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
            fields['category'] = ttk.Entry(form_frame, width=30)
            fields['category'].insert(0, product['category'])
            fields['category'].grid(row=1, column=1, padx=5, pady=5)

            # Price
            ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
            fields['price'] = ttk.Entry(form_frame, width=30)
            fields['price'].insert(0, str(product['price']))
            fields['price'].grid(row=2, column=1, padx=5, pady=5)

            # Quantity
            ttk.Label(form_frame, text="Quantity:").grid(row=3, column=0, padx=5, pady=5)
            fields['quantity'] = ttk.Entry(form_frame, width=30)
            fields['quantity'].insert(0, str(product['quantity']))
            fields['quantity'].grid(row=3, column=1, padx=5, pady=5)

            # Notes
            ttk.Label(form_frame, text="Notes:").grid(row=4, column=0, padx=5, pady=5)
            fields['notes'] = tk.Text(form_frame, width=30, height=3)
            fields['notes'].insert('1.0', product['notes'] if product['notes'] else '')
            fields['notes'].grid(row=4, column=1, padx=5, pady=5)

            def update_product():
                try:
                    updates = {
                        'name': fields['name'].get(),
                        'category': fields['category'].get(),
                        'price': float(fields['price'].get()),
                        'quantity': int(fields['quantity'].get()),
                        'notes': fields['notes'].get('1.0', tk.END).strip()
                    }

                    success, message = self.inventory_manager.update_product(product_id, **updates)
                    if success:
                        messagebox.showinfo("Success", "Product updated successfully!")
                        perform_search()  # Refresh the results
                    else:
                        messagebox.showerror("Error", message)
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for price and quantity")

            # Update button
            ttk.Button(form_frame,
                       text="Update Product",
                       command=update_product).grid(row=5, column=0, columnspan=2, pady=10)

        # Search button
        ttk.Button(search_frame,
                   text="Search",
                   command=perform_search).pack(side=tk.LEFT, padx=5)

        # Update button
        ttk.Button(results_frame,
                   text="Update Selected",
                   command=show_update_form).pack(pady=10)

    def show_delete_product(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        ttk.Label(self.content_area,
                  text="Delete Product",
                  font=('Helvetica', 20, 'bold')).pack(pady=10)

        # Search frame
        search_frame = ttk.Frame(self.content_area)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        # Search type dropdown
        ttk.Label(search_frame, text="Search by:").pack(side=tk.LEFT, padx=5)
        search_type_var = tk.StringVar(value="id")
        search_type_combo = ttk.Combobox(search_frame,
                                         textvariable=search_type_var,
                                         values=["id", "name", "category"],
                                         state="readonly",
                                         width=10)
        search_type_combo.pack(side=tk.LEFT, padx=5)

        # Search entry
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Results frame
        results_frame = ttk.Frame(self.content_area)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create table for results
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity', 'Notes')
        tree = ttk.Treeview(results_frame, columns=columns, show='headings')

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def perform_search():
            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)

            search_type = search_type_var.get()
            search_term = search_var.get()

            if not search_term:
                messagebox.showwarning("Warning", "Please enter a search term")
                return

            # Get products based on search type
            if search_type == "id":
                try:
                    product_id = int(search_term)
                    product = self.inventory_manager.get_product_by_id(product_id)
                    if product:
                        products = [product]
                    else:
                        products = []
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid ID number")
                    return
            else:
                products = self.inventory_manager.search_products(search_term)
                # Filter by the selected field
                if search_type != "name":  # name is already handled by search_products
                    products = [p for p in products if search_term.lower() in str(p[search_type]).lower()]

            if not products:
                messagebox.showinfo("Info", "No products found matching your search")
                return

            # Display results
            for product in products:
                tree.insert('', 'end', values=(
                    product['id'],
                    product['name'],
                    product['category'],
                    f"${product['price']:.2f}",
                    product['quantity'],
                    product['notes'] if product['notes'] else 'N/A'
                ))

        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a product to delete")
                return

            product_id = tree.item(selected_item[0])['values'][0]
            product_name = tree.item(selected_item[0])['values'][1]

            if messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete '{product_name}'?"):
                success, message = self.inventory_manager.delete_product(product_id)
                if success:
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    perform_search()  # Refresh the results
                else:
                    messagebox.showerror("Error", message)

        # Search button
        ttk.Button(search_frame,
                   text="Search",
                   command=perform_search).pack(side=tk.LEFT, padx=5)

        # Delete button
        ttk.Button(results_frame,
                   text="Delete Selected",
                   command=delete_selected).pack(pady=10)

    def display_products(self, products):
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Create table
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity', 'Expired Date')
        tree = ttk.Treeview(self.results_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for product in products:
            tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['category'],
                f"${product['price']:.2f}",
                product['quantity'],
                product['expiry_date'] if product['expiry_date'] else 'N/A'
            ))

    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if self.auth_system.login(username, password):
            self.show_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def handle_logout(self):
        self.auth_system.logout()
        self.show_homepage()

    def show_register_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame,
                                text="Create New Account",
                                font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=20)

        # Form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)

        # Username
        ttk.Label(form_frame, text="Username:", font=('Helvetica', 12)).pack()
        self.reg_username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.reg_username_var, width=30)
        username_entry.pack(pady=5)

        # Password
        ttk.Label(form_frame, text="Password:", font=('Helvetica', 12)).pack()
        self.reg_password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.reg_password_var, show="•", width=30)
        password_entry.pack(pady=5)

        # Confirm Password
        ttk.Label(form_frame, text="Confirm Password:", font=('Helvetica', 12)).pack()
        self.reg_confirm_password_var = tk.StringVar()
        confirm_password_entry = ttk.Entry(form_frame, textvariable=self.reg_confirm_password_var, show="•", width=30)
        confirm_password_entry.pack(pady=5)

        # Security Question
        ttk.Label(form_frame, text="Security Question:", font=('Helvetica', 12)).pack()
        self.reg_security_question_var = tk.StringVar()
        security_question_combo = ttk.Combobox(form_frame,
                                               textvariable=self.reg_security_question_var,
                                               values=[
                                                   "What is your mother's maiden name?",
                                                   "What was your first pet's name?",
                                                   "What city were you born in?",
                                                   "What is your favorite book?",
                                                   "What was your first school's name?"
                                               ],
                                               state="readonly",
                                               width=30)
        security_question_combo.pack(pady=5)

        # Security Answer
        ttk.Label(form_frame, text="Security Answer:", font=('Helvetica', 12)).pack()
        self.reg_security_answer_var = tk.StringVar()
        security_answer_entry = ttk.Entry(form_frame, textvariable=self.reg_security_answer_var, width=30)
        security_answer_entry.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="Register",
                   command=self.handle_register).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Back to Home",
                   command=self.show_homepage).pack(side=tk.LEFT, padx=5)

    def handle_register(self):
        username = self.reg_username_var.get().strip()
        password = self.reg_password_var.get()
        confirm_password = self.reg_confirm_password_var.get()
        security_question = self.reg_security_question_var.get()
        security_answer = self.reg_security_answer_var.get().strip()

        # Validate inputs
        if not username or not password or not confirm_password or not security_question or not security_answer:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if len(username) < 4:
            messagebox.showerror("Error", "Username must be at least 4 characters long")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if self.auth_system.register(username, password, security_question, security_answer):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    def show_forget_pass_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame,
                                text="Password Recovery",
                                font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=20)

        # Form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)

        # Username
        ttk.Label(form_frame, text="Username:", font=('Helvetica', 12)).pack()
        self.for_username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.for_username_var, width=30)
        username_entry.pack(pady=5)

        # Security Question
        ttk.Label(form_frame, text="Security Question:", font=('Helvetica', 12)).pack()
        self.for_security_question_var = tk.StringVar()
        security_question_label = ttk.Label(form_frame,
                                            textvariable=self.for_security_question_var,
                                            font=('Helvetica', 12))
        security_question_label.pack(pady=5)

        # Security Answer
        ttk.Label(form_frame, text="Security Answer:", font=('Helvetica', 12)).pack()
        self.for_security_answer_var = tk.StringVar()
        security_answer_entry = ttk.Entry(form_frame, textvariable=self.for_security_answer_var, width=30)
        security_answer_entry.pack(pady=5)

        # New Password
        ttk.Label(form_frame, text="New Password:", font=('Helvetica', 12)).pack()
        self.for_new_password_var = tk.StringVar()
        new_password_entry = ttk.Entry(form_frame, textvariable=self.for_new_password_var, show="•", width=30)
        new_password_entry.pack(pady=5)

        # Confirm New Password
        ttk.Label(form_frame, text="Confirm New Password:", font=('Helvetica', 12)).pack()
        self.for_confirm_password_var = tk.StringVar()
        confirm_password_entry = ttk.Entry(form_frame, textvariable=self.for_confirm_password_var, show="•", width=30)
        confirm_password_entry.pack(pady=5)

        def load_security_question():
            username = self.for_username_var.get().strip()
            if not username:
                messagebox.showwarning("Warning", "Please enter your username")
                return

            security_question = self.auth_system.get_security_question(username)
            if security_question:
                self.for_security_question_var.set(security_question)
            else:
                messagebox.showerror("Error", "Username not found")

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="Load Security Question",
                   command=load_security_question).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Reset Password",
                   command=self.handle_forget_pass).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Back to Homepage",
                   command=self.show_homepage).pack(side=tk.LEFT, padx=5)

    def handle_forget_pass(self):
        username = self.for_username_var.get().strip()
        security_answer = self.for_security_answer_var.get().strip()
        new_password = self.for_new_password_var.get()
        confirm_password = self.for_confirm_password_var.get()

        # Validate inputs
        if not username or not security_answer or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if len(new_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if self.auth_system.reset_password(username, security_answer, new_password):
            messagebox.showinfo("Success", "Password has been reset successfully! Please login with your new password.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Invalid security answer or username not found")

    def show_statistic(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Create scrollable canvas
        canvas = tk.Canvas(self.content_area, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Title
        ttk.Label(scrollable_frame,
                  text="Inventory Statistics",
                  font=self.fonts['title'],
                  background=self.colors['bg']).pack(pady=20)

        # Get current products
        products = self.inventory_manager.get_all_products()

        if not products:
            ttk.Label(scrollable_frame,
                      text="No products available for statistics.",
                      font=self.fonts['normal']).pack(pady=20)
            return

        # Calculate summary statistics
        total_products = len(products)
        total_quantity = sum(p['quantity'] for p in products)
        total_value = sum(p['price'] * p['quantity'] for p in products)

        # Summary Cards Frame
        summary_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        summary_frame.pack(fill=tk.X, padx=30, pady=10)

        # Summary Cards
        summary_data = [
            ("Total Products", total_products, self.colors['primary']),
            ("Total Quantity", total_quantity, self.colors['success']),
            ("Total Value", f"${total_value:,.2f}", self.colors['warning'])
        ]

        for title, value, color in summary_data:
            card = ttk.Frame(summary_frame, style='Card.TFrame')
            card.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

            ttk.Label(card,
                      text=title,
                      font=self.fonts['normal']).pack(pady=5)

            ttk.Label(card,
                      text=str(value),
                      font=self.fonts['title'],
                      foreground=color).pack(pady=5)

        # Prepare data for charts
        # Category distribution
        category_totals = defaultdict(int)
        for p in products:
            category_totals[p['category']] += p['quantity']

        categories = list(category_totals.keys())
        quantities_by_category = list(category_totals.values())

        # Top 5 most stocked items
        sorted_by_quantity = sorted(products, key=lambda x: x['quantity'], reverse=True)[:5]
        top_quantity_names = [p['name'] for p in sorted_by_quantity]
        top_quantity_values = [p['quantity'] for p in sorted_by_quantity]

        # Top 5 most expensive items
        sorted_by_price = sorted(products, key=lambda x: x['price'], reverse=True)[:5]
        top_price_names = [p['name'] for p in sorted_by_price]
        top_price_values = [p['price'] for p in sorted_by_price]

        # Low stock items (quantity < 5)
        low_stock_items = [p for p in products if p['quantity'] < 5]
        low_stock_names = [p['name'] for p in low_stock_items]
        low_stock_values = [p['quantity'] for p in low_stock_items]

        # Create each chart in its own card frame
        # Chart 1: Category Distribution (Pie Chart)
        chart1_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        chart1_frame.pack(fill=tk.X, padx=30, pady=20)

        ttk.Label(chart1_frame,
                  text="Inventory Distribution by Category",
                  font=self.fonts['header']).pack(pady=10)

        fig1, ax1 = plt.subplots(figsize=(10, 7))
        ax1.pie(quantities_by_category, labels=categories, autopct='%1.1f%%', startangle=90,
                shadow=True, explode=[0.05] * len(categories))
        ax1.axis('equal')

        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=chart1_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Chart 2: Top 5 Most Stocked Items
        chart2_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        chart2_frame.pack(fill=tk.X, padx=30, pady=20)

        ttk.Label(chart2_frame,
                  text="Top 5 Most Stocked Items",
                  font=self.fonts['header']).pack(pady=10)

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        bars = ax2.bar(top_quantity_names, top_quantity_values, color='royalblue')
        ax2.set_xlabel('Product')
        ax2.set_ylabel('Quantity')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, linestyle='--', alpha=0.7, axis='y')

        # Add data labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f'{height}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')

        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=chart2_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Chart 3: Top 5 Most Expensive Items
        chart3_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        chart3_frame.pack(fill=tk.X, padx=30, pady=20)

        ttk.Label(chart3_frame,
                  text="Top 5 Most Expensive Items",
                  font=self.fonts['header']).pack(pady=10)

        fig3, ax3 = plt.subplots(figsize=(10, 5))
        bars = ax3.bar(top_price_names, top_price_values, color='forestgreen')
        ax3.set_xlabel('Product')
        ax3.set_ylabel('Price ($)')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, linestyle='--', alpha=0.7, axis='y')

        # Add data labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax3.annotate(f'${height:,.2f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')

        fig3.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=chart3_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Chart 4: Low Stock Items
        chart4_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        chart4_frame.pack(fill=tk.X, padx=30, pady=20)

        ttk.Label(chart4_frame,
                  text="Low Stock Items (Quantity < 5)",
                  font=self.fonts['header']).pack(pady=10)

        if low_stock_items:
            fig4, ax4 = plt.subplots(figsize=(10, 5))
            bars = ax4.bar(low_stock_names, low_stock_values, color='crimson')
            ax4.set_xlabel('Product')
            ax4.set_ylabel('Quantity')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, linestyle='--', alpha=0.7, axis='y')

            # Add data labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                ax4.annotate(f'{height}',
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3),
                             textcoords="offset points",
                             ha='center', va='bottom')

            fig4.tight_layout()
            canvas4 = FigureCanvasTkAgg(fig4, master=chart4_frame)
            canvas4.draw()
            canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        else:
            ttk.Label(chart4_frame,
                      text="No low stock items found.",
                      font=self.fonts['normal']).pack(pady=20)

        # Add download buttons for each chart
        def save_chart_as_png(fig, title):
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title=f"Save {title} as PNG"
            )
            if file_path:
                fig.savefig(file_path, format='png', dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"{title} saved successfully as PNG!")

        # Add download buttons for each chart
        for i, (fig, title) in enumerate([
            (fig1, "Category Distribution"),
            (fig2, "Top Stocked Items"),
            (fig3, "Most Expensive Items"),
            (fig4, "Low Stock Items") if low_stock_items else None
        ]):
            if fig:
                button_frame = ttk.Frame(scrollable_frame)
                button_frame.pack(pady=5)
                ttk.Button(button_frame,
                           text=f"Save {title} as PNG",
                           command=lambda f=fig, t=title: save_chart_as_png(f, t)).pack(pady=5)

        # Add "Save All as PDF" button
        def save_all_charts_pdf():
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save All Charts as PDF"
            )
            if file_path:
                from matplotlib.backends.backend_pdf import PdfPages
                with PdfPages(file_path) as pdf:
                    # Add summary statistics as first page
                    fig_summary, ax_summary = plt.subplots(figsize=(10, 5))
                    ax_summary.axis('off')
                    summary_text = f"Inventory Statistics Summary\n\n" \
                                   f"Total Products: {total_products}\n" \
                                   f"Total Quantity: {total_quantity}\n" \
                                   f"Total Value: ${total_value:,.2f}"
                    ax_summary.text(0.5, 0.5, summary_text,
                                    ha='center', va='center',
                                    fontsize=12, transform=ax_summary.transAxes)
                    pdf.savefig(fig_summary, bbox_inches='tight')
                    plt.close(fig_summary)

                    # Save each chart with its title
                    for fig, title in [
                        (fig1, "Category Distribution"),
                        (fig2, "Top 5 Most Stocked Items"),
                        (fig3, "Top 5 Most Expensive Items"),
                        (fig4, "Low Stock Items") if low_stock_items else None
                    ]:
                        if fig:
                            # Add title to the figure
                            fig.suptitle(title, fontsize=14, y=1.02)
                            pdf.savefig(fig, bbox_inches='tight')
                            plt.close(fig)

                messagebox.showinfo("Success", "All charts saved successfully as PDF!")

        # Add the "Save All as PDF" button
        save_all_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        save_all_frame.pack(fill=tk.X, padx=30, pady=20)

        ttk.Button(save_all_frame,
                   text="Save All Charts as PDF",
                   style='Success.TButton',
                   command=save_all_charts_pdf).pack(pady=10)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Make sure scrolling works with mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def run(self):
        self.root.mainloop()