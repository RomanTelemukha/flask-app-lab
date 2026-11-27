from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, SelectMultipleField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

CATEGORIES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other")
]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40})
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date",
        format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"],
        default=datetime.now,
        validators=[Optional()]
    )
    category = SelectField("Category", choices=CATEGORIES, default="news")
    tags = SelectMultipleField("Tags", coerce=int)
    author_id = SelectField("Author", coerce=int)
    submit = SubmitField("Add Post")
