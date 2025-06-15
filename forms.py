# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    mensagem = CKEditorField('Mensagem', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    conteudo = CKEditorField('Conteúdo', validators=[DataRequired()])
    imagem = FileField('Imagem principal')
    enviar = SubmitField('Publicar')
