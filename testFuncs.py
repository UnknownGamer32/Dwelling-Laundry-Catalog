import modifyData
from modifyData import *

# To test if insert works
'''
if __name__ == "__main__":

    db = connect_db() 
    insert_owner(
    name="German D",
    allergies=["Sodium lauryl sulfate", "Bleach"],
    can_wash=["Jane Doe", "Biggie Cheese"],
    liked_cleaners=["Cleaner's R Us"]
    )
    insert_cleaners(
    address="123 Elm st",
    name="Cleaner's R Us",
    supported_systems=[
        ("Washing Machine", "Tide", "Tumble Dry"),
        ("Dry Clean", "Perchloroethylene", "Press")
     ]
    )
    insert_laundry(
        owner="German D",
        description="Gucci Flip Flops",
        location="Laundry basket",
        special_instructions="Scrub with soap & water",
        dirty=True,
        volume=1,
        detergents=["Dove soap"],
        color="black",
    ) # only function without exception "already exists"
    insert_detergent(
        name="Dove soap",
        for_darks=True,
        for_whites=True,
        whitens=False,
        ingredients=["Sodium lauryl sulfate", "Stearic Acid", "Sodium Tallowate"],
        db=db,
    )  
    insert_owner("tester",["H2O","NaOH"],["German D"],["Home"])
    insert_laundry("tester","Rolex watch","Home","do not wash",False,1,["none"],"Gold",) # <- can insert the same thing multiple times
    insert_detergent("OxiBleach",False,True,True,["Sodium hypochlorite","NaOH","Sodium chloride"])
    insert_cleaners("Cathedral Hall","Home", [("Washing Machine", "Oxiclean", "Tumble Dry")])

    db.close()
''' 

# To test if delete works
if __name__ == "__main__":
    db = connect_db()
    #delete_laundry(32) # can delete by id, or laundry & id deleted when owner is gone. 
    delete_detergent("OxiBleach")
    delete_owner("tester")
    delete_cleaners("Cathedral Hall")
    db.close()