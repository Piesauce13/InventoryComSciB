from database import Database
from auth import AuthSystem
from inventory import InventoryManager
from ui import InventoryUI
from generate_data import generate_sample_data

def main():

    """Main application entry point"""
    try:
        # Initialize database
        db = Database()
        # db.clear_products_for_new_user()
        generate_sample_data()
        
        # Initialize systems
        auth_system = AuthSystem(db)
        inventory_manager = InventoryManager(db)
        # generate_sample_data()
        
        # Initialize user interface
        ui = InventoryUI(auth_system, inventory_manager)
        
        # Run the application
        ui.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close database connection
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()