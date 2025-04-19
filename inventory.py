import sqlite3
from datetime import datetime

class InventoryManager:
    def __init__(self, db):
        self.db = db

    def add_product(self, name, category, price, quantity, expiry_date=None, mfg_date=None, min_stock_level=5, notes=None):
        """Add a new product to inventory"""
        try:
            # Validate inputs
            if price < 0 or quantity < 0:
                return False, "Price and quantity must be non-negative"
                
            cursor = self.db.conn.cursor()
            cursor.execute('''
            INSERT INTO products (
                name, 
                category, 
                price, 
                quantity, 
                expiry_date, 
                mfg_date,
                min_stock_level,
                notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, category, price, quantity, expiry_date, mfg_date, min_stock_level, notes))
            self.db.conn.commit()
            return True, "Product added successfully"
        except Exception as e:
            return False, f"Error adding product: {e}"

    def update_product(self, product_id, **kwargs):
        """Update an existing product"""
        try:
            if not kwargs:
                return False, "No updates provided"

            # Validate inputs
            if 'price' in kwargs and kwargs['price'] < 0:
                return False, "Price must be non-negative"
            if 'quantity' in kwargs and kwargs['quantity'] < 0:
                return False, "Quantity must be non-negative"

            set_clause = ', '.join(f"{k} = ?" for k in kwargs)
            values = list(kwargs.values())
            values.append(product_id)

            cursor = self.db.conn.cursor()
            cursor.execute(f'''
            UPDATE products 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', values)
            self.db.conn.commit()
            
            if cursor.rowcount > 0:
                return True, "Product updated successfully"
            else:
                return False, "Product not found"
        except Exception as e:
            return False, f"Error updating product: {e}"

    def delete_product(self, product_id):
        """Delete a product from inventory"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            self.db.conn.commit()
            
            if cursor.rowcount > 0:
                return True, "Product deleted successfully"
            else:
                return False, "Product not found"
        except Exception as e:
            return False, f"Error deleting product: {e}"

    def get_product_by_id(self, product_id):
        """Get a single product by ID"""
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        return dict(product) if product else None

    def get_all_products(self):
        """Get all products in inventory"""
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM products')
        return [dict(row) for row in cursor.fetchall()]

    def search_products(self, query):
        """Search products by name or category"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
        SELECT * FROM products 
        WHERE name LIKE ? OR category LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]

    def get_products_sorted(self, sort_by='name', ascending=True):
        """Get products sorted by a specific field"""
        valid_sorts = ['name', 'category', 'price', 'quantity', 'expiry_date']
        if sort_by not in valid_sorts:
            raise ValueError(f"Invalid sort field. Use one of: {valid_sorts}")

        cursor = self.db.conn.cursor()
        cursor.execute(f'''
        SELECT * FROM products 
        ORDER BY {sort_by} {'ASC' if ascending else 'DESC'}
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def get_low_stock_products(self):
        """Get products with stock level below minimum threshold"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
        SELECT * FROM products 
        WHERE quantity < min_stock_level
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def get_expired_products(self, current_date=None):
        """Get expired products"""
        if current_date is None:
            current_date = datetime.now().strftime('%Y-%m-%d')
            
        cursor = self.db.conn.cursor()
        cursor.execute('''
        SELECT * FROM products 
        WHERE expiry_date IS NOT NULL AND expiry_date < ?
        ''', (current_date,))
        return [dict(row) for row in cursor.fetchall()]