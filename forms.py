from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Enviar Mensagem')

class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=5, max=200)])
    # O campo 'conteudo' agora é apenas um TextAreaField, sem validação DataRequired
    conteudo = TextAreaField('Conteúdo')
    resumo = TextAreaField('Resumo (para SEO)', validators=[Optional(), Length(max=300)])
    imagem = FileField('Imagem de Destaque', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    publicado = BooleanField('Publicar', default=True)
    submit = SubmitField('Salvar Post')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Entrar')