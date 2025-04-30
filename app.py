from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)

from models import Pet
from forms import AddPetForm, EditPetForm

@app.route("/")
def show_homepage():
    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        new_pet = Pet(
            # Grab form data
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data or None,
            age=form.age.data or None,
            notes=form.notes.data or None
        )

        db.session.add(new_pet)
        db.session.commit()

        flash(f"{new_pet.name} added successfully!", "success")
        return redirect(url_for("show_homepage"))
    else:
        print("Form did not validate:", form.errors)
    
    return render_template("add_pet.html", form=form)

@app.route("/pets/<int:pet_id>", methods=["GET", "POST"])
def show_edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash("Pet updated successfully!", "success")
        return redirect(url_for("show_homepage"))

    return render_template("pet_detail.html", pet=pet, form=form)
