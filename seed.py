from app import app
from models import db, Pet
import random

# List of possible species and the default photo URL
species_list = ["dog", "cat", "porcupine"]

# Dictionary with species-specific image lists
species_images = {
    "dog": [
        "images/dog1.jpg",
        "images/dog2.jpg",
        "images/dog3.jpg"
    ],
    "cat": [
        "images/cat1.jpg",
        "images/cat2.jpg",
        "images/cat3.jpg"
    ],
    "porcupine": [
        "images/porcupine1.jpg",
        "images/porcupine2.jpg",
        "images/porcupine3.jpg"
    ]
}

# Default image path
default_photo_url = "images/default_pet_pic.png"

# List of pet names
name_list = ["Rex", "Whiskers", "Fluffy", "Bella", "Max", "Luna", "Charlie", "Buddy", "Milo", "Oliver", "Daisy", "Cleo"]

# Generate some random data for seeding
def generate_random_pet(name):
    species = random.choice(species_list)
    age = random.randint(1, 10)  # Random age between 1 and 10
    notes = random.choice(["Loves playing fetch.", "Very friendly.", "Needs a lot of attention.", "Shy but sweet.", "Great with kids."])

    # Choose a random image for the species
    photo_url = default_photo_url
    if random.random() > 0.5:  # Decide whether to use a default image or a random species-specific image
        photo_url = random.choice(species_images[species])

    pet = Pet(name=name, species=species, age=age, notes=notes, photo_url=photo_url)
    return pet

# Seeding script
with app.app_context():
    # Drop all existing tables and recreate them
    db.drop_all()
    db.create_all()

    # Shuffle the list of names to ensure no duplicates
    random.shuffle(name_list)

    # Generate a list of random pets, using each name from the shuffled list
    pets = [generate_random_pet(name) for name in name_list]  # Creating pets using unique names

    # Add pets to the database
    try:
        db.session.add_all(pets)
        db.session.commit()
        print("Database seeded successfully with random pets!")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print(f"Error seeding the database: {e}")
