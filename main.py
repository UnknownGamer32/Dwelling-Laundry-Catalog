import sqlite3
from modifyData import *
from viewQuery import *
from insert_data import do_laundry

# prompts user for name until name is found in database
def get_username(db: sqlite3.Connection) -> str:
    cursor = db.cursor()
    cursor.execute("SELECT name FROM owner;")
    owners = cursor.fetchall()
    for owner in owners:
        print(owner[0])
    username = str(input("Enter your name: "))
    if username in [owner[0] for owner in owners]:
        return username
    print("Name not found. Please try again.")
    return get_username(db)

def get_menu_option(db: sqlite3.Connection) -> int:
    print("1. Do Laundry")
    print("2. Mark things as dirty")
    print("3. Edit")
    print("4. Exit")
    option = input("Select an option: ")
    # check if input is a number
    if not option.isdigit():
        print("Invalid option. Please try again.")
        return get_menu_option(db)
    int_option = int(option)
    if int_option < 1 or int_option > 4:
        print("Invalid option. Please try again.")
        return get_menu_option(db)
    return int_option

def open_dirty_menu(db: sqlite3.Connection, username: str) -> None:
    cursor = db.cursor()

    # get all laundry in ownedby table where name = username
    laundry_ids = cursor.execute("SELECT id FROM OwnedBy WHERE name = ?;", (username,)).fetchall()
    laundry = cursor.execute("SELECT * FROM laundry WHERE id IN ({});".format(", ".join([str(laundry_id[0]) for laundry_id in laundry_ids]))).fetchall()
    
    ids: list[int] = []
    all_laundry_dirty = True
    for item in laundry:
        if not int(item[4]):
            all_laundry_dirty = False
        ids.append(item[0])
        print(f"ID: {item[0]}, Description: {item[1]} - {('DIRTY' if int(item[4]) else 'CLEAN')}")
    
    if all_laundry_dirty:
        print("All laundry is dirty.")
        return

    dirty_id = input("Enter the ID of the item you want to mark as dirty (Enter -1 to exit): ")
    if dirty_id == "-1":
        return
    if dirty_id.isdigit() and int(dirty_id) not in ids:
        print("Invalid ID. Please try again.")
        return open_dirty_menu(db, username)

    cursor = db.cursor()
    cursor.execute("UPDATE laundry SET dirty = 1 WHERE id = ?;", (dirty_id,))
    db.commit()
    print(f"Item {dirty_id} marked as dirty.")
    open_dirty_menu(db, username)

def edit_laundry_menu(db, username):
    cursor = db.cursor()
    laundry_ids = cursor.execute("SELECT id FROM OwnedBy WHERE name = ?;", (username,)).fetchall()
    laundry = cursor.execute("SELECT * FROM laundry WHERE id IN ({});".format(", ".join([str(laundry_id[0]) for laundry_id in laundry_ids]))).fetchall()

    ids = []
    print("\nYour Laundry Items:")
    for item in laundry:
        ids.append(item[0])
        print(f"ID: {item[0]}, Description: {item[1]}, Location: {item[2]}, "
              f"Special Instructions: {item[3]}, Volume: {item[5]}, "
              f"Status: {'DIRTY' if int(item[4]) else 'CLEAN'}")
    
    # Prompt user to select an item to edit
    selected_id = input("\nEnter the ID of the item you want to edit (Enter -1 to exit): ")
    if selected_id == "-1":
        return
    if not selected_id.isdigit() or int(selected_id) not in ids:
        print("Invalid ID. Please try again.")
        return edit_laundry_menu(db, username)
    
    # Gather new values for the selected laundry item
    selected_id = int(selected_id)
    print("\nWhat would you like to do with this laundry item?")
    print("1. Edit")
    print("2. Delete")
    print("3. Cancel")
    choice = input("Enter your choice (1/2/3): ").strip()


    if choice == "1":
        print("\nEnter new values or press Enter to keep the current value:")
        new_description = input("New Description: ")
        new_location = input("New Location: ")
        new_special_instructions = input("New Special Instructions: ")
        new_dirty_status = input("Is it Dirty? (yes/no): ").strip().lower()
        new_volume = input("New Volume: ")
    
        # Convert inputs into valid values
        dirty = True if new_dirty_status == "yes" else False if new_dirty_status == "no" else None
        volume = int(new_volume) if new_volume.isdigit() else None

        # Call update_laundry function with provided inputs
        update_laundry(
            laundry_id=selected_id,
            description=new_description if new_description else None,
            location=new_location if new_location else None,
            special_instructions=new_special_instructions if new_special_instructions else None,
            dirty=dirty,
            volume=volume,
            db=db
        )
    
        print(f"\nLaundry item {selected_id} updated successfully.")

    elif choice == "2":
        # Proceed with deleting the laundry item
        confirm = input(
            f"Are you sure you want to delete laundry item {selected_id}? (yes/no): "
        ).strip().lower()
        if confirm == "yes":
            delete_laundry(selected_id, db)  # Assuming delete_laundry is implemented
            print(f"\nLaundry item {selected_id} deleted successfully.")
        else:
            print("Deletion canceled.")

    elif choice == "3":
        # Cancel the operation
        print("Operation canceled.")
        return edit_laundry_menu(db, username)
    
    # Ask user if they want to edit another item
    edit_again = input("\nDo you want to edit another laundry item? (yes/no): ").strip().lower()
    if edit_again == "yes":
        return edit_laundry_menu(db, username)


