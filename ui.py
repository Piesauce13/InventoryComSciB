import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry  # You'll need to install this: pip install tkcalendar
import tkinter.font as tkfont

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
            'primary': '#2c3e50',    # Dark Blue
            'secondary': '#3498db',   # Light Blue
            'success': '#2ecc71',     # Green
            'warning': '#f1c40f',     # Yellow
            'danger': '#e74c3c',      # Red
            'light': '#ecf0f1',       # Light Gray
            'dark': '#2c3e50',        # Dark Blue
            'white': '#ffffff',
            'bg': '#f5f6fa'           # Background
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
        self.show_login_screen()

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
                  text="Register",
                  command=self.show_register_screen).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Forget Password",
                   command=self.show_forget_pass_screen).pack(side=tk.LEFT, padx=5)

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
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity')
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
                product['quantity']
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
        
        # Expiry Date
        ttk.Label(dates_info, text="Expiry Date:").grid(row=1, column=0, padx=5, pady=5)
        fields['expiry_date'] = DateEntry(dates_info, 
                                        width=20, 
                                        background=self.colors['primary'],
                                        foreground=self.colors['white'], 
                                        borderwidth=2,
                                        date_pattern='yyyy-mm-dd',
                                        mindate=datetime.now())  # Must be future date
        fields['expiry_date'].grid(row=1, column=1, padx=5, pady=5)
        
        # Add date validation
        def validate_dates(*args):
            try:
                mfg_date = fields['mfg_date'].get_date()
                exp_date = fields['expiry_date'].get_date()
                
                if mfg_date > datetime.now().date():
                    messagebox.showerror("Error", "Manufacturing date cannot be in the future")
                    fields['mfg_date'].set_date(datetime.now())
                    return False
                
                if exp_date <= mfg_date:
                    messagebox.showerror("Error", "Expiry date must be after manufacturing date")
                    fields['expiry_date'].set_date(mfg_date + timedelta(days=1))
                    return False
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Invalid date format: {str(e)}")
                return False

        # Bind validation to date changes
        fields['mfg_date'].bind("<<DateEntrySelected>>", validate_dates)
        fields['expiry_date'].bind("<<DateEntrySelected>>", validate_dates)
        
        # Additional Information Section
        additional_info = ttk.LabelFrame(form_frame, text="Additional Information", padding=10)
        additional_info.pack(fill=tk.X, padx=10, pady=5)
        
        # Notes
        ttk.Label(additional_info, text="Notes:").pack(anchor='w', padx=5, pady=5)
        fields['notes'] = tk.Text(additional_info, height=4, width=50)
        fields['notes'].pack(padx=5, pady=5, fill=tk.X)
        
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
                    'expiry_date': fields['expiry_date'].get_date().strftime('%Y-%m-%d'),
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
                  command=lambda: [field.delete(0, tk.END) for field in fields.values() if isinstance(field, ttk.Entry)]
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
        columns = ('ID', 'Name', 'Category', 'Expiry Date')
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
                product['expiry_date']
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
        
        # Product selection frame
        select_frame = ttk.Frame(self.content_area)
        select_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(select_frame, text="Product ID:").pack(side=tk.LEFT, padx=5)
        id_var = tk.StringVar()
        id_entry = ttk.Entry(select_frame, textvariable=id_var, width=10)
        id_entry.pack(side=tk.LEFT, padx=5)
        
        def load_product():
            try:
                product_id = int(id_var.get())
                product = self.inventory_manager.get_product_by_id(product_id)
                if product:
                    show_update_form(product)
                else:
                    messagebox.showerror("Error", "Product not found")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid product ID")
        
        ttk.Button(select_frame,
                  text="Load Product",
                  command=load_product).pack(side=tk.LEFT, padx=5)
        
        # Update form container
        self.update_form_frame = ttk.Frame(self.content_area)
        self.update_form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def show_update_form(product):
            # Clear previous form
            for widget in self.update_form_frame.winfo_children():
                widget.destroy()
            
            # Create form fields
            fields = {}
            
            # Name
            ttk.Label(self.update_form_frame, text="Name:").pack(anchor='w')
            fields['name'] = ttk.Entry(self.update_form_frame, width=30)
            fields['name'].insert(0, product['name'])
            fields['name'].pack(pady=5)
            
            # Category
            ttk.Label(self.update_form_frame, text="Category:").pack(anchor='w')
            fields['category'] = ttk.Entry(self.update_form_frame, width=30)
            fields['category'].insert(0, product['category'])
            fields['category'].pack(pady=5)
            
            # Price
            ttk.Label(self.update_form_frame, text="Price:").pack(anchor='w')
            fields['price'] = ttk.Entry(self.update_form_frame, width=30)
            fields['price'].insert(0, str(product['price']))
            fields['price'].pack(pady=5)
            
            # Quantity
            ttk.Label(self.update_form_frame, text="Quantity:").pack(anchor='w')
            fields['quantity'] = ttk.Entry(self.update_form_frame, width=30)
            fields['quantity'].insert(0, str(product['quantity']))
            fields['quantity'].pack(pady=5)
            
            def update_product():
                try:
                    updates = {
                        'name': fields['name'].get(),
                        'category': fields['category'].get(),
                        'price': float(fields['price'].get()),
                        'quantity': int(fields['quantity'].get())
                    }
                    
                    success, message = self.inventory_manager.update_product(product['id'], **updates)
                    if success:
                        messagebox.showinfo("Success", "Product updated successfully!")
                        self.show_products()
                    else:
                        messagebox.showerror("Error", message)
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for price and quantity")
            
            ttk.Button(self.update_form_frame,
                      text="Update Product",
                      command=update_product).pack(pady=20)

    def show_delete_product(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        ttk.Label(self.content_area,
                 text="Delete Product",
                 font=('Helvetica', 20, 'bold')).pack(pady=10)
        
        # Delete frame
        delete_frame = ttk.Frame(self.content_area)
        delete_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(delete_frame, text="Product ID:").pack(side=tk.LEFT, padx=5)
        id_var = tk.StringVar()
        id_entry = ttk.Entry(delete_frame, textvariable=id_var, width=10)
        id_entry.pack(side=tk.LEFT, padx=5)
        
        def delete_product():
            try:
                product_id = int(id_var.get())
                if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
                    success, message = self.inventory_manager.delete_product(product_id)
                    if success:
                        messagebox.showinfo("Success", "Product deleted successfully!")
                        self.show_products()
                    else:
                        messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid product ID")
        
        ttk.Button(delete_frame,
                  text="Delete Product",
                  command=delete_product).pack(side=tk.LEFT, padx=5)

    def display_products(self, products):
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Create table
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity')
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
                product['quantity']
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
        self.show_login_screen()

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
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame,
                  text="Register",
                  command=self.handle_register).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame,
                  text="Back to Login",
                  command=self.show_login_screen).pack(side=tk.LEFT, padx=5)

    def handle_register(self):
        username = self.reg_username_var.get()
        password = self.reg_password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.auth_system.register(username, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    def handle_forget_pass(self):
        userid = self.for_id_var.get()
        username = self.for_username_var.get()
        role = self.for_role_var.get()
        new_password1 = self.new_for_password1_var.get()
        new_password2 = self.new_for_password2_var.get()

        if not (userid and username and role and new_password1 and new_password2):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # print("change", self.auth_system.forget_password(userid, username, role, new_password))
        if new_password1 == new_password2 and self.auth_system.forget_password(userid, username, role, new_password1):
            messagebox.showinfo("Success", "Password change successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Invalid info.")

    def show_forget_pass_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame,
                                text="Forget Password",
                                font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=20)

        # Form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)

        #ID
        ttk.Label(form_frame, text="ID:", font=('Helvetica', 12)).pack()
        self.for_id_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.for_id_var, width=30)
        username_entry.pack(pady=5)

        # Username
        ttk.Label(form_frame, text="Username:", font=('Helvetica', 12)).pack()
        self.for_username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.for_username_var, width=30)
        username_entry.pack(pady=5)

        # Role
        ttk.Label(form_frame, text="Role:", font=('Helvetica', 12)).pack()
        self.for_role_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.for_role_var, width=30)
        password_entry.pack(pady=5)

        # New Password1
        ttk.Label(form_frame, text="New Password:", font=('Helvetica', 12)).pack()
        self.new_for_password1_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.new_for_password1_var, show="•", width=30)
        password_entry.pack(pady=5)

        # New Password2
        ttk.Label(form_frame, text="New Password:", font=('Helvetica', 12)).pack()
        self.new_for_password2_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.new_for_password2_var, show="•", width=30)
        password_entry.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="Change",
                   command=self.handle_forget_pass).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="Back to Login",
                   command=self.show_login_screen).pack(side=tk.LEFT, padx=5)


    def run(self):
        self.root.mainloop()