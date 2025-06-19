# models.py
from datetime import datetime
from slugify import slugify
from extensions import db  # IMPORTANTE: importar db de extensions, não recriar!

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True)
    resumo = db.Column(db.Text)
    conteudo = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(200))
    publicado = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug:
            self.slug = slugify(self.titulo)
        # opcional: gerar resumo automático
        if not self.resumo:
            plain = (self.conteudo or "").replace('<', '').replace('>', '')
            self.resumo = (plain[:200] + '...') if len(plain) > 200 else plain
