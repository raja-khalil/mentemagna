from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from forms import ContatoForm
from extensions import mail
from flask_mail import Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home(): return render_template('home.html', title="Página Inicial")

@main_bp.route('/sobre')
def sobre(): return render_template('sobre.html', title="Sobre Nós")

@main_bp.route('/produtos')
def produtos(): return render_template('produtos.html', title="Produtos")

@main_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        try:
            msg = Message("Nova Mensagem do Site",
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
def termos(): return render_template('legal/termos.html')

@main_bp.route('/privacidade')
def privacidade(): return render_template('legal/privacidade.html')