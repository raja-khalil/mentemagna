# seo_helper.py - Sistema de SEO dinâmico simplificado
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class SEOData:
    """Classe para dados de SEO de uma página"""
    title: str
    description: str
    keywords: List[str]
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    canonical_url: Optional[str] = None
    schema_type: str = "WebPage"

class SEOManager:
    """Gerenciador de SEO dinâmico para o site"""
    
    def __init__(self):
        self.base_keywords = [
            "tecnologia", "programação", "python", "flask", "desenvolvimento web",
            "inteligência artificial", "machine learning", "chatgpt", "inovação",
            "tutorial", "blog tech", "desenvolvedor", "código", "software"
        ]
        
        # Templates de SEO por tipo de página
        self.seo_templates = {
            "home": {
                "title": "Mente Magna - Portal de Tecnologia, Programação e Inovação",
                "description": "Portal de referência em tecnologia, programação, IA e inovação. Artigos, tutoriais, ferramentas e insights para desenvolvedores e entusiastas de tecnologia.",
                "keywords": self.base_keywords + ["portal tecnologia", "blog programação", "tutoriais desenvolvimento"]
            },
            "blog_list": {
                "title": "Blog - Mente Magna | Artigos sobre Tecnologia e Programação",
                "description": "Artigos sobre tecnologia, programação, inteligência artificial e desenvolvimento. Tutoriais práticos, análises e insights para desenvolvedores.",
                "keywords": self.base_keywords + ["blog tecnologia", "artigos programação", "tutoriais desenvolvimento"]
            },
            "tool": {
                "title_template": "{tool_name} - Ferramenta Online Gratuita | Mente Magna",
                "description_template": "{tool_description}. Ferramenta online gratuita, rápida e segura. Use agora sem cadastro!",
                "keywords_base": self.base_keywords + ["ferramenta online", "calculadora", "grátis"]
            }
        }
    
    def get_post_seo(self, post_title: str, post_content: str, post_excerpt: str = None) -> SEOData:
        """Gera SEO para posts individuais"""
        # Gerar descrição
        description = post_excerpt or (post_content[:160] + "..." if len(post_content) > 160 else post_content)
        # Remove HTML básico
        description = description.replace('<', '').replace('>', '')
        
        return SEOData(
            title=f"{post_title} - Mente Magna",
            description=description,
            keywords=self.base_keywords + [post_title.lower()],
            schema_type="Article"
        )
    
    def get_tool_seo(self, tool_name: str, tool_description: str, tool_type: str) -> SEOData:
        """Gera SEO para ferramentas/calculadoras"""
        tool_keywords = {
            "calculadora": ["calculadora online", "calcular", "matemática", "fórmulas"],
            "cid": ["cid", "classificação internacional doenças", "código cid", "diagnóstico"],
            "cbo": ["cbo", "classificação brasileira ocupações", "profissões", "código cbo"],
        }
        
        specific_keywords = tool_keywords.get(tool_type, [])
        
        return SEOData(
            title=f"{tool_name} - Ferramenta Online Gratuita | Mente Magna",
            description=f"{tool_description}. Ferramenta online gratuita, rápida e segura. Use agora sem cadastro!",
            keywords=self.base_keywords + ["ferramenta online", "grátis", "calculadora"] + specific_keywords,
            schema_type="WebApplication"
        )

# Instância global do SEO Manager
seo_manager = SEOManager()

# Função helper para templates
def get_seo_data(page_type: str, **kwargs) -> Dict:
    """Função helper para usar nos templates"""
    if page_type == "post":
        seo_data = seo_manager.get_post_seo(
            kwargs.get('post_title', ''),
            kwargs.get('post_content', ''),
            kwargs.get('post_excerpt', '')
        )
    elif page_type == "tool":
        seo_data = seo_manager.get_tool_seo(
            kwargs.get('tool_name', ''),
            kwargs.get('tool_description', ''),
            kwargs.get('tool_type', '')
        )
    else:
        # Default home page
        template = seo_manager.seo_templates.get("home", {})
        seo_data = SEOData(
            title=template.get("title", "Mente Magna"),
            description=template.get("description", "Portal de tecnologia e inovação"),
            keywords=template.get("keywords", seo_manager.base_keywords)
        )
    
    return {
        'page_title': seo_data.title,
        'page_description': seo_data.description,
        'page_keywords': ', '.join(seo_data.keywords),
        'og_title': seo_data.og_title or seo_data.title,
        'og_description': seo_data.og_description or seo_data.description,
        'schema_type': seo_data.schema_type
    }