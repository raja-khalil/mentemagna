# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed # <-- ADICIONADO "FileField" AQUI
from flask_ckeditor import CKEditorField

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    enviar = SubmitField('Enviar Mensagem')

class PostForm(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired()])
    conteudo = CKEditorField('Conteúdo', validators=[DataRequired()])
    resumo = TextAreaField('Resumo (Opcional - para SEO)')
    imagem = FileField(
        'Imagem de Destaque',
        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Somente imagens!')]
    )
    publicado = BooleanField('Publicar Imediatamente', default=True)
    submit = SubmitField('Salvar Post')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')