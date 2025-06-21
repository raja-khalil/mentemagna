# forms.py - Formulários Corrigidos

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=10, max=1000)])
    enviar = SubmitField('Enviar Mensagem')

class PostForm(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(min=5, max=200)])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired(), Length(min=10)])
    resumo = TextAreaField('Resumo (Opcional - para SEO)', validators=[Length(max=300)])
    imagem = FileField(
        'Imagem de Destaque',
        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Somente imagens permitidas!')]
    )
    publicado = BooleanField('Publicar Imediatamente', default=True)
    submit = SubmitField('Salvar Post')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Entrar')