# routes/solutions.py - Sistema modular de soluções
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from seo_helper import get_seo_data
import json

solutions_bp = Blueprint('solutions', __name__, url_prefix='/solucoes')

# --- CONFIGURAÇÃO CENTRAL DE SOLUÇÕES ---
SOLUTIONS_CONFIG = {
    'consulta-cid': {
        'name': 'Consulta CID',
        'description': 'Busque códigos da Classificação Internacional de Doenças (CID-10) de forma rápida e precisa.',
        'icon': '🏥',
        'category': 'Saúde',
        'keywords': ['cid', 'classificação internacional doenças', 'código cid', 'diagnóstico', 'oms'],
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbxeqxH0-ru4NiDqJQYF19pxi1ualySptKZlMdnC219tJJP4F2-KDK7wDiX-nJgztHoz',
        'template': 'solutions/cid.html',
        'status': 'active',
        'featured': True
    },
    'consulta-cbo': {
        'name': 'Consulta CBO',
        'description': 'Consulte códigos da Classificação Brasileira de Ocupações (CBO) e detalhes de profissões.',
        'icon': '👔',
        'category': 'Profissional',
        'keywords': ['cbo', 'classificação brasileira ocupações', 'profissões', 'código cbo', 'mte'],
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbwyGB71MUHmivLgiPwROWaa-AjvsfFe6yD4H9L7jAE57lFjLb3bSu44mkF3u0kohWmd',
        'template': 'solutions/cbo.html',
        'status': 'active',
        'featured': True
    },
    'consulta-sigtap': {
        'name': 'Consulta SIGTAP',
        'description': 'Pesquise procedimentos, medicamentos e OPMs da tabela SIGTAP do SUS (Maio/2025).',
        'icon': '🧾',
        'category': 'Saúde',
        'keywords': ['sigtap', 'sus', 'tabela de procedimentos', 'medicamentos', 'opm', 'saúde pública'],
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbzNzp-V_EWEBhcMSLMaU8SOO0hxhFrto6OpRLl4sGtndvLZS-3SJ-kBoYqNsyCL6W0',
        'template': 'templates/solutions/sigtap.html', # Corrigi o caminho do template
        'status': 'active',
        'featured': True
    },
    'calculadora': {
        'name': 'Calculadora Online',
        'description': 'Calculadora online completa com funções básicas, histórico e interface amigável.',
        'icon': '🧮',
        'category': 'Utilitários',
        'keywords': ['calculadora', 'matemática', 'calcular', 'operações'],
        'type': 'html_js',
        'template': 'templates/solutions/calculadora.html', # Corrigi o caminho do template
        'status': 'active',
        'featured': True
    },
}

@solutions_bp.route('/')
def solutions_index():
    active_solutions = {k: v for k, v in SOLUTIONS_CONFIG.items() if v['status'] == 'active'}
    categories = {}
    for slug, config in active_solutions.items():
        category = config['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({'slug': slug, **config})
    return render_template('solutions/index.html', categories=dict(sorted(categories.items())))

@solutions_bp.route('/<solution_slug>')
def solution_detail(solution_slug):
    solution = SOLUTIONS_CONFIG.get(solution_slug)
    if not solution:
        return render_template('404.html'), 404
    if solution['type'] == 'google_apps_script':
        solution['script_url'] = f"https://script.google.com/macros/s/{solution['deployment_id']}/exec"
    return render_template(solution['template'].replace('templates/', ''), solution=solution)