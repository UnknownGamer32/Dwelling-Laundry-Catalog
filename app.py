from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect("Checkpoint2-dbase.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn

# Route: Login page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM owner;")
            owners = [row["name"] for row in cursor.fetchall()]
            if username in owners:
                return redirect(url_for("menu", username=username))
            else:
                return render_template("login.html", error="Name not found. Please try again.")
    return render_template("login.html")

# Route: Main menu
@app.route("/menu/<username>")
def menu(username):
    return render_template("menu.html", username=username)

# Route: Do Laundry
@app.route("/laundry/<username>", methods=["GET", "POST"])
def laundry(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            cleaner = request.form.get("cleaner")
            cleaning_method = request.form.get("cleaning_method")
            laundry_ids = request.form.getlist("laundry_ids")

            # Mark selected laundry items as clean
            for laundry_id in laundry_ids:
                cursor.execute("UPDATE laundry SET dirty = 0 WHERE id = ?;", (laundry_id,))
            conn.commit()
            return redirect(url_for("menu", username=username))

        # Get cleaners available
        cursor.execute("SELECT address, name FROM cleaners;")
        cleaners = cursor.fetchall()

        # Get cleaning methods available (initially empty until a cleaner is selected)
        cleaning_methods = []
        laundry_items = []

        # If a cleaner is selected, fetch cleaning methods and laundry items
        selected_cleaner = request.args.get("cleaner")
        if selected_cleaner:
            cursor.execute(
                "SELECT wash_method, detergent, dry_method FROM SupportsCleaningSystem WHERE cleaners = ?;",
                (selected_cleaner,)
            )
            cleaning_methods = cursor.fetchall()

            # Fetch laundry items owned by the user that match the selected cleaner's methods
            cursor.execute(
                """
                SELECT l.* FROM laundry l
                JOIN OwnedBy ob ON l.id = ob.id
                WHERE ob.name = ? AND l.dirty = 1;
                """,
                (username,)
            )
            laundry_items = cursor.fetchall()

    return render_template(
        "laundry.html",
        username=username,
        cleaners=cleaners,
        cleaning_methods=cleaning_methods,
        laundry_items=laundry_items,
    )

# Route: Mark Clothes Dirty
@app.route("/mark_dirty/<username>", methods=["GET", "POST"])
def mark_dirty(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            laundry_ids = request.form.getlist("laundry_ids")
            for laundry_id in laundry_ids:
                cursor.execute("UPDATE laundry SET dirty = 1 WHERE id = ?;", (laundry_id,))
            conn.commit()
            return redirect(url_for("menu", username=username))

        cursor.execute(
            """
            SELECT l.* FROM laundry l
            JOIN OwnedBy ob ON l.id = ob.id
            WHERE ob.name = ? AND l.dirty = 0;
            """,
            (username,)
        )
        clean_laundry = cursor.fetchall()

    return render_template("mark_dirty.html", username=username, laundry=clean_laundry)

# Route: Edit menu
@app.route("/edit_menu/<username>")
def edit_menu(username):
    return render_template("edit_menu.html", username=username)

# Routes for managing laundry
@app.route("/edit/laundry/<username>", methods=["GET", "POST"])
def edit_laundry(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            action = request.form.get("action")
            if action == "edit":
                cursor.execute(
                    """
                    UPDATE laundry
                    SET description = ?, location = ?, special_instructions = ?, dirty = ?, volume = ?
                    WHERE id = ?;
                    """,
                    (
                        request.form["description"],
                        request.form["location"],
                        request.form["special_instructions"],
                        int(request.form["dirty"]),
                        request.form["volume"],
                        request.form["laundry_id"],
                    ),
                )

            elif action == "delete":
                cursor.execute("DELETE FROM laundry WHERE id = ?;", (request.form["laundry_id"],))

            conn.commit()

            # Fetch updated laundry list and return only the table
            cursor.execute(
                """
                SELECT l.id, l.description, l.location, l.special_instructions, l.dirty, l.volume
                FROM laundry l
                JOIN OwnedBy ob ON l.id = ob.id
                WHERE ob.name = ?;
                """,
                (username,),
            )
            laundry_items = [
                {
                    "id": row["id"],
                    "description": row["description"],
                    "location": row["location"],
                    "special_instructions": row["special_instructions"],
                    "dirty": row["dirty"],
                    "volume": row["volume"],
                }
                for row in cursor.fetchall()
            ]
            return render_template("partials/laundry_table.html", laundry=laundry_items)

        # Render full page for GET requests
        cursor.execute(
            """
            SELECT l.id, l.description, l.location, l.special_instructions, l.dirty, l.volume
            FROM laundry l
            JOIN OwnedBy ob ON l.id = ob.id
            WHERE ob.name = ?;
            """,
            (username,),
        )
        laundry_items = [
            {
                "id": row["id"],
                "description": row["description"],
                "location": row["location"],
                "special_instructions": row["special_instructions"],
                "dirty": row["dirty"],
                "volume": row["volume"],
            }
            for row in cursor.fetchall()
        ]

    return render_template("edit_laundry.html", username=username, laundry=laundry_items)

# Routes for managing detergents
@app.route("/edit/detergent", methods=["GET", "POST"])
def edit_detergent():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            action = request.form.get("action")

            if action == "edit":
                # Edit detergent properties
                cursor.execute(
                    """
                    UPDATE detergent
                    SET for_darks = ?, for_lights = ?, whitens = ?
                    WHERE name = ?;
                    """,
                    (
                        int("for_darks" in request.form),
                        int("for_lights" in request.form),
                        int("whitens" in request.form),
                        request.form["name"],
                    ),
                )

            elif action == "delete":
                # Delete detergent
                cursor.execute("DELETE FROM detergent WHERE name = ?;", (request.form["name"],))

            elif action == "rename":
                # Rename detergent
                cursor.execute(
                    "UPDATE detergent SET name = ? WHERE name = ?;",
                    (request.form["new_name"], request.form["old_name"]),
                )

            elif action == "add_ingredient":
                # Add detergent ingredient and update DetergentComposedOf
                ingredient_name = request.form["ingredient_name"]
                detergent_name = request.form["detergent_name"]

                # Insert ingredient into detergent_ingredient table if not exists
                cursor.execute(
                    "INSERT OR IGNORE INTO detergent_ingredient (name) VALUES (?);",
                    (ingredient_name,)
                )

                # Link detergent and ingredient in DetergentComposedOf table
                cursor.execute(
                    "INSERT INTO DetergentComposedOf (detergent, ingredient) VALUES (?, ?);",
                    (detergent_name, ingredient_name),
                )

            conn.commit()

        # Fetch all detergents
        cursor.execute("SELECT * FROM detergent;")
        detergents = [
            {
                "name": row["name"],
                "for_darks": row["for_darks"],
                "for_lights": row["for_lights"],
                "whitens": row["whitens"],
            }
            for row in cursor.fetchall()
        ]

    return render_template("edit_detergent.html", detergents=detergents)

# Routes for managing cleaners
@app.route("/edit/cleaner", methods=["GET", "POST"])
def edit_cleaner():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            action = request.form.get("action")

            if action == "edit":
                # Edit cleaner's name
                cursor.execute(
                    "UPDATE cleaners SET name = ? WHERE address = ?;",
                    (request.form["name"], request.form["address"]),
                )

            elif action == "delete":
                # Delete cleaner
                cursor.execute("DELETE FROM cleaners WHERE address = ?;", (request.form["address"],))

            conn.commit()

        # Fetch all cleaners
        cursor.execute("SELECT * FROM cleaners;")
        cleaners = [
            {
                "address": row["address"],
                "name": row["name"],
            }
            for row in cursor.fetchall()
        ]

    return render_template("edit_cleaner.html", cleaners=cleaners)

# Route: Manage User Settings
@app.route("/edit/user/<username>", methods=["GET", "POST"])
def edit_user(username):
    error = None
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            action = request.form.get("action")

            if action == "add_allergy":
                ingredient = request.form["ingredient"]
                cursor.execute("SELECT name FROM detergent_ingredient WHERE name = ?;", (ingredient,))
                if cursor.fetchone():
                    cursor.execute("INSERT INTO IsAllergicTo (owner, detergent_ingredient) VALUES (?, ?);", (username, ingredient))
                else:
                    error = "Ingredient does not exist."

            elif action == "add_can_wash":
                washee = request.form["washee"]
                cursor.execute("SELECT name FROM owner WHERE name = ?;", (washee,))
                if cursor.fetchone():
                    cursor.execute("INSERT INTO OwnerCanWash (washer, washee) VALUES (?, ?);", (username, washee))
                else:
                    error = "Person does not exist."

            elif action == "remove_can_wash":
                washee = request.form["washee"]
                cursor.execute("DELETE FROM OwnerCanWash WHERE washer = ? AND washee = ?;", (username, washee))

            elif action == "add_likes":
                cleaner = request.form["cleaner"]
                cursor.execute("SELECT address FROM cleaners WHERE address = ?;", (cleaner,))
                if cursor.fetchone():
                    cursor.execute("INSERT INTO Likes (cleaners, owner) VALUES (?, ?);", (cleaner, username))
                else:
                    error = "Cleaner does not exist."

            conn.commit()

        # Fetch user's allergies
        cursor.execute("SELECT detergent_ingredient FROM IsAllergicTo WHERE owner = ?;", (username,))
        allergies = [row["detergent_ingredient"] for row in cursor.fetchall()]

        # Fetch who the user can wash for
        cursor.execute("SELECT washee FROM OwnerCanWash WHERE washer = ?;", (username,))
        can_wash = [row["washee"] for row in cursor.fetchall()]

        # Fetch user's liked cleaners
        cursor.execute("SELECT cleaners FROM Likes WHERE owner = ?;", (username,))
        liked_cleaners = [row["cleaners"] for row in cursor.fetchall()]

    return render_template(
        "edit_user.html",
        username=username,
        allergies=allergies,
        can_wash=can_wash,
        liked_cleaners=liked_cleaners,
        error=error,
    )

if __name__ == "__main__":
    app.run(debug=True)
