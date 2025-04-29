import random
from datetime import datetime, timedelta
from database import Database
from inventory import InventoryManager
from auth import AuthSystem

def generate_sample_data():
    """Generate sample data for the inventory management system"""
    print("Generating sample data...")
    
    # Initialize database
    db = Database()
    auth_system = AuthSystem(db)
    inventory_manager = InventoryManager(db)
    
    # Create admin and regular user if they don't exist
    auth_system.register("admin", "admin123", "admin")
    auth_system.register("user", "password", "regular")
    
    # Product categories
    categories = [
        "Electronics", "Food", "Clothing", "Books", "Office Supplies",
        "Household", "Tools", "Toys", "Sports", "Beauty"
    ]
    
    # Product names by category
    product_names = {
        "Electronics": [
            "Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch",
            "Bluetooth Speaker", "Power Bank", "USB Drive", "Keyboard", "Mouse"
        ],
        "Food": [
            "Pasta", "Rice", "Cereal", "Canned Soup", "Coffee",
            "Tea", "Chocolate", "Biscuits", "Milk", "Juice"
        ],
        "Clothing": [
            "T-Shirt", "Jeans", "Sweater", "Hoodie", "Jacket",
            "Socks", "Gloves", "Hat", "Scarf", "Shoes"
        ],
        "Books": [
            "Novel", "Textbook", "Cookbook", "Magazine", "Dictionary",
            "Children's Book", "Biography", "Self-Help", "History Book", "Comic Book"
        ],
        "Office Supplies": [
            "Pen", "Notebook", "Stapler", "Paper Clips", "Sticky Notes",
            "Calendar", "Binder", "Scissors", "Tape", "Printer Paper"
        ],
        "Household": [
            "Detergent", "Soap", "Towel", "Blanket", "Pillow",
            "Light Bulb", "Air Freshener", "Paper Towels", "Trash Bags", "Dishwasher Tabs"
        ],
        "Tools": [
            "Hammer", "Screwdriver", "Wrench", "Drill", "Saw",
            "Pliers", "Tape Measure", "Level", "Utility Knife", "Flashlight"
        ],
        "Toys": [
            "Action Figure", "Board Game", "Puzzle", "Doll", "RC Car",
            "Building Blocks", "Stuffed Animal", "Card Game", "Yo-Yo", "Toy Car"
        ],
        "Sports": [
            "Basketball", "Soccer Ball", "Tennis Racket", "Baseball Bat", "Yoga Mat",
            "Dumbbells", "Jump Rope", "Helmet", "Swimming Goggles", "Running Shoes"
        ],
        "Beauty": [
            "Shampoo", "Conditioner", "Body Wash", "Lotion", "Face Cream",
            "Lipstick", "Mascara", "Nail Polish", "Perfume", "Sunscreen"
        ]
    }
    
    # Get current date
    today = datetime.now()
    start_of_year = datetime(today.year, 1, 1)
    
    # Create 100 sample products
    products_added = 0
    for _ in range(100):
        # Select random category
        category = random.choice(categories)
        
        # Select random product name from that category
        name = random.choice(product_names[category])
        
        # Add variations to make names unique
        variations = ["Premium", "Basic", "Pro", "Ultra", "Mini", "Max", "Plus", "Standard", "Classic", "Deluxe"]
        brands = ["TechCo", "HomeStyle", "GoodLife", "EcoFriendly", "SuperValue", "PrimeBrand", "QualityPlus", "BestChoice", "SmartBuy", "ValuePick"]
        
        # Randomize product name with brand and variation
        if random.random() > 0.3:  # 70% chance to have a brand
            brand = random.choice(brands)
            name = f"{brand} {name}"
        
        if random.random() > 0.5:  # 50% chance to have a variation
            variation = random.choice(variations)
            name = f"{name} {variation}"
        
        # Generate random price between $1.99 and $999.99
        price = round(random.uniform(1.99, 999.99), 2)
        
        # Generate random quantity between 0 and 100 (some will be low stock)
        quantity = random.randint(0, 100)
        
        # Set min stock level between 5 and 20
        min_stock_level = random.randint(5, 20)
        
        # Generate manufacturing date (between start of current year and today)
        mfg_date = (start_of_year + timedelta(days=random.randint(0, (today - start_of_year).days))).strftime('%Y-%m-%d')
        
        # Determine if product has expiry date (food and some others have expiry)
        has_expiry = category in ["Food", "Beauty"] or random.random() > 0.7
        
        # Generate expiry date (future for non-expired, past for some expired)
        if has_expiry:
            if random.random() > 0.8:  # 20% chance product is expired
                expiry_days = random.randint(-100, -1)  # Expired up to 100 days ago
            else:
                expiry_days = random.randint(30, 730)  # Expires in 30 days to 2 years
                
            expiry_date = (today + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
        else:
            expiry_date = None
        
        # Generate some sample notes
        notes_options = [
            f"Restocked on {(today - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')}",
            "Popular item",
            "Seasonal item",
            "New product",
            "Customer favorite",
            "Limited edition",
            "Clearance item",
            "Frequent reorder item",
            None  # Some items have no notes
        ]
        notes = random.choice(notes_options)
        
        # Add the product to the database
        success, message = inventory_manager.add_product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            expiry_date=expiry_date,
            mfg_date=mfg_date,
            min_stock_level=min_stock_level,
            notes=notes
        )
        
        if success:
            products_added += 1
            print(f"Added product: {name} ({category}) - Qty: {quantity}, Price: ${price:.2f}")
        else:
            print(f"Failed to add product {name}: {message}")
    
    print(f"\nSuccessfully added {products_added} sample products to the database.")
    print("Sample users created:")
    print("  Username: admin, Password: admin123 (Admin role)")
    print("  Username: user, Password: password (Regular role)")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    generate_sample_data()
