# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, BooleanField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed


class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = CKEditorField('Mensagem', validators=[DataRequired()])
    enviar = SubmitField('Enviar')


class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    conteudo = CKEditorField('Conteúdo', validators=[DataRequired()])
    imagem = FileField('Imagem principal', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas.')
    ])
    publicado = BooleanField('Publicar agora', default=True)
    enviar = SubmitField('Publicar')
