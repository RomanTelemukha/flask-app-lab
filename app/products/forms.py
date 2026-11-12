from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(min=3, message="Назва повинна містити щонайменше 3 символи")
        ]
    )
    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Це поле є обов'язковим")
        ],
        render_kw={"rows": 5, "cols": 40}
    )
    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            InputRequired(message="Вкажіть ціну"),
            NumberRange(min=0.01, message="Ціна повинна бути додатною")
        ]
    )
    category = SelectField(
        "Категорія",
        choices=[
            ("Ноутбуки", "Ноутбуки"),
            ("Смартфони", "Смартфони"),
            ("Комп'ютери", "Комп'ютери"),
            ("Аксесуари", "Аксесуари")
        ],
        validators=[
            DataRequired(message="Оберіть категорію")
        ]
    )
    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Вкажіть кількість"),
            NumberRange(min=0, message="Кількість не може бути від'ємною")
        ],
        default=0
    )
    image = FileField(
        "Зображення",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Дозволені лише формати JPG, JPEG та PNG")
        ]
    )
    submit = SubmitField("Зберегти")
