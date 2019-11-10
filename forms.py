from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flaskblog.secrets_poster import main,first_run

class PostForm(FlaskForm):
    hashtag = StringField('Hashtag', validators=[DataRequired()],default="hashtag")
    content = TextAreaField('Content', validators=[DataRequired()],default="text")
    post = SubmitField('Post secret')
    archive = SubmitField('Move to archive')
    change_hashtag = SubmitField('Change hashtag')
    admin_edit = StringField('[αδμιν εδιτ]:')
