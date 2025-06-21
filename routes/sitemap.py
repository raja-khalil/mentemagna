from flask import Blueprint, Response, url_for, request
from models import Post
from datetime import datetime
import xml.etree.ElementTree as ET

sitemap_bp = Blueprint('sitemap', __name__)

@sitemap_bp.route('/sitemap.xml')
def sitemap():
    """Gera sitemap XML dinâmico"""
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Páginas estáticas
    static_routes = ['main.home', 'main.sobre', 'main.produtos', 'main.contato', 'blog.blog', 'solutions.solutions_index']
    for route in static_routes:
        url_element = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url_element, 'loc')
        loc.text = url_for(route, _external=True)
        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    # Posts do blog
    posts = Post.query.filter_by(publicado=True).all()
    for post in posts:
        url_element = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url_element, 'loc')
        loc.text = url_for('blog.post_detail', slug=post.slug, _external=True)
        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = post.data_atualizacao.strftime('%Y-%m-%d') if post.data_atualizacao else post.data_criacao.strftime('%Y-%m-%d')

    xml_str = ET.tostring(urlset, encoding='unicode', method='xml')
    return Response('<?xml version="1.0" encoding="UTF-8"?>' + xml_str, mimetype='application/xml')

@sitemap_bp.route('/robots.txt')
def robots():
    """Gera robots.txt dinâmico"""
    sitemap_url = url_for('sitemap.sitemap', _external=True)
    robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}"
    return Response(robots_content, mimetype='text/plain')