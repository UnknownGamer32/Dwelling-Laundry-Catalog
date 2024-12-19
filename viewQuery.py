# 1. List all laundry items owned by a specific person
def list_laundry_owned_by_person(conn, specific_person_name):
    query = """
    SELECT laundry.id, laundry.description, laundry.location, laundry.special_instructions, laundry.volume, laundry.dirty
    FROM laundry
    JOIN OwnedBy ON laundry.id = OwnedBy.id
    WHERE OwnedBy.name = :specific_person_name;
    """
    cursor = conn.execute(query, {'specific_person_name': specific_person_name})
    for row in cursor.fetchall():
        print(dict(row))

# 2. Get laundry items that a person is allowed to wash
def get_laundry_allowed_to_wash(conn, person_name):
    query = """
    SELECT DISTINCT l.id, l.description, l.location, l.special_instructions, l.volume, l.dirty
    FROM laundry l
    JOIN OwnedBy o ON l.id = o.id
    LEFT JOIN OwnerCanWash ocw ON o.name = ocw.washee
    WHERE ocw.washer = :person_name 
       OR o.name = :person_name;
    """
    cursor = conn.execute(query, {'person_name': person_name})
    for row in cursor.fetchall():
        print(dict(row))

# 3. Identify compatible detergents for dark/light clothes
def identify_compatible_detergents(conn, is_dark):
    query = """
    SELECT DISTINCT d.name
    FROM detergent d
    WHERE (d.for_darks = TRUE AND :is_dark = TRUE)
       OR (d.for_lights = TRUE AND :is_dark = FALSE);
    """
    cursor = conn.execute(query, {'is_dark': is_dark})
    for row in cursor.fetchall():
        print(dict(row))

# 4. Check allergy information
def check_allergy_information(conn, owner_name):
    query = """
    SELECT DISTINCT d.name as detergent_name, di.name as ingredient_name
    FROM detergent d
    JOIN DetergentComposedOf dco ON d.name = dco.detergent
    JOIN detergent_ingredient di ON dco.ingredient = di.name
    JOIN IsAllergicTo iat ON di.name = iat.detergent_ingredient
    WHERE iat.owner = :owner_name;
    """
    cursor = conn.execute(query, {'owner_name': owner_name})
    for row in cursor.fetchall():
        print(dict(row))

# 5. Find laundry items washed by a specific cleaning system
def find_laundry_by_cleaning_system(conn, wash_method, detergent_name, dry_method):
    query = """
    SELECT l.id, l.description
    FROM laundry l
    JOIN CleanedBy cb ON l.id = cb.laundry
    WHERE cb.wash_method = :wash_method
      AND cb.detergent = :detergent_name
      AND cb.dry_method = :dry_method;
    """
    cursor = conn.execute(query, {'wash_method': wash_method, 'detergent_name': detergent_name, 'dry_method': dry_method})
    for row in cursor.fetchall():
        print(dict(row))

# 6. Retrieve laundry history for an item
def get_laundry_history(conn, laundry_id):
    query = """
    SELECT l.id, l.description, cb.wash_method, cb.detergent, cb.dry_method
    FROM laundry l
    JOIN CleanedBy cb ON l.id = cb.laundry
    WHERE l.id = :laundry_id;
    """
    cursor = conn.execute(query, {'laundry_id': laundry_id})
    for row in cursor.fetchall():
        print(dict(row))

# 7. List cleaners liked by a specific person
def list_liked_cleaners(conn, person_name):
    query = """
    SELECT c.address, c.name
    FROM cleaners c
    JOIN Likes l ON c.address = l.cleaners
    WHERE l.owner = :person_name;
    """
    cursor = conn.execute(query, {'person_name': person_name})
    for row in cursor.fetchall():
        print(dict(row))

# 8. Identify compatible laundry items for a load
def identify_compatible_laundry(conn, desired_wash_method, desired_detergent, desired_dry_method):
    query = """
    SELECT DISTINCT l.id, l.description
    FROM laundry l
    JOIN CleanedBy cb ON l.id = cb.laundry
    JOIN SupportsCleaningSystem scs ON cb.wash_method = scs.wash_method 
        AND cb.detergent = scs.detergent 
        AND cb.dry_method = scs.dry_method
    WHERE scs.wash_method = :desired_wash_method
      AND scs.detergent = :desired_detergent
      AND scs.dry_method = :desired_dry_method;
    """
    cursor = conn.execute(query, {'desired_wash_method': desired_wash_method, 'desired_detergent': desired_detergent, 'desired_dry_method': desired_dry_method})
    for row in cursor.fetchall():
        print(dict(row))

# 9. Get special instructions for a laundry item
def get_special_instructions(conn, laundry_id):
    query = """
    SELECT id, description, special_instructions
    FROM laundry
    WHERE id = :laundry_id;
    """
    cursor = conn.execute(query, {'laundry_id': laundry_id})
    for row in cursor.fetchall():
        print(dict(row))

# 10. List detergent ingredients
def list_detergent_ingredients(conn, detergent_name):
    query = """
    SELECT di.name as ingredient_name
    FROM detergent_ingredient di
    JOIN DetergentComposedOf dco ON di.name = dco.ingredient
    WHERE dco.detergent = :detergent_name;
    """
    cursor = conn.execute(query, {'detergent_name': detergent_name})
    for row in cursor.fetchall():
        print(dict(row))