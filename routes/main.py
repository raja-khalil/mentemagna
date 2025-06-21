# routes/main.py - Rotas Principais Corrigidas
from flask import Blueprint, render_template, redirect, url_for, flash, request
from forms import ContatoForm
from flask_mail import Message
from extensions import mail
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html', title="Início")

@main_bp.route('/sobre')
def sobre():
    return render_template('sobre.html', title="Sobre")

@main_bp.route('/produtos')
def produtos():
    return render_template('produtos.html', title="Produtos")

@main_bp.route('/emagna')
def emagna():
    return render_template('emagna.html', title="E-Magna")

@main_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject='Nova mensagem de contato - Mente Magna',
                sender=form.email.data,
                recipients=[os.getenv('MAIL_USERNAME', 'contato@mentemagna.com')],
                body=f"""
Nova mensagem recebida do site Mente Magna:

Nome: {form.nome.data}
Email: {form.email.data}

Mensagem:
{form.mensagem.data}

---
Enviado automaticamente pelo sistema do Mente Magna
                """
            )
            mail.send(msg)
            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('main.contato'))
        except Exception as e:
            flash(f'Erro ao enviar mensagem: {str(e)}. Tente novamente.', 'error')
    
    return render_template('contato.html', title="Contato", form=form)

# Páginas Legais (LGPD e Google)
@main_bp.route('/termos')
def termos():
    return render_template('legal/termos.html', title="Condições Gerais")

@main_bp.route('/aviso-legal')
def aviso_legal():
    return render_template('legal/aviso-legal.html', title="Aviso Legal")

@main_bp.route('/privacidade')
def privacidade():
    return render_template('legal/privacidade.html', title="Política de Privacidade")

@main_bp.route('/cookies')
def cookies():
    return render_template('legal/cookies.html', title="Política de Cookies")