import sqlite3
from modifyData import *

def update_owner(
    name: str,
    new_allergies: list[str] = None,
    new_can_wash: list[str] = None,
    new_liked_cleaners: list[str] = None,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Verify owner exists
        cursor.execute("SELECT name FROM owner WHERE name = ?;", (name,))
        if not cursor.fetchone():
            print(f"Owner {name} does not exist in the database.")
            return

        if new_allergies is not None:
            # Remove old allergies
            cursor.execute("DELETE FROM IsAllergicTo WHERE owner = ?;", (name,))
            # Add new allergies
            for allergy in new_allergies:
                cursor.execute("INSERT INTO IsAllergicTo (owner, detergent_ingredient) VALUES (?, ?);", (name, allergy))

        if new_can_wash is not None:
            # Remove old wash permissions
            cursor.execute("DELETE FROM OwnerCanWash WHERE washer = ?;", (name,))
            # Add new wash permissions
            for washee in new_can_wash:
                cursor.execute(
                    "INSERT INTO OwnerCanWash (washer, washee) VALUES (?, ?);", (name, washee))

        if new_liked_cleaners is not None:
            # Remove old likes
            cursor.execute("DELETE FROM Likes WHERE owner = ?;", (name,))
            # Add new likes
            for cleaner in new_liked_cleaners:
                cursor.execute(
                    "INSERT INTO Likes (cleaners, owner) VALUES (?, ?);",
                    (cleaner, name)
                )

        print(f"Owner {name} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating owner {name}: {e}")

    cursor.close()
    db.commit()

def update_cleaners(
    address: str,
    new_name: str = None,
    new_supported_systems: list[tuple[str, str, str]] = None,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Verify cleaner exists
        cursor.execute("SELECT address FROM cleaners WHERE address = ?;", (address,))
        if not cursor.fetchone():
            print(f"Cleaner at {address} does not exist in the database.")
            return

        if new_name is not None:
            delete_cleaners(address, db)  # Delete existing cleaner data
            cursor.execute(
                "INSERT OR IGNORE INTO cleaners (address, name) VALUES (?, ?);",
                (address, new_name)
            )  

        if new_supported_systems is not None:
            # Remove old systems
            cursor.execute("DELETE FROM SupportsCleaningSystem WHERE cleaners = ?;", (address,))
            # Add new systems
            for system in new_supported_systems:
                wash_method, detergent, dry_method = system
                cursor.execute(
                    "INSERT OR IGNORE INTO cleaning_system VALUES (?, ?, ?);",
                    (wash_method, detergent, dry_method)
                )
                cursor.execute(
                    "INSERT INTO SupportsCleaningSystem VALUES (?, ?, ?, ?);",
                    (address, wash_method, detergent, dry_method)
                )

        print(f"Cleaner at {address} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating cleaner at {address}: {e}")

    cursor.close()
    db.commit()
    # Removed db.close() to keep the connection open for further operations

def update_laundry(# for front end a while loop whill go through all laundry from owner listed by a query 
    laundry_id: int,
    description: str = None,
    location: str = None,
    special_instructions: str = None,
    dirty: bool = None,
    volume: int = None,
    detergents: list[str] = None,
    color: str = None,
    isDark: bool = False,
    owner: str = None,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    # Update logic
    if description is not None:
        cursor.execute("UPDATE laundry SET description = ? WHERE id = ?;", (description, laundry_id))
    if location is not None:
        cursor.execute("UPDATE laundry SET location = ? WHERE id = ?;", (location, laundry_id))
    if special_instructions is not None:
        cursor.execute("UPDATE laundry SET special_instructions = ? WHERE id = ?;", (special_instructions, laundry_id))
    if dirty is not None:
        cursor.execute("UPDATE laundry SET dirty = ? WHERE id = ?;", (dirty, laundry_id))
    if volume is not None:
        cursor.execute("UPDATE laundry SET volume = ? WHERE id = ?;", (volume, laundry_id))
    if detergents is not None:
        # Clear existing detergents for this laundry item
        cursor.execute("DELETE FROM Deterges WHERE laundry = ?;", (laundry_id,))
        for detergent in detergents:
            cursor.execute("INSERT INTO Deterges VALUES (?, ?);", (laundry_id, detergent))
    if color is not None:
        cursor.execute("INSERT OR REPLACE INTO color VALUES (?, ?);", (color, isDark))        
        cursor.execute("UPDATE IsColor SET color = ? WHERE laundry = ?", (color, laundry_id))
    if owner is not None:
        cursor.execute("UPDATE OwnedBy SET name = ? WHERE id = ?;", (owner, laundry_id))

    cursor.close()
    db.commit()

def update_detergent(
    name: str,
    new_name: str = None,
    new_for_darks: bool = None,
    new_for_lights: bool = None,
    new_whitens: bool = None,
    new_ingredients: list[str] = None,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Verify detergent exists
        cursor.execute("SELECT name FROM detergent WHERE name = ?;", (name,))
        if not cursor.fetchone():
            print(f"Detergent {name} does not exist in the database.")
            return

        # Update main detergent table
        if new_for_darks is not None:
            cursor.execute("UPDATE detergent SET for_darks = ? WHERE name = ?;", (new_for_darks, name))

        if new_for_lights is not None:
            cursor.execute("UPDATE detergent SET for_lights = ? WHERE name = ?;", (new_for_lights, name))
            
        if new_whitens is not None:
            cursor.execute("UPDATE detergent SET whitens = ? WHERE name = ?;", (new_whitens, name))

        if new_name is not None:
            cursor.execute("UPDATE detergent SET name = ? WHERE name = ?;", (new_name, name))
            
        if new_ingredients is not None:
            current_name = new_name if new_name else name
            cursor.execute("DELETE FROM DetergentComposedOf WHERE detergent = ?;", (name,))
            
            for ingredient in new_ingredients:
                cursor.execute("INSERT OR IGNORE INTO detergent_ingredient (name) VALUES (?);", (ingredient,))
                cursor.execute("INSERT INTO DetergentComposedOf (detergent, ingredient) VALUES (?, ?);", (current_name, ingredient))
        
        print(f"Detergent {name} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating detergent {name}: {e}")

    cursor.close()
    db.commit()
    #db.close()

if __name__ == "__main__":

    db = connect_db()

    # update_owner(
    #     name="GARFIELD",
    #     new_allergies=["Grinch", "Lorax"],
    #     new_can_wash=["Anyone but nermal"],
    #     new_liked_cleaners=["John's House"],
    #     db=db
    # )
    # # Update a cleaner
    # update_cleaners(
    #     address="123 G St",
    #     new_name="Grand opening",
    #     new_supported_systems=[["Washing machines","All purpose","Dryers"]],
    #     db = db
    # )
    # # Update a laundry item
    # update_laundry(
    #     laundry_id=30,
    #     description="Designer pants",
    #     location="123 G St",
    #     special_instructions="never wash",
    #     dirty=False,
    #     volume=2,
    #     detergents=[],
    #     color="Solid Purple",
    #     isDark = True,
    #     owner="Odie",
    #     db=db
    #     )

    # # Update a detergent
    # update_detergent(
    #     name="Bad value",
    #     new_name = "better value",
    #     new_for_darks=True,
    #     new_for_lights=True,
    #     new_whitens=True,
    #     new_ingredients=["best enzyme", "best fragrance", "best surfactant"],
    #     db=db
    # )
    delete_owner("German D", db)
    

    db.close()
