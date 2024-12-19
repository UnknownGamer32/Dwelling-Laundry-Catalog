-- DATA RETRIEVAL --

-- List all laundry items owned by a specific person
-- This one works, test with: WHERE OwnedBy.name = 'Donald'
SELECT laundry.id, laundry.description, laundry.location, laundry.special_instructions, laundry.volume, laundry.dirty
FROM laundry
JOIN OwnedBy ON laundry.id = OwnedBy.id
WHERE OwnedBy.name = :specific_person_name;

-- Get laundry items that a person is allowed to wash
-- This one works, test with: WHERE ocw.washer = 'Donald'
SELECT DISTINCT l.id, l.description, l.location, l.special_instructions, l.volume, l.dirty
FROM laundry l
JOIN OwnedBy o ON l.id = o.id
LEFT JOIN OwnerCanWash ocw ON o.name = ocw.washee
WHERE ocw.washer = :person_name 
   OR o.name = :person_name;

-- Identify compatible detergents for dark/light clothes
-- This works, test with: WHERE (d.for_darks = TRUE AND TRUE)
SELECT DISTINCT d.name
FROM detergent d
WHERE (d.for_darks = TRUE AND :is_dark = TRUE)
   OR (d.for_lights = TRUE AND :is_dark = FALSE);

-- Check allergy information
-- This works, test with: WHERE iat.owner = 'Herbert'
SELECT DISTINCT d.name as detergent_name, di.name as ingredient_name
FROM detergent d
JOIN DetergentComposedOf dco ON d.name = dco.detergent
JOIN detergent_ingredient di ON dco.ingredient = di.name
JOIN IsAllergicTo iat ON di.name = iat.detergent_ingredient
WHERE iat.owner = :owner_name;

-- Find laundry items washed by a specific cleaning system
-- This works, test with: 
-- WHERE cb.wash_method = 'Washing Machine' 
--   AND cb.detergent = 'AllPurpose'
--   AND cb.dry_method = 'Tumble Dry'
SELECT l.id, l.description
FROM laundry l
JOIN CleanedBy cb ON l.id = cb.laundry
WHERE cb.wash_method = :wash_method
  AND cb.detergent = :detergent_name
  AND cb.dry_method = :dry_method;

-- Retrieve laundry history for an item
-- This works, test with: WHERE l.id = 1
SELECT l.id, l.description, cb.wash_method, cb.detergent, cb.dry_method
FROM laundry l
JOIN CleanedBy cb ON l.id = cb.laundry
WHERE l.id = :laundry_id;

-- List cleaners liked by a specific person
-- This returns nothing because no Likes data was inserted
-- Need to add: INSERT INTO Likes (cleaners, owner) VALUES ('1234 Elm St', 'Donald');
SELECT c.address, c.name
FROM cleaners c
JOIN Likes l ON c.address = l.cleaners
WHERE l.owner = :person_name;

-- Identify compatible laundry items for a load
-- This works, test with:
-- WHERE scs.wash_method = 'Washing Machine'
--   AND scs.detergent = 'AllPurpose'
--   AND scs.dry_method = 'Tumble Dry'
SELECT DISTINCT l.id, l.description
FROM laundry l
JOIN CleanedBy cb ON l.id = cb.laundry
JOIN SupportsCleaningSystem scs ON cb.wash_method = scs.wash_method 
    AND cb.detergent = scs.detergent 
    AND cb.dry_method = scs.dry_method
WHERE scs.wash_method = :desired_wash_method
  AND scs.detergent = :desired_detergent
  AND scs.dry_method = :desired_dry_method;

-- Get special instructions for a laundry item
-- This works, test with: WHERE id = 1
SELECT id, description, special_instructions
FROM laundry
WHERE id = :laundry_id;

-- List detergent ingredients
-- This works, test with: WHERE dco.detergent = 'AllPurpose'
SELECT di.name as ingredient_name
FROM detergent_ingredient di
JOIN DetergentComposedOf dco ON di.name = dco.ingredient
WHERE dco.detergent = :detergent_name;
-------------------------------------- 

-- DATA INSERTION
INSERT INTO owner (name) VALUES ('Donald');
INSERT INTO owner (name) VALUES ('Herbert');
INSERT INTO owner (name) VALUES ('Harry');

