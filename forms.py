from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=10, max=1000)])
    enviar = SubmitField('Enviar Mensagem')

class PostForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(min=5, max=200)])
    conteudo = TextAreaField('Conteudo', validators=[DataRequired(), Length(min=10)])
    resumo = TextAreaField('Resumo', validators=[Optional(), Length(max=300)])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    publicado = BooleanField('Publicar', default=True)
    submit = SubmitField('Salvar Post')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Entrar')
