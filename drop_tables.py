from db_manager import DBManager

# Create an instance of DBManager
db_manager = DBManager("database.db")

# Call the clear_tables method to clear all tables in the database
db_manager.drop_all_tables()

print("All tables have been dropped.")