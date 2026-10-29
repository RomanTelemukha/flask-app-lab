from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(min=4, max=10, message="Довжина імені повинна бути від 4 до 10 символів")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Email(message="Некоректний формат email")
        ]
    )
    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Regexp(r"^\+380\d{9}$", message="Формат телефону повинен бути +380XXXXXXXXX")
        ]
    )
    subject = SelectField(
        "Тема повідомлення",
        choices=[
            ("general", "Загальні питання"),
            ("support", "Технічна підтримка"),
            ("collaboration", "Співпраця"),
            ("feedback", "Відгук")
        ],
        validators=[
            DataRequired(message="Оберіть тему")
        ]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(max=500, message="Довжина повідомлення повинна бути до 500 символів")
        ]
    )
    submit = SubmitField("Send Message")
