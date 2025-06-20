 # MenteMagna

**Site institucional em Flask** com blog, painel administrativo, autenticação, CKEditor 5, Google AdSense e contato por e-mail.

---

## 🔖 Visão Geral

O **MenteMagna** é um projeto em Flask para apresentação de serviços/produtos e blog integrado, com:

* Front-end responsivo com **Bootstrap 5**
* Editor WYSIWYG **CKEditor 5** com upload de arquivos
* Banco de dados **SQLite** (podendo migrar para outro SGBD)
* **Autenticação** de administrador via Flask-Login
* **Painel Admin** para CRUD de posts
* **Monetização** com Google AdSense nos templates
* **Formulário de Contato** enviando e-mail via Flask-Mail (Gmail)
* **Migrações** de banco com Flask-Migrate
* Configuração por ambiente em **config.py**

---

## 🚀 Funcionalidades

1. **Áreas Públicas**

   * Páginas: Início, Sobre, E-Magna, Produtos, Soluções, Blog, Contato
   * Carrosséis de destaques e posts na Home
   * Listagem e detalhe de posts no Blog
   * Formulário de contato com validação e envio de e-mail
   * Blocos de anúncios AdSense em vários pontos

2. **Painel Administrativo**

   * **Login** para administrador (`/auth/login`)
   * Dashboard com lista de posts publicados
   * Editor de posts com CKEditor (upload de imagem/mp4)
   * Rota de upload aproveitada pelo CKEditor (`/admin/upload`)
   * Protegido por sessão Flask-Login (`/admin/*`)

3. **Desenvolvimento e Deploy**

   * Configurações separadas para **development** e **production**
   * Variáveis de ambiente em arquivo `.env`
   * Estrutura de pastas clara e modular

---

## 📋 Pré-requisitos

* Python 3.10+
* Git
* Conta Google/Gmail (para envio de e-mail e AdSense)
* (Opcional) Virtualenv

---

## ⚙️ Instalação

1. **Clone o repositório**

   ```bash
   git clone git@github.com:raja-khalil/mentemagna.git
   cd mentemagna
   ```

2. **Crie e ative um virtualenv**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate    # Windows
   ```

3. **Instale dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente**

   * Copie `.env.example` para `.env`
   * Edite as chaves:

     ```ini
     FLASK_ENV=development
     SECRET_KEY=sua_chave_secreta
     MAIL_SERVER=smtp.gmail.com
     MAIL_PORT=587
     MAIL_USE_TLS=True
     MAIL_USERNAME=seu.email@gmail.com
     MAIL_PASSWORD=sua_senha_app  # caso use App Password do Gmail
     ```

5. **Prepare o banco de dados**

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Crie usuário administrador**

   ```bash
   flask shell
   >>> from extensions import db
   >>> from models import User
   >>> u = User(username='admin')
   >>> u.set_password('sua_senha')
   >>> db.session.add(u)
   >>> db.session.commit()
   >>> exit()
   ```

7. **Execute a aplicação**

   ```bash
   python run.py
   ```

   Acesse: `http://localhost:5000/`

---

## 📂 Estrutura de Pastas

```
mentemagna/
├─ admin/                 # Blueprint do painel admin
│  ├─ routes.py
│  └─ templates/admin/    # templates do admin
├─ routes/
│  ├─ main.py             # rotas públicas
│  └─ blog.py             # rotas do blog
├─ templates/             # templates globais
│  ├─ auth/               # login/logout
│  ├─ blog/               # blog.html, post.html
│  └─ public/             # home.html, sobre.html, etc.
├─ static/                # CSS, JS, imagens, uploads
├─ migrations/            # arquivos de migração
├─ instance/              # database.db e uploads locais
├─ extensions.py          # instâncias de extensões
├─ config.py              # configurações por ambiente
├─ models.py              # models Post e User
├─ forms.py               # ContatoForm, PostForm, LoginForm
├─ run.py                 # application factory
├─ requirements.txt
└─ .env                   # variáveis de ambiente
```

---

## 🔒 Segurança e Boas Práticas

* **Não** versionar o arquivo `.env` (já inclui `.gitignore`)
* Use **App Password** no Gmail em vez da sua senha principal
* Configure **HTTPS** em produção (SSL/TLS)
* Mantenha dependências atualizadas

---

## 🛣️ Próximos Passos

* Implementar paginação e busca no Blog
* Adicionar sitemap.xml e robots.txt
* Integrar Google Analytics e consentimento de cookies
* Melhorar SEO (Open Graph, metatags dinâmicas)
* Testes automatizados com `pytest`

---

**Desenvolvido por Raja Khalil**

