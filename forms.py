from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField, TextAreaField, FileField
from wtforms.validators import InputRequired, Optional, URL, NumberRange


class AddPetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()])

    species = SelectField(
        "Species", 
        choices=[("cat", "Cat"),
                 ("dog", "Dog"),
                 ("porcupine", "Porcupine")]
    )
    photo_file = FileField("Upload a Photo", validators=[Optional()])

    photo_url = StringField(
        "Photo URL", 
        validators=[Optional(), URL(message="Must be a valid URL")])

    age = IntegerField(
        "Age",
        validators=[Optional(), NumberRange(min=0, max=30, message="Must be between 0 and 30")])

    notes = TextAreaField("Notes", validators=[Optional()])

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False

        if self.photo_url.data and self.photo_file.data:
            self.photo_url.errors.append("Choose either a photo URL or upload a file, not both.")
            self.photo_file.errors.append("Choose either a photo URL or upload a file, not both.")
            return False

        # if not self.photo_url.data and not self.photo_file.data:
        #     self.photo_url.errors.append("You must provide either a photo URL or upload a photo file.")
        #     self.photo_file.errors.append("You must provide either a photo URL or upload a photo file.")
        #     return False

        return True

class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available")
