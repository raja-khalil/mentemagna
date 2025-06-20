# forms_working.py - Versão sem CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()], render_kw={"rows": 6})
    enviar = SubmitField('Enviar')

class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()], render_kw={"rows": 10})
    imagem = FileField(
        'Imagem principal',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas.')]
    )
    publicado = BooleanField('Publicar agora', default=True)
    enviar = SubmitField('Publicar')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')