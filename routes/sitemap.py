# routes/sitemap.py - Sitemap automático para SEO
from flask import Blueprint, Response, url_for, request
from models import Post
from datetime import datetime
import xml.etree.ElementTree as ET

sitemap_bp = Blueprint('sitemap', __name__)

@sitemap_bp.route('/sitemap.xml')
def sitemap():
    """Gera sitemap XML dinâmico"""
    
    # Criar elemento raiz
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:news', 'http://www.google.com/schemas/sitemap-news/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
    urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    
    # URL base do site
    base_url = request.url_root.rstrip('/')
    
    # Páginas estáticas - ordenadas por prioridade
    static_pages = [
        {
            'url': url_for('main.home', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0'
        },
        {
            'url': url_for('blog.blog', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '0.9'
        },
        {
            'url': url_for('main.sobre', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'url': url_for('main.produtos', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8'
        },
        {
            'url': url_for('main.emagna', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8'
        },
        {
            'url': url_for('main.contato', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.7'
        },
        {
            'url': url_for('main.termos', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'yearly',
            'priority': '0.3'
        },
        {
            'url': url_for('main.privacidade', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'yearly',
            'priority': '0.3'
        },
        {
            'url': url_for('main.aviso_legal', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'yearly',
            'priority': '0.3'
        },
        {
            'url': url_for('main.cookies', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'yearly',
            'priority': '0.3'
        }
    ]
    
    # Adicionar páginas estáticas
    for page in static_pages:
        url_element = ET.SubElement(urlset, 'url')
        
        loc = ET.SubElement(url_element, 'loc')
        loc.text = page['url']
        
        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = page['lastmod']
        
        changefreq = ET.SubElement(url_element, 'changefreq')
        changefreq.text = page['changefreq']
        
        priority = ET.SubElement(url_element, 'priority')
        priority.text = page['priority']
    
    # Posts do blog - dinâmicos
    try:
        posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).all()
        
        for post in posts:
            url_element = ET.SubElement(urlset, 'url')
            
            # URL do post
            loc = ET.SubElement(url_element, 'loc')
            loc.text = url_for('blog.post_detail', slug=post.slug, _external=True)
            
            # Data de modificação
            lastmod = ET.SubElement(url_element, 'lastmod')
            lastmod.text = post.data_criacao.strftime('%Y-%m-%d')
            
            # Frequência de mudança
            changefreq = ET.SubElement(url_element, 'changefreq')
            changefreq.text = 'weekly'
            
            # Prioridade
            priority = ET.SubElement(url_element, 'priority')
            priority.text = '0.8'
            
            # Imagem do post (se existir)
            if post.imagem:
                image = ET.SubElement(url_element, 'image:image')
                image_loc = ET.SubElement(image, 'image:loc')
                image_loc.text = base_url + post.imagem
                
                image_title = ET.SubElement(image, 'image:title')
                image_title.text = post.titulo
                
                image_caption = ET.SubElement(image, 'image:caption')
                image_caption.text = post.resumo or post.titulo
            
            # News markup para posts recentes (últimos 2 dias)
            dias_desde_publicacao = (datetime.now() - post.data_criacao).days
            if dias_desde_publicacao <= 2:
                news = ET.SubElement(url_element, 'news:news')
                publication = ET.SubElement(news, 'news:publication')
                
                pub_name = ET.SubElement(publication, 'news:name')
                pub_name.text = 'Mente Magna'
                
                pub_language = ET.SubElement(publication, 'news:language')
                pub_language.text = 'pt'
                
                pub_date = ET.SubElement(news, 'news:publication_date')
                pub_date.text = post.data_criacao.strftime('%Y-%m-%d')
                
                title = ET.SubElement(news, 'news:title')
                title.text = post.titulo
                
    except Exception as e:
        # Se houver erro com posts, continua sem eles
        print(f"Erro ao gerar sitemap de posts: {e}")
    
    # Converter para string XML
    xml_str = ET.tostring(urlset, encoding='unicode', method='xml')
    
    # Adicionar declaração XML
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content = xml_declaration + xml_str
    
    # Retornar resposta XML
    response = Response(xml_content, mimetype='application/xml')
    response.headers['Cache-Control'] = 'max-age=3600'  # Cache por 1 hora
    
    return response

@sitemap_bp.route('/robots.txt')
def robots():
    """Gera robots.txt dinâmico"""
    
    base_url = request.url_root.rstrip('/')
    
    robots_content = f"""User-agent: *
Allow: /

# Permitir bots de busca importantes
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

# Bloquear áreas administrativas
Disallow: /admin/
Disallow: /auth/
Disallow: /static/uploads/
Disallow: *.pdf$
Disallow: *.doc$
Disallow: *.docx$

# Permitir CSS e JS para renderização
Allow: /static/css/
Allow: /static/js/
Allow: /static/img/

# Sitemap
Sitemap: {base_url}/sitemap.xml

# Informações adicionais
# Crawl-delay: 1
# Visit-time: 0100-0800

# Este site está em conformidade com:
# - LGPD (Lei Geral de Proteção de Dados)
# - Políticas do Google AdSense
# - Diretrizes de SEO do Google
"""
    
    response = Response(robots_content, mimetype='text/plain')
    response.headers['Cache-Control'] = 'max-age=86400'  # Cache por 24 horas
    
    return response

@sitemap_bp.route('/sitemap-index.xml')
def sitemap_index():
    """Sitemap index para sites grandes (futuro)"""
    
    base_url = request.url_root.rstrip('/')
    
    # Criar elemento raiz
    sitemapindex = ET.Element('sitemapindex')
    sitemapindex.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Sitemap principal
    sitemap = ET.SubElement(sitemapindex, 'sitemap')
    loc = ET.SubElement(sitemap, 'loc')
    loc.text = f"{base_url}/sitemap.xml"
    
    lastmod = ET.SubElement(sitemap, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    # Converter para string XML
    xml_str = ET.tostring(sitemapindex, encoding='unicode', method='xml')
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content = xml_declaration + xml_str
    
    return Response(xml_content, mimetype='application/xml')

@sitemap_bp.route('/sitemap-posts.xml')
def sitemap_posts():
    """Sitemap específico para posts (para sites com muitos posts)"""
    
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    
    try:
        posts = Post.query.filter_by(publicado=True).order_by(Post.data_criacao.desc()).limit(1000).all()
        
        for post in posts:
            url_element = ET.SubElement(urlset, 'url')
            
            loc = ET.SubElement(url_element, 'loc')
            loc.text = url_for('blog.post_detail', slug=post.slug, _external=True)
            
            lastmod = ET.SubElement(url_element, 'lastmod')
            lastmod.text = post.data_criacao.strftime('%Y-%m-%d')
            
            changefreq = ET.SubElement(url_element, 'changefreq')
            changefreq.text = 'weekly'
            
            priority = ET.SubElement(url_element, 'priority')
            priority.text = '0.8'
            
            if post.imagem:
                image = ET.SubElement(url_element, 'image:image')
                image_loc = ET.SubElement(image, 'image:loc')
                image_loc.text = request.url_root.rstrip('/') + post.imagem
                
                image_title = ET.SubElement(image, 'image:title')
                image_title.text = post.titulo
                
    except Exception as e:
        print(f"Erro ao gerar sitemap de posts: {e}")
    
    xml_str = ET.tostring(urlset, encoding='unicode', method='xml')
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content = xml_declaration + xml_str
    
    return Response(xml_content, mimetype='application/xml')