def edit_detergent_menu(db):
    cursor = db.cursor()

    detergents = cursor.execute("SELECT * FROM detergent;").fetchall()
    if not detergents:
        print("No detergents found in the database.")
        return

    print("\nDetergents Available:")
    for detergent in detergents:
        print(f"Name: {detergent[0]}, For Darks: {bool(detergent[1])}, "
              f"For Lights: {bool(detergent[2])}, Whitens: {bool(detergent[3])}")

    # Prompt user to select a detergent by name
    selected_name = input("\nEnter the name of the detergent you want to edit (Enter -1 to exit): ")
    if selected_name == "-1":
        return
    if selected_name not in [detergent[0] for detergent in detergents]:
        print("Invalid name. Please try again.")
        return edit_detergent_menu(db)
    
    print(f"\nWhat would you like to do with the '{selected_name}' detergent?")
    print("1. Edit")
    print("2. Delete")
    print("3. Cancel")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        # Gather new values for the selected detergent
        print("\nEnter new values or press Enter to keep the current value:")
        new_name = input("New Name: ")
        new_for_darks = input("For Darks (yes/no): ").strip().lower()
        new_for_lights = input("For Lights (yes/no): ").strip().lower()
        new_whitens = input("Whitens (yes/no): ").strip().lower()

        # Convert boolean inputs
        for_darks = True if new_for_darks == "yes" else False if new_for_darks == "no" else None
        for_lights = True if new_for_lights == "yes" else False if new_for_lights == "no" else None
        whitens = True if new_whitens == "yes" else False if new_whitens == "no" else None

        # Prompt user to update ingredients
        update_ingredients = input("Do you want to update the ingredients? (yes/no): ").strip().lower()
        new_ingredients = []
        if update_ingredients == "yes":
            print("Enter new ingredients (type 'done' to finish):")
            while True:
                ingredient = input("Ingredient: ").strip()
                if ingredient.lower() == "done":
                    break
                if ingredient:
                    new_ingredients.append(ingredient)

        # Call update_detergent function with provided inputs
        update_detergent(
            name=selected_name,
            new_name=new_name if new_name else None,
            new_for_darks=for_darks,
            new_for_lights=for_lights,
            new_whitens=whitens,
            new_ingredients=new_ingredients if update_ingredients == "yes" else None,
            db=db
        )
    
    elif choice == "2":
        # Proceed with deleting the laundry item
        confirm = input(
            f"Are you sure you want to delete laundry item {selected_name}? (yes/no): "
        ).strip().lower()
        if confirm == "yes":
            delete_detergent(selected_name, db)  
            print(f"\nDetergent item {selected_name} deleted successfully.")
        else:
            print("Deletion canceled.")

    elif choice == "3":
        # Cancel the operation
        print("Operation canceled.")
        return edit_detergent_menu(db)

    # Ask user if they want to edit another detergent
    edit_again = input("\nDo you want to edit another detergent? (yes/no): ").strip().lower()
    if edit_again == "yes":
        return edit_detergent_menu(db)
    
