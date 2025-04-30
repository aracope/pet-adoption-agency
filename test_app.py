import os
import pytest
from app import app, db
from models import Pet
from forms import AddPetForm, EditPetForm


os.environ['FLASK_ENV'] = 'testing'

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test'
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for form testing

@pytest.fixture
def client():
    """Create a test client and initialize a clean test DB."""

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Add a sample pet
            pet = Pet(name="Whiskey", species="cat", available=True)
            db.session.add(pet)
            db.session.commit()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_homepage_lists_pets(client):
    """Homepage should show sample pet."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Whiskey" in response.data

def test_add_pet_form(client):
    data = {
        "name": "Fido",
        "species": "dog",
        "photo_url": "",
        "age": "2",
        "notes": "",
    }
    response = client.post("/add", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Fido added successfully!" in response.data
    assert b"Fido" in response.data

def test_edit_pet(client):
    """Test editing a pet's profile."""
    with app.app_context():
        pet = Pet.query.first()
        assert pet is not None

    response = client.post(
        f"/pets/{pet.id}",
        data={
        "photo_url": "http://example.com/photo.jpg",
        "notes": "Loves belly rubs",
        "available": "y"
    }, follow_redirects=True)

    # Check the response
    assert response.status_code == 200
    assert b"updated successfully" in response.data

    # Check the DB for actual changes
    with app.app_context():
        updated_pet = Pet.query.get(pet.id)
        assert updated_pet.photo_url == "http://example.com/photo.jpg"
        assert updated_pet.notes == "Loves belly rubs"
        assert updated_pet.available is True