INSERT INTO OwnerCanWash (washer, washee) VALUES ('Donald', 'Herbert');
INSERT INTO OwnerCanWash (washer, washee) VALUES ('Donald', 'Harry');
INSERT INTO OwnerCanWash (washer, washee) VALUES ('Harry', 'Herbert');
INSERT INTO OwnerCanWash (washer, washee) VALUES ('Herbert', 'Harry');

INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (1, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (2, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (3, 'Pair of sweats', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (4, 'Pair of jeans', 'Closet', 'Machine wash cold', FALSE, 3);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (5, 'Suit top', 'Closet', 'Dry clean only', FALSE, 4);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (6, 'Suit bottom', 'Closet', 'Dry clean only', FALSE, 4);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (7, 'Button-up shirt', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (8, 'Underpants', 'Dresser', 'Machine wash warm', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (9, 'Socks', 'Dresser', 'Machine wash warm', FALSE, 1);

INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (10, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (11, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (12, 'Pair of sweats', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (13, 'Pair of sweats', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (14, 'Pair of jeans', 'Closet', 'Machine wash cold', FALSE, 3);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (15, 'Suit top', 'Closet', 'Dry clean only', FALSE, 4);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (16, 'Suit bottom', 'Closet', 'Dry clean only', FALSE, 4);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (17, 'Button-up shirt', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (18, 'Underpants', 'Dresser', 'Machine wash warm', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (19, 'Socks', 'Dresser', 'Machine wash warm', FALSE, 1);

INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (20, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (21, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (22, 'Pair of sweats', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (23, 'Pair of jeans', 'Closet', 'Machine wash cold', FALSE, 3);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (24, 'Suit top', 'Closet', 'Dry clean only', FALSE, 4);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (25, 'Suit bottom', 'Closet', 'Dry clean only', FALSE, 4);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (26, 'Button-up shirt', 'Closet', 'Machine wash warm', FALSE, 2);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (27, 'Underpants', 'Dresser', 'Machine wash warm', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (28, 'Socks', 'Dresser', 'Machine wash warm', FALSE, 1);
INSERT INTO laundry (id, description, location, special_instructions, dirty, volume) VALUES (29, 'T-shirt', 'Closet', 'Machine wash cold', FALSE, 1);

INSERT INTO IsColor (color, laundry) VALUES ('Blue', 1);
INSERT INTO IsColor (color, laundry) VALUES ('Red', 2);
INSERT INTO IsColor (color, laundry) VALUES ('Gray', 3);
INSERT INTO IsColor (color, laundry) VALUES ('Blue', 4);
INSERT INTO IsColor (color, laundry) VALUES ('Black', 5);
INSERT INTO IsColor (color, laundry) VALUES ('Black', 6);
INSERT INTO IsColor (color, laundry) VALUES ('White', 7);
INSERT INTO IsColor (color, laundry) VALUES ('White', 8);
INSERT INTO IsColor (color, laundry) VALUES ('White', 9);

INSERT INTO IsColor (color, laundry) VALUES ('Blue', 10);
INSERT INTO IsColor (color, laundry) VALUES ('Cyan', 11);
INSERT INTO IsColor (color, laundry) VALUES ('Gray', 12);
INSERT INTO IsColor (color, laundry) VALUES ('Gray', 13);
INSERT INTO IsColor (color, laundry) VALUES ('Blue', 14);
INSERT INTO IsColor (color, laundry) VALUES ('Black', 15);
INSERT INTO IsColor (color, laundry) VALUES ('White', 16);
INSERT INTO IsColor (color, laundry) VALUES ('White', 17);
INSERT INTO IsColor (color, laundry) VALUES ('White', 18);
INSERT INTO IsColor (color, laundry) VALUES ('White', 19);

INSERT INTO IsColor (color, laundry) VALUES ('Yellow', 20);
INSERT INTO IsColor (color, laundry) VALUES ('Blue', 21);
INSERT INTO IsColor (color, laundry) VALUES ('Gray', 22);
INSERT INTO IsColor (color, laundry) VALUES ('Blue', 23);
INSERT INTO IsColor (color, laundry) VALUES ('Black', 24);
INSERT INTO IsColor (color, laundry) VALUES ('Black', 25);
INSERT INTO IsColor (color, laundry) VALUES ('White', 26);
INSERT INTO IsColor (color, laundry) VALUES ('White', 27);
INSERT INTO IsColor (color, laundry) VALUES ('White', 28);
INSERT INTO IsColor (color, laundry) VALUES ('White', 29);

-- ownedby 1-9 by Donald, 10-19 by Herbert, 20-29 by Harry
-- Herbert owns two pairs of sweats
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 1);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 2);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 3);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 4);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 5);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 6);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 7);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 8);
INSERT INTO OwnedBy (name, id) VALUES ('Donald', 9);

INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 10);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 11);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 12);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 13);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 14);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 15);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 16);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 17);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 18);
INSERT INTO OwnedBy (name, id) VALUES ('Herbert', 19);

INSERT INTO OwnedBy (name, id) VALUES ('Harry', 20);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 21);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 22);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 23);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 24);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 25);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 26);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 27);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 28);
INSERT INTO OwnedBy (name, id) VALUES ('Harry', 29);

INSERT INTO color (color, dark) VALUES ('Blue', TRUE);
INSERT INTO color (color, dark) VALUES ('Red', TRUE);
INSERT INTO color (color, dark) VALUES ('Gray', TRUE);
INSERT INTO color (color, dark) VALUES ('Black', TRUE);
INSERT INTO color (color, dark) VALUES ('White', FALSE);
INSERT INTO color (color, dark) VALUES ('Cyan', FALSE);
INSERT INTO color (color, dark) VALUES ('Yellow', FALSE);

INSERT INTO detergent_ingredient (name) VALUES ('Sodium Lauryl Sulfate');
INSERT INTO IsAllergicTo (owner, detergent_ingredient) VALUES ('Herbert', 'Sodium Lauryl Sulfate');

INSERT INTO cleaners (address, name) VALUES ('1234 Elm St', 'Dry Cleaners R Us');
INSERT INTO cleaners (address, name) VALUES ('Home', 'Washing Machine');

INSERT INTO detergent (name, for_darks, for_lights, whitens) VALUES ('AllPurpose', TRUE, TRUE, FALSE);
INSERT INTO detergent (name, for_darks, for_lights, whitens) VALUES ('DrySolvent', FALSE, FALSE, TRUE);
INSERT INTO detergent (name, for_darks, for_lights, whitens) VALUES ('BadDetergent', FALSE, FALSE, FALSE);

INSERT INTO detergent_ingredient (name) VALUES ('Water');

INSERT INTO DetergentComposedOf (detergent, ingredient) VALUES ('AllPurpose', 'Water');
INSERT INTO DetergentComposedOf (detergent, ingredient) VALUES ('DrySolvent', 'Water');
INSERT INTO DetergentComposedOf (detergent, ingredient) VALUES ('BadDetergent', 'Water');
INSERT INTO DetergentComposedOf (detergent, ingredient) VALUES ('BadDetergent', 'Sodium Lauryl Sulfate');

INSERT INTO cleaning_system (wash_method, detergent, dry_method) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry');
INSERT INTO cleaning_system (wash_method, detergent, dry_method) VALUES ('Washing Machine', 'AllPurpose', 'Hang Dry');
INSERT INTO cleaning_system (wash_method, detergent, dry_method) VALUES ('Washing Machine', 'BadDetergent', 'Tumble Dry');
INSERT INTO cleaning_system (wash_method, detergent, dry_method) VALUES ('Washing Machine', 'BadDetergent', 'Hang Dry');
INSERT INTO cleaning_system (wash_method, detergent, dry_method) VALUES ('Dry Clean', 'DrySolvent', 'Press');

INSERT INTO SupportsCleaningSystem (cleaners, wash_method, detergent, dry_method) VALUES ('Home', 'Washing Machine', 'AllPurpose', 'Tumble Dry');
INSERT INTO SupportsCleaningSystem (cleaners, wash_method, detergent, dry_method) VALUES ('456 Elm St', 'Dry Clean', 'DrySolvent', 'Press');

INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 1);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 2);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 3);

INSERT INTO Likes (cleaners, owner) VALUES ('Home', 'Donald');
INSERT INTO Likes (cleaners, owner) VALUES ('Home', 'Herbert');
INSERT INTO Likes (cleaners, owner) VALUES ('Home', 'Harry');
INSERT INTO Likes (cleaners, owner) VALUES ('456 Elm St', 'Donald');
INSERT INTO Likes (cleaners, owner) VALUES ('456 Elm St', 'Herbert');
INSERT INTO Likes (cleaners, owner) VALUES ('456 Elm St', 'Harry');

INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 1);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 2);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 3);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 4);
INSERT INTO Deterges (detergent, laundry) VALUES ('DrySolvent', 5);
INSERT INTO Deterges (detergent, laundry) VALUES ('DrySolvent', 6);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 7);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 8);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 9);

INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 10);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 11);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 12);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 13);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 14);
INSERT INTO Deterges (detergent, laundry) VALUES ('DrySolvent', 15);
INSERT INTO Deterges (detergent, laundry) VALUES ('DrySolvent', 16);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 17);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 18);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 19);

INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 20);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 21);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 22);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 23);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 24);
INSERT INTO Deterges (detergent, laundry) VALUES ('DrySolvent', 25);
INSERT INTO Deterges (detergent, laundry) VALUES ('DrySolvent', 26);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 27);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 28);
INSERT INTO Deterges (detergent, laundry) VALUES ('AllPurpose', 29);

INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 1);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 2);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 3);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 4);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Dry Clean', 'DrySolvent', 'Press', 5);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Dry Clean', 'DrySolvent', 'Press', 6);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 7);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 8);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 9);

INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 10);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 11);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 12);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 13);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 14);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Dry Clean', 'DrySolvent', 'Press', 15);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Dry Clean', 'DrySolvent', 'Press', 16);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 17);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 18);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 19);

INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 20);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 21);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 22);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 23);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 24);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Dry Clean', 'DrySolvent', 'Press', 25);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Dry Clean', 'DrySolvent', 'Press', 26);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 27);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 28);
INSERT INTO CleanedBy (wash_method, detergent, dry_method, laundry) VALUES ('Washing Machine', 'AllPurpose', 'Tumble Dry', 29);


-- DATABASE CREATION

CREATE TABLE owner (
  name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE laundry (
  id INT PRIMARY KEY,
  description VARCHAR(255),
  location VARCHAR(255),
  special_instructions VARCHAR(255),
  dirty BOOLEAN,
  volume INT
);

CREATE TABLE detergent (
  name VARCHAR(255) PRIMARY KEY,
  for_darks BOOLEAN,
  for_lights BOOLEAN,
  whitens BOOLEAN
);

CREATE TABLE detergent_ingredient (
  name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE cleaning_system (
  wash_method VARCHAR(255),
  detergent VARCHAR(255),
  dry_method VARCHAR(255),
  PRIMARY KEY (wash_method, detergent, dry_method),
  FOREIGN KEY (detergent) REFERENCES detergent(name)
);

CREATE TABLE color (
  color VARCHAR(255) PRIMARY KEY,
  dark BOOLEAN
);

CREATE TABLE cleaners (
  address VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE IsColor (
  color VARCHAR(255),
  laundry INT,
  FOREIGN KEY (color) REFERENCES color(color),
  FOREIGN KEY (laundry) REFERENCES laundry(id)
);

CREATE TABLE SupportsCleaningSystem (
  cleaners VARCHAR(255),
  wash_method VARCHAR(255),
  detergent VARCHAR(255),
  dry_method VARCHAR(255),
  PRIMARY KEY (cleaners, wash_method, detergent, dry_method),
  FOREIGN KEY (wash_method, detergent, dry_method) REFERENCES cleaning_system(wash_method, detergent, dry_method),
  FOREIGN KEY (cleaners) REFERENCES cleaners(address)
);

CREATE TABLE CleanedBy (
  wash_method VARCHAR(255),
  detergent VARCHAR(255),
  dry_method VARCHAR(255),
  laundry INT,
  PRIMARY KEY (wash_method, detergent, dry_method, laundry),
  FOREIGN KEY (wash_method, detergent, dry_method) REFERENCES cleaning_system(wash_method, detergent, dry_method),
  FOREIGN KEY (laundry) REFERENCES laundry(id)
);

CREATE TABLE IsAllergicTo (
  owner VARCHAR(255),
  detergent_ingredient VARCHAR(255),
  PRIMARY KEY (owner, detergent_ingredient),
  FOREIGN KEY (owner) REFERENCES owner(name),
  FOREIGN KEY (detergent_ingredient) REFERENCES detergent_ingredient(name)
);

CREATE TABLE Deterges (
  laundry INT,
  detergent VARCHAR(255),
  PRIMARY KEY (laundry, detergent),
  FOREIGN KEY (detergent) REFERENCES detergent(name),
  FOREIGN KEY (laundry) REFERENCES laundry(id)
);

CREATE TABLE DetergentComposedOf (
  detergent VARCHAR(255),
  ingredient VARCHAR(255),
  PRIMARY KEY (detergent, ingredient),
  FOREIGN KEY (detergent) REFERENCES detergent(name),
  FOREIGN KEY (ingredient) REFERENCES detergent_ingredient(name)
);

CREATE TABLE OwnerCanWash (
  washer VARCHAR(255),
  washee VARCHAR(255),
  PRIMARY KEY (washer, washee),
  FOREIGN KEY (washer) REFERENCES owner(name),
  FOREIGN KEY (washee) REFERENCES owner(name)
);

CREATE TABLE OwnedBy (
  name VARCHAR(255),
  id INT,
  PRIMARY KEY (name, id),
  FOREIGN KEY (name) REFERENCES owner(name),
  FOREIGN KEY (id) REFERENCES laundry(id)
);

CREATE TABLE Likes (
  cleaners VARCHAR(255),
  owner VARCHAR(255),
  PRIMARY KEY (cleaners, owner),
  FOREIGN KEY (owner) REFERENCES owner(name),
  FOREIGN KEY (cleaners) REFERENCES cleaners(address)
);

--Python script to insert data

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

    if can_wash:
        for washee in can_wash:
            try:
                cursor.execute(
                    "INSERT INTO OwnerCanWash VALUES (?, ?);",
                    (name, washee)
                )
            except sqlite3.IntegrityError:
                print(f"Wash permission {name}->{washee} already exists")

    if liked_cleaners:
        for cleaner in liked_cleaners:
            try:
                cursor.execute(
                    "INSERT INTO Likes VALUES (?, ?);",
                    (cleaner, name)
                )
            except sqlite3.IntegrityError:
                print(f"Like relationship {name}->{cleaner} already exists")

    cursor.close()
    db.commit()
    db.close()

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

    cursor.close()
    db.commit()
    db.close()

def insert_laundry(
    owner: str,
    description: str,
    db: sqlite3.Connection = connect_db(),
    location: str = "",
    special_instructions: str = "",
    dirty: bool = False,
    volume: int = 0,
    detergents: list[str] = [],
    color: str = "",
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
                "INSERT INTO Deterges VALUES (?, ?);", (laundry_id, detergent)
            )

    if color:
        cursor.execute("INSERT INTO IsColor VALUES (?, ?);", (color, laundry_id))

    if owner:
        cursor.execute("INSERT INTO OwnedBy VALUES (?, ?);", (owner, laundry_id))

    cursor.close()
    db.commit()
    db.close()


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

    if ingredients:
        for ingredient in ingredients:
            try:
                cursor.execute(
                    f"INSERT INTO detergent_ingredient VALUES (?)", (ingredient,)
                )
            except sqlite3.IntegrityError:
                print(f"Ingredient {ingredient} already exists in the database.")

    cursor.close()
    db.commit()
    db.close()

-- python script to delete data

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
        cursor.execute("DELETE FROM OwnedBy WHERE name = ?;", (name,))
        # Finally delete the owner
        cursor.execute("DELETE FROM owner WHERE name = ?;", (name,))
        print(f"Owner {name} and related data deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting owner {name}: {e}")

    cursor.close()
    db.commit()
    db.close()

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

    cursor.close()
    db.commit()
    db.close()

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

    cursor.close()
    db.commit()
    db.close()

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

    cursor.close()
    db.commit()
    db.close()

-- python script to update data

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
                cursor.execute(
                    "INSERT OR IGNORE INTO detergent_ingredient VALUES (?);", 
                    (allergy,)
                )
                cursor.execute(
                    "INSERT INTO IsAllergicTo VALUES (?, ?);",
                    (name, allergy)
                )

        if new_can_wash is not None:
            # Remove old wash permissions
            cursor.execute("DELETE FROM OwnerCanWash WHERE washer = ?;", (name,))
            # Add new wash permissions
            for washee in new_can_wash:
                cursor.execute(
                    "INSERT INTO OwnerCanWash VALUES (?, ?);",
                    (name, washee)
                )

        if new_liked_cleaners is not None:
            # Remove old likes
            cursor.execute("DELETE FROM Likes WHERE owner = ?;", (name,))
            # Add new likes
            for cleaner in new_liked_cleaners:
                cursor.execute(
                    "INSERT INTO Likes VALUES (?, ?);",
                    (cleaner, name)
                )

        print(f"Owner {name} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating owner {name}: {e}")

    cursor.close()
    db.commit()
    db.close()

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
            cursor.execute(
                "UPDATE cleaners SET name = ? WHERE address = ?;",
                (new_name, address)
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
    db.close()

def update_laundry(
    laundry_id: int,
    new_description: str = None,
    new_location: str = None,
    new_special_instructions: str = None,
    new_dirty: bool = None,
    new_volume: int = None,
    new_detergents: list[str] = None,
    new_color: str = None,
    new_owner: str = None,
    db: sqlite3.Connection = connect_db()
) -> None:
    cursor = db.cursor()

    try:
        # Verify laundry exists
        cursor.execute("SELECT id FROM laundry WHERE id = ?;", (laundry_id,))
        if not cursor.fetchone():
            print(f"Laundry item {laundry_id} does not exist in the database.")
            return

        # Update main laundry table
        update_fields = []
        update_values = []
        if new_description is not None:
            update_fields.append("description = ?")
            update_values.append(new_description)
        if new_location is not None:
            update_fields.append("location = ?")
            update_values.append(new_location)
        if new_special_instructions is not None:
            update_fields.append("special_instructions = ?")
            update_values.append(new_special_instructions)
        if new_dirty is not None:
            update_fields.append("dirty = ?")
            update_values.append(new_dirty)
        if new_volume is not None:
            update_fields.append("volume = ?")
            update_values.append(new_volume)

        if update_fields:
            update_values.append(laundry_id)
            cursor.execute(
                f"UPDATE laundry SET {', '.join(update_fields)} WHERE id = ?;",
                tuple(update_values)
            )

        if new_detergents is not None:
            # Update detergents
            cursor.execute("DELETE FROM Deterges WHERE laundry = ?;", (laundry_id,))
            for detergent in new_detergents:
                cursor.execute(
                    "INSERT INTO Deterges VALUES (?, ?);",
                    (laundry_id, detergent)
                )

        if new_color is not None:
            # Update color
            cursor.execute("DELETE FROM IsColor WHERE laundry = ?;", (laundry_id,))
            cursor.execute(
                "INSERT INTO IsColor VALUES (?, ?);",
                (new_color, laundry_id)
            )

        if new_owner is not None:
            # Update owner
            cursor.execute("DELETE FROM OwnedBy WHERE id = ?;", (laundry_id,))
            cursor.execute(
                "INSERT INTO OwnedBy VALUES (?, ?);",
                (new_owner, laundry_id)
            )

        print(f"Laundry item {laundry_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating laundry item {laundry_id}: {e}")

    cursor.close()
    db.commit()
    db.close()

def update_detergent(
    name: str,
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
        update_fields = []
        update_values = []
        if new_for_darks is not None:
            update_fields.append("for_darks = ?")
            update_values.append(new_for_darks)
        if new_for_lights is not None:
            update_fields.append("for_lights = ?")
            update_values.append(new_for_lights)
        if new_whitens is not None:
            update_fields.append("whitens = ?")
            update_values.append(new_whitens)

        if update_fields:
            update_values.append(name)
            cursor.execute(
                f"UPDATE detergent SET {', '.join(update_fields)} WHERE name = ?;",
                tuple(update_values)
            )

        if new_ingredients is not None:
            # Update ingredients
            cursor.execute("DELETE FROM DetergentComposedOf WHERE detergent = ?;", (name,))
            for ingredient in new_ingredients:
                cursor.execute(
                    "INSERT OR IGNORE INTO detergent_ingredient VALUES (?);",
                    (ingredient,)
                )
                cursor.execute(
                    "INSERT INTO DetergentComposedOf VALUES (?, ?);",
                    (name, ingredient)
                )

        print(f"Detergent {name} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating detergent {name}: {e}")

    cursor.close()
    db.commit()
    db.close()