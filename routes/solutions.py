# routes/solutions.py - Sistema modular de soluções
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from seo_helper import get_seo_data
import json

solutions_bp = Blueprint('solutions', __name__, url_prefix='/solucoes')

# Configuração das soluções disponíveis
SOLUTIONS_CONFIG = {
    'consulta-cid': {
        'name': 'Consulta CID',
        'description': 'Busque códigos CID (Classificação Internacional de Doenças) de forma rápida e precisa',
        'icon': '🏥',
        'category': 'Saúde',
        'keywords': ['cid', 'classificação internacional doenças', 'código cid', 'diagnóstico'],
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbxeqxH0-ru4NiDqJQYF19pxi1ualySptKZlMdnC219tJJP4F2-KDK7wDiX-nJgztHoz',
        'template': 'solutions/cid.html',
        'status': 'active',
        'featured': True
    },
    'consulta-cbo': {
        'name': 'Consulta CBO',
        'description': 'Consulte códigos CBO (Classificação Brasileira de Ocupações) e profissões',
        'icon': '👔',
        'category': 'Profissional',
        'keywords': ['cbo', 'classificação brasileira ocupações', 'profissões', 'código cbo'],
        'type': 'google_apps_script',
        'deployment_id': 'AKfycbwyGB71MUHmivLgiPwROWaa-AjvsfFe6yD4H9L7jAE57lFjLb3bSu44mkF3u0kohWmd',
        'template': 'solutions/cbo.html',
        'status': 'active',
        'featured': True
    },
    'calculadora': {
        'name': 'Calculadora Online',
        'description': 'Calculadora online completa com funções básicas e avançadas',
        'icon': '🧮',
        'category': 'Matemática',
        'keywords': ['calculadora', 'matemática', 'calcular', 'operações'],
        'type': 'html_js',
        'template': 'solutions/calculadora.html',
        'status': 'active',
        'featured': True
    },
    'conversor-unidades': {
        'name': 'Conversor de Unidades',
        'description': 'Converta unidades de medida: comprimento, peso, temperatura, área e volume',
        'icon': '⚖️',
        'category': 'Conversores',
        'keywords': ['conversor', 'unidades', 'medidas', 'conversão'],
        'type': 'html_js',
        'template': 'solutions/conversor.html',
        'status': 'development',
        'featured': False
    },
    'gerador-senha': {
        'name': 'Gerador de Senhas',
        'description': 'Gere senhas seguras e personalizadas com diferentes critérios de segurança',
        'icon': '🔐',
        'category': 'Segurança',
        'keywords': ['gerador senha', 'senha segura', 'password generator'],
        'type': 'html_js',
        'template': 'solutions/gerador_senha.html',
        'status': 'development',
        'featured': False
    },
    'validador-cpf': {
        'name': 'Validador de CPF',
        'description': 'Valide números de CPF e verifique se estão corretos',
        'icon': '🆔',
        'category': 'Validadores',
        'keywords': ['validador cpf', 'verificar cpf', 'cpf válido'],
        'type': 'html_js',
        'template': 'solutions/validador_cpf.html',
        'status': 'development',
        'featured': False
    },
    'imc': {
        'name': 'Calculadora de IMC',
        'description': 'Calcule seu Índice de Massa Corporal (IMC) e veja sua classificação',
        'icon': '⚕️',
        'category': 'Saúde',
        'keywords': ['imc', 'índice massa corporal', 'peso ideal', 'saúde'],
        'type': 'html_js',
        'template': 'solutions/imc.html',
        'status': 'development',
        'featured': False
    },
    'juros-compostos': {
        'name': 'Calculadora de Juros Compostos',
        'description': 'Calcule rendimentos com juros compostos para investimentos',
        'icon': '💰',
        'category': 'Financeiro',
        'keywords': ['juros compostos', 'investimento', 'rendimento', 'financeiro'],
        'type': 'python_flask',
        'template': 'solutions/juros_compostos.html',
        'status': 'development',
        'featured': False
    }
}

@solutions_bp.route('/')
def solutions_index():
    """Página principal das soluções"""
    # Filtrar apenas soluções ativas
    active_solutions = {k: v for k, v in SOLUTIONS_CONFIG.items() if v['status'] == 'active'}
    
    # Agrupar soluções por categoria
    categories = {}
    featured_solutions = []
    
    for solution_slug, solution_config in active_solutions.items():
        # Adicionar slug à configuração
        solution_config['slug'] = solution_slug
        
        # Soluções em destaque
        if solution_config.get('featured', False):
            featured_solutions.append({
                'slug': solution_slug,
                **solution_config
            })
        
        # Agrupar por categoria
        category = solution_config['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'slug': solution_slug,
            **solution_config
        })
    
    # SEO para página de soluções
    seo_data = get_seo_data('tool', 
                           tool_name='Soluções Online Gratuitas',
                           tool_description='Coleção de soluções online gratuitas: consulta CID, CBO, calculadoras, conversores e utilitários',
                           tool_type='soluções')
    
    return render_template('solutions/index.html', 
                         categories=categories,
                         featured_solutions=featured_solutions,
                         solutions_count=len(active_solutions),
                         **seo_data)

@solutions_bp.route('/<solution_slug>')
def solution_detail(solution_slug):
    """Página individual de cada solução"""
    if solution_slug not in SOLUTIONS_CONFIG:
        return render_template('solutions/404.html'), 404
    
    solution = SOLUTIONS_CONFIG[solution_slug]
    
    # Verificar se a solução está ativa
    if solution['status'] != 'active':
        return render_template('solutions/coming_soon.html', solution=solution), 503
    
    # SEO específico da solução
    seo_data = get_seo_data('tool',
                           tool_name=solution['name'],
                           tool_description=solution['description'],
                           tool_type=solution_slug)
    
    # Adicionar dados específicos do Google Apps Script se necessário
    if solution['type'] == 'google_apps_script':
        solution['script_url'] = f"https://script.google.com/macros/s/{solution['deployment_id']}/exec"
    
    return render_template(solution['template'],
                         solution=solution,
                         solution_slug=solution_slug,
                         **seo_data)

@solutions_bp.route('/api/proxy/<solution_slug>')
def proxy_google_script(solution_slug):
    """Proxy para Google Apps Script (contorna CORS se necessário)"""
    if solution_slug not in SOLUTIONS_CONFIG:
        return jsonify({'error': 'Solução não encontrada'}), 404
    
    solution = SOLUTIONS_CONFIG[solution_slug]
    
    if solution['type'] != 'google_apps_script':
        return jsonify({'error': 'Tipo de solução inválido'}), 400
    
    # Construir URL do script
    script_url = f"https://script.google.com/macros/s/{solution['deployment_id']}/exec"
    
    # Passar parâmetros da query string
    params = request.args.to_dict()
    
    try:
        import requests
        response = requests.get(script_url, params=params, timeout=10)
        
        # Retornar resposta do Google Apps Script
        return jsonify({
            'success': True,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao conectar com Google Apps Script: {str(e)}'
        }), 500

@solutions_bp.route('/admin/add_solution', methods=['GET', 'POST'])
def add_solution():
    """Interface para adicionar novas soluções (futuro painel admin)"""
    if request.method == 'POST':
        # Aqui você pode implementar a adição dinâmica de soluções
        # Por enquanto, retorna uma mensagem
        return jsonify({
            'message': 'Funcionalidade em desenvolvimento',
            'info': 'Por enquanto, adicione soluções editando o arquivo routes/solutions.py'
        })
    
    return render_template('solutions/add_solution.html')

# Funções auxiliares

def get_solution_stats():
    """Retorna estatísticas das soluções"""
    total = len(SOLUTIONS_CONFIG)
    active = len([s for s in SOLUTIONS_CONFIG.values() if s['status'] == 'active'])
    development = len([s for s in SOLUTIONS_CONFIG.values() if s['status'] == 'development'])
    
    return {
        'total': total,
        'active': active,
        'development': development,
        'categories': len(set(s['category'] for s in SOLUTIONS_CONFIG.values()))
    }

def search_solutions(query):
    """Busca soluções por termo"""
    if not query or len(query) < 2:
        return []
    
    query_lower = query.lower()
    results = []
    
    for slug, solution in SOLUTIONS_CONFIG.items():
        if solution['status'] != 'active':
            continue
            
        # Buscar em nome, descrição e keywords
        searchable_text = ' '.join([
            solution['name'],
            solution['description'],
            ' '.join(solution['keywords'])
        ]).lower()
        
        if query_lower in searchable_text:
            results.append({
                'slug': slug,
                'name': solution['name'],
                'description': solution['description'],
                'icon': solution['icon'],
                'category': solution['category']
            })
    
    return results[:10]  # Limitar a 10 resultados

@solutions_bp.route('/api/search')
def api_search():
    """API de busca de soluções"""
    query = request.args.get('q', '').strip()
    results = search_solutions(query)
    return jsonify({'results': results})

# Template filters personalizados

@solutions_bp.app_template_filter('solution_type_badge')
def solution_type_badge(solution_type):
    """Retorna badge para tipo de solução"""
    badges = {
        'google_apps_script': '<span class="badge bg-success">Google Apps Script</span>',
        'html_js': '<span class="badge bg-primary">HTML/JS</span>',
        'python_flask': '<span class="badge bg-info">Python/Flask</span>',
        'iframe': '<span class="badge bg-warning">iFrame</span>',
        'api': '<span class="badge bg-secondary">API</span>'
    }
    return badges.get(solution_type, '<span class="badge bg-light">Outro</span>')

@solutions_bp.app_template_filter('solution_status_badge')
def solution_status_badge(status):
    """Retorna badge para status da solução"""
    badges = {
        'active': '<span class="badge bg-success">Ativo</span>',
        'development': '<span class="badge bg-warning">Em Desenvolvimento</span>',
        'maintenance': '<span class="badge bg-danger">Manutenção</span>',
        'deprecated': '<span class="badge bg-secondary">Descontinuado</span>'
    }
    return badges.get(status, '<span class="badge bg-light">Desconhecido</span>')

# Context processor para templates

@solutions_bp.app_context_processor
def inject_solution_stats():
    """Injeta estatísticas das soluções em todos os templates"""
    return {
        'solution_stats': get_solution_stats(),
        'featured_solutions_count': len([s for s in SOLUTIONS_CONFIG.values() 
                                        if s.get('featured', False) and s['status'] == 'active'])
    }