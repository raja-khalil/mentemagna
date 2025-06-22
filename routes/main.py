from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from forms import ContatoForm
from extensions import mail
from flask_mail import Message
from models import Post
from routes.solutions import SOLUTIONS_CONFIG

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Buscando os 3 posts mais recentes para exibir na home
    latest_posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).limit(3).all()
    # Pega as soluções para exibir na home
    featured_solutions = {k: v for k, v in SOLUTIONS_CONFIG.items() if v['status'] == 'active' and v.get('featured', False)}
    return render_template('home.html', title="Página Inicial", posts=latest_posts, solutions=featured_solutions)

@main_bp.route('/sobre')
def sobre():
    return render_template('sobre.html', title="Sobre Nós")

@main_bp.route('/produtos')
def produtos():
    return render_template('produtos.html', title="Produtos")

@main_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        try:
            msg = Message("Nova Mensagem do Site - Mente Magna",
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[current_app.config['MAIL_USERNAME']])
            msg.body = f"""
            De: {form.nome.data} <{form.email.data}>
            ---
            {form.mensagem.data}
            """
            mail.send(msg)
            flash('Sua mensagem foi enviada com sucesso!', 'success')
            return redirect(url_for('main.contato'))
        except Exception as e:
            flash(f'Ocorreu um erro ao enviar sua mensagem: {e}', 'danger')
    return render_template('contato.html', title="Contato", form=form)

# Rotas para páginas legais
@main_bp.route('/termos')
def termos():
    return render_template('legal/termos.html', title="Condições Gerais")

@main_bp.route('/privacidade')
def privacidade():
    return render_template('legal/privacidade.html', title="Política de Privacidade")

@main_bp.route('/cookies')
def cookies():
    return render_template('legal/cookies.html', title="Política de Cookies")

@main_bp.route('/aviso-legal')
def aviso_legal():
    return render_template('legal/aviso-legal.html', title="Aviso Legal")

# ROTA ADICIONADA PARA A LANDING PAGE DO LIVRO
@main_bp.route('/produtos/maquinas-inteligentes-decisoes-humanas')
def produto_maquinas_inteligentes():
    """Exibe a landing page do livro."""
    return render_template('products/maquinas-inteligentes.html', title="Livro: Máquinas Inteligentes, Decisões Humanas")