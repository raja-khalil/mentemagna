# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash
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
        msg = Message(
            subject='Nova mensagem de contato - Mente Magna',
            sender=form.email.data,
            recipients=[os.getenv('MAIL_USERNAME')],
            body=f"""
            Nome: {form.nome.data}
            Email: {form.email.data}

            Mensagem:
            {form.mensagem.data}
            """
        )
        mail.send(msg)
        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('main.contato'))
    return render_template('contato.html', title="Contato", form=form)
