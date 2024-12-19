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
