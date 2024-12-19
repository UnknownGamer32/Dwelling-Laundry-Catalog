import sqlite3

def connect_db():
    conn = sqlite3.connect("Checkpoint2-dbase.sqlite3")
    return conn

def insert_owner(
    name: str,
    allergies: list[str] = [],
    can_wash: list[str] = [],
    liked_cleaners: list[str] = [],
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO owner VALUES (?);", (name,))
    except sqlite3.IntegrityError:
        print(f"Owner {name} already exists in the database.")
        db.rollback() 

    if allergies:
        for allergy in allergies:
            try:
                # First ensure the ingredient exists
                cursor.execute(
                    "INSERT OR IGNORE INTO detergent_ingredient VALUES (?);", 
                    (allergy,)
                )
                # Then create the allergy relationship
                cursor.execute(
                    "INSERT INTO IsAllergicTo VALUES (?, ?);",
                    (name, allergy)
                )
            except sqlite3.IntegrityError:
                print(f"Allergy {allergy} already recorded for {name}")
                db.rollback()

    if can_wash:
        for washee in can_wash:
            try:
                cursor.execute(
                    "INSERT INTO OwnerCanWash VALUES (?, ?);",
                    (name, washee)
                )
            except sqlite3.IntegrityError:
                print(f"Wash permission {name}->{washee} already exists")
                db.rollback()

    if liked_cleaners:
        for cleaner in liked_cleaners:
            try:
                cursor.execute(
                    "INSERT INTO Likes VALUES (?, ?);",
                    (cleaner, name)
                )
            except sqlite3.IntegrityError:
                print(f"Like relationship {name}->{cleaner} already exists")
                db.rollback()

    cursor.close()
    db.commit()
    #db.close()

def insert_cleaners(
    address: str,
    name: str,
    supported_systems: list[tuple[str, str, str]] = [],  # List of (wash_method, detergent, dry_method)
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO cleaners VALUES (?, ?);",
            (address, name)
        )
    except sqlite3.IntegrityError:
        print(f"Cleaner at address {address} already exists in the database.")
        db.rollback() 

    if supported_systems:
        for system in supported_systems:
            wash_method, detergent, dry_method = system
            try:
                # First ensure the cleaning system exists
                cursor.execute(
                    "INSERT OR IGNORE INTO cleaning_system VALUES (?, ?, ?);",
                    (wash_method, detergent, dry_method)
                )
                # Then create the support relationship
                cursor.execute(
                    "INSERT INTO SupportsCleaningSystem VALUES (?, ?, ?, ?);",
                    (address, wash_method, detergent, dry_method)
                )
            except sqlite3.IntegrityError:
                print(f"System support {address}->{system} already exists")
                db.rollback()

    cursor.close()
    db.commit()
    #db.close()

def insert_laundry(
    owner: str,
    description: str,
    location: str = "",
    special_instructions: str = "",
    dirty: bool = False,
    volume: int = 0,
    detergents: list[str] = [],
    color: str = "",
    isDark: bool = False,
    db: sqlite3.Connection = connect_db(),
) -> None:
    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) FROM laundry;")
    laundry_id = cursor.fetchone()[0]
    if laundry_id is None:
        laundry_id = 1
    else:
        laundry_id += 1

    cursor.execute(
        "INSERT INTO laundry VALUES (?, ?, ?, ?, ?, ?);",
        (laundry_id, description, location, special_instructions, dirty, volume),
    )

    if detergents:
        for detergent in detergents:
            cursor.execute(
                "INSERT OR IGNORE INTO Deterges VALUES (?, ?);", (laundry_id, detergent)
            )

    if color:
        cursor.execute("INSERT OR REPLACE INTO color VALUES (?, ?);", (color, isDark))
        cursor.execute("INSERT OR REPLACE INTO IsColor VALUES (?, ?);", (color, laundry_id))

    if owner:
        cursor.execute("INSERT INTO OwnedBy VALUES (?, ?);", (owner, laundry_id))

    cursor.close()
    db.commit()
    #db.close()


def insert_detergent(
    name: str,
    for_darks: bool,
    for_whites: bool,
    whitens: bool,
    ingredients: list[str],
    db: sqlite3.Connection = connect_db(),
) -> None:
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO detergent VALUES (?, ?, ?, ?);",
            (name, for_darks, for_whites, whitens),
        )
    except sqlite3.IntegrityError:
        print(f"Detergent {name} already exists in the database.")
        db.rollback()

    if ingredients:
        for ingredient in ingredients:
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO detergent_ingredient VALUES (?);", (ingredient,)
                )
                cursor.execute(
                    "INSERT INTO DetergentComposedOf VALUES (?, ?);", (name, ingredient)
                )
            except sqlite3.IntegrityError:
                print(f"Ingredient {ingredient} already exists in the database.")
                db.rollback()

    cursor.close()
    db.commit()
    #db.close()
    
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
        db.rollback()

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
        db.rollback()

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
        db.rollback()

    cursor.close()
    db.commit()
    #db.close() 

def delete_owner(
    name: str,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Delete from related tables first due to foreign key constraints
        cursor.execute("DELETE FROM IsAllergicTo WHERE owner = ?;", (name,))
        cursor.execute("DELETE FROM OwnerCanWash WHERE washer = ? OR washee = ?;", (name, name))
        cursor.execute("DELETE FROM Likes WHERE owner = ?;", (name,))
        cursor.execute("DELETE FROM laundry WHERE id IN (SELECT id FROM OwnedBy WHERE name = ?);", (name,))
        cursor.execute("DELETE FROM isColor WHERE laundry IN (SELECT id FROM OwnedBy WHERE name = ?);", (name,))
        cursor.execute("DELETE FROM OwnedBy WHERE name = ?;", (name,))
        # Finally delete the owner
        cursor.execute("DELETE FROM owner WHERE name = ?;", (name,))
        print(f"Owner {name} and related data deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting owner {name}: {e}")
        db.rollback()

    cursor.close()
    db.commit()
    #db.close()

def delete_cleaners(
    address: str,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Delete from related tables first
        cursor.execute("DELETE FROM SupportsCleaningSystem WHERE cleaners = ?;", (address,))
        cursor.execute("DELETE FROM Likes WHERE cleaners = ?;", (address,))
        # Delete the cleaner
        cursor.execute("DELETE FROM cleaners WHERE address = ?;", (address,))
        print(f"Cleaner at {address} and related data deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting cleaner at {address}: {e}")
        db.rollback()

    cursor.close()
    db.commit()
    #db.close()

def delete_laundry(
    laundry_id: int,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Delete from related tables first
        cursor.execute("DELETE FROM Deterges WHERE laundry = ?;", (laundry_id,))
        cursor.execute("DELETE FROM IsColor WHERE laundry = ?;", (laundry_id,))
        cursor.execute("DELETE FROM OwnedBy WHERE id = ?;", (laundry_id,))
        cursor.execute("DELETE FROM CleanedBy WHERE laundry = ?;", (laundry_id,))
        # Delete the laundry item
        cursor.execute("DELETE FROM laundry WHERE id = ?;", (laundry_id,))
        print(f"Laundry item {laundry_id} and related data deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting laundry item {laundry_id}: {e}")
        db.rollback()

    cursor.close()
    db.commit()
    #db.close()

def delete_detergent(
    name: str,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Delete from related tables first
        cursor.execute("DELETE FROM DetergentComposedOf WHERE detergent = ?;", (name,))
        cursor.execute("DELETE FROM Deterges WHERE detergent = ?;", (name,))
        cursor.execute("DELETE FROM cleaning_system WHERE detergent = ?;", (name,))
        # Delete the detergent
        cursor.execute("DELETE FROM detergent WHERE name = ?;", (name,))
        print(f"Detergent {name} and related data deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting detergent {name}: {e}")
        db.rollback()

    cursor.close()
    db.commit()
    #db.close()
