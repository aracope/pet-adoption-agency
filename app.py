from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import os
from werkzeug.utils import secure_filename

# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize Debug Toolbar and database
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
        # Get data from the form
        photo_url = form.photo_url.data
        photo_file = form.photo_file.data

        # If a file is uploaded
        if photo_file:
            filename = secure_filename(photo_file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo_file.save(upload_path)
            photo_url = url_for('static', filename=f'uploads/{filename}')

        # If no photo URL or file is provided, use the default image
        if not photo_url:
            photo_url = url_for('static', filename="images/default_pet_pic.png")

        # Now create the Pet object
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=photo_url,
            age=form.age.data,
            notes=form.notes.data,
            available=True
        )

        db.session.add(new_pet)
        db.session.commit()

        flash(f"{new_pet.name} added successfully!", "success")
        return redirect(url_for("show_homepage"))
    
    return render_template("add_pet.html", form=form)

@app.route("/pets/<int:pet_id>", methods=["GET", "POST"])
def show_edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        form.populate_obj(pet)  # updates pet with form data
        db.session.commit()
        flash("Pet updated successfully!", "success")
        return redirect(url_for("show_homepage"))

    return render_template("pet_detail.html", pet=pet, form=form)