def edit_user_menu(db, username):
    cursor = db.cursor()

    # Display existing details for the selected owner
    allergies = cursor.execute(
        "SELECT detergent_ingredient FROM IsAllergicTo WHERE owner = ?;", (username,)
    ).fetchall()
    can_wash = cursor.execute(
        "SELECT washee FROM OwnerCanWash WHERE washer = ?;", (username,)
    ).fetchall()
    liked_cleaners = cursor.execute(
        "SELECT cleaners FROM Likes WHERE owner = ?;", (username,)
    ).fetchall()

    print(f"\nDetails for {username}:")
    print(f"Allergies: {[a[0] for a in allergies]}")
    print(f"Can Wash For: {[w[0] for w in can_wash]}")
    print(f"Liked Cleaners: {[c[0] for c in liked_cleaners]}")

    print("\nWhat would you like to do?")
    print("1. Edit")
    print("2. Delete my account")
    print("3. Return")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        # Gather new values for the owner
        update_allergies = input("\nDo you want to update allergies? (yes/no): ").strip().lower()
        new_allergies = []
        if update_allergies == "yes":
            print("Enter new allergies (type 'done' to finish):")
            while True:
                allergy = input("Allergy: ").strip()
                if allergy.lower() == "done":
                    break
                if allergy:
                    new_allergies.append(allergy)

        update_can_wash = input("\nDo you want to update who they can wash for? (yes/no): ").strip().lower()
        new_can_wash = []
        if update_can_wash == "yes":
            print("Enter names of people they can wash for (type 'done' to finish):")
            while True:
                washee = input("Can wash for: ").strip()
                if washee.lower() == "done":
                    break
                if washee:
                    new_can_wash.append(washee)

        update_liked_cleaners = input("\nDo you want to update liked cleaners? (yes/no): ").strip().lower()
        new_liked_cleaners = []
        if update_liked_cleaners == "yes":
            print("Enter names of cleaners they like (type 'done' to finish):")
            while True:
                cleaner = input("Cleaner: ").strip()
                if cleaner.lower() == "done":
                    break
                if cleaner:
                    new_liked_cleaners.append(cleaner)

        # Call update_owner function with provided inputs
        update_owner(
            name=username,
            new_allergies=new_allergies if update_allergies == "yes" else None,
            new_can_wash=new_can_wash if update_can_wash == "yes" else None,
            new_liked_cleaners=new_liked_cleaners if update_liked_cleaners == "yes" else None,
            db=db
        )

    elif choice == "2":
        # Proceed with deleting the laundry item
        confirm = input(
            f"Are you sure you want to delete data for {username}? (yes/no): "
        ).strip().lower()
        if confirm == "yes":
            delete_owner(username, db)  
            print(f"\n{username} deleted successfully.")
        else:
            print("Deletion canceled.")
            return edit_user_menu(db, username)
    
    elif choice == "3":
        return edit(db, username)



def edit_cleaner_menu(db):
    cursor = db.cursor()

     # Fetch and display all cleaners
    cleaners = cursor.execute("SELECT address, name FROM cleaners;").fetchall()
    if not cleaners:
        print("No cleaners found in the database.")
        return

    print("\nCleaners Available:")
    for cleaner in cleaners:
        print(f"Address: {cleaner[0]}, Name: {cleaner[1]}")

    # Prompt user to select a cleaner by address
    selected_address = input("\nEnter the address of the cleaner you want to edit (Enter -1 to exit): ")
    if selected_address == "-1":
        return
    if selected_address not in [cleaner[0] for cleaner in cleaners]:
        print("Invalid address. Please try again.")
        return edit_cleaner_menu(db)


    print(f"\nWhat would you like to do with the address : {selected_address}?")
    print("1. Edit")
    print("2. Delete")
    print("3. Cancel")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        # Display existing supported systems for the selected cleaner
        supported_systems = cursor.execute(
            "SELECT wash_method, detergent, dry_method FROM SupportsCleaningSystem WHERE cleaners = ?;",
            (selected_address,)
        ).fetchall()

        print(f"\nDetails for cleaner at {selected_address}:")
        print(f"Supported Systems: {supported_systems if supported_systems else 'None'}")

        # Gather new values for the cleaner
        new_name = input("\nEnter new name for the cleaner (or press Enter to keep current name): ").strip()
        update_supported_systems = input("Do you want to update supported systems? (yes/no): ").strip().lower()

        new_supported_systems = []
        if update_supported_systems == "yes":
            print("Enter new supported systems (type 'done' to finish):")
            while True:
                wash_method = input("Wash Method (or type 'done' to finish): ").strip()
                if wash_method.lower() == "done":
                    break
                detergent = input("Detergent: ").strip()
                dry_method = input("Dry Method: ").strip()
                if wash_method and detergent and dry_method:
                    new_supported_systems.append((wash_method, detergent, dry_method))

        # Call update_cleaners function with provided inputs
        update_cleaners(
            address=selected_address,
            new_name=new_name if new_name else None,
            new_supported_systems=new_supported_systems if update_supported_systems == "yes" else None,
            db=db
        )

    elif choice == "2":
        # Proceed with deleting the laundry item
        confirm = input(
            f"Are you sure you want to delete {selected_address}? (yes/no): "
        ).strip().lower()
        if confirm == "yes":
            delete_cleaners(selected_address, db)  # Assuming delete_laundry is implemented
            print(f"\n{selected_address} deleted successfully.")
        else:
            print("Deletion canceled.")
        
    elif choice == "3":
        # Cancel the operation
        print("Operation canceled.")
        return edit_cleaner_menu(db)

    # Ask user if they want to edit another cleaner
    edit_again = input("\nDo you want to edit another cleaner? (yes/no): ").strip().lower()
    if edit_again == "yes":
        return edit_cleaner_menu(db)


def edit(db: sqlite3.Connection, username: str) -> None:
    cursor = db.cursor()
    print("1. Laundry")
    print("2. Detergent")
    print("3. User")
    print("4. Cleaner")
    option = input("Select an option: ")
    if not option.isdigit():
        print("Invalid option. Please try again.")
        return edit(db, username)
    int_option = int(option)
    if int_option < 1 or int_option > 4:
        print("Invalid option. Please try again.")
        return edit(db, username)
    if int_option == 1:
        edit_laundry_menu(db, username)
    elif int_option == 2:
        edit_detergent_menu(db)
    elif int_option == 3:
        edit_user_menu(db, username)
    else:
        edit_cleaner_menu(db)

def execute_menu_option(menu_option: int, db: sqlite3.Connection, username: str) -> None:
    match menu_option:
        case 1:
            do_laundry(db, username)
        case 2:
            open_dirty_menu(db, username)
        case 3:
            edit(db, username)
        case 4:
            db.close()
            exit()
        case _:
            print("Invalid option. Please try again.")
    execute_menu_option(get_menu_option(db), db, username)

# First, enter name

# menu items
# 1. Do Laundry
# 2. Mark things as dirty
# 3. Edit (Insert/Delete/Update)
#  a. Laundry
    # if it's a new color, ask if it's dark or light
#  b. Detergent
#  c. User
#  d. Cleaner

db = sqlite3.connect("Checkpoint2-dbase.sqlite3")

# establish foreign key constraints
db.execute("PRAGMA foreign_keys = ON;")
db.commit()

cursor = db.cursor()

username = get_username(db)
execute_menu_option(get_menu_option(db), db, username)
