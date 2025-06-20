# seo_helper.py - Sistema de SEO dinâmico e palavras-chave
from dataclasses import dataclass
from typing import List, Dict, Optional
import re

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
        
        # Palavras-chave por categoria
        self.category_keywords = {
            "inteligencia_artificial": [
                "inteligência artificial", "machine learning", "deep learning", 
                "chatgpt", "gpt", "redes neurais", "algoritmos", "ia", 
                "reconhecimento de imagem", "processamento de linguagem natural",
                "computer vision", "tensorflow", "pytorch", "scikit-learn"
            ],
            "programacao": [
                "programação", "python", "javascript", "java", "c++", "php",
                "desenvolvimento", "código", "algoritmos", "estrutura de dados",
                "orientação a objetos", "framework", "biblioteca", "api"
            ],
            "web_development": [
                "desenvolvimento web", "frontend", "backend", "html", "css",
                "javascript", "react", "vue", "angular", "node.js", "flask",
                "django", "laravel", "responsivo", "spa", "pwa"
            ],
            "ferramentas": [
                "calculadora", "ferramentas online", "utilitários", "produtividade",
                "cid", "cbo", "conversores", "geradores", "validadores"
            ],
            "mobile": [
                "desenvolvimento mobile", "android", "ios", "react native",
                "flutter", "kotlin", "swift", "app", "aplicativo móvel"
            ],
            "cloud": [
                "cloud computing", "aws", "azure", "google cloud", "docker",
                "kubernetes", "devops", "ci/cd", "infraestrutura", "serverless"
            ]
        }
        
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
            "category": {
                "title_template": "{category_name} - Blog Mente Magna",
                "description_template": "Artigos e tutoriais sobre {category_name}. Conteúdo especializado em {category_description} para desenvolvedores e entusiastas.",
                "keywords_base": self.base_keywords
            },
            "post": {
                "title_template": "{post_title} - Mente Magna",
                "description_template": "{post_excerpt}",
                "keywords_base": self.base_keywords
            },
            "tool": {
                "title_template": "{tool_name} - Ferramenta Online Gratuita | Mente Magna",
                "description_template": "{tool_description}. Ferramenta online gratuita, rápida e segura. Use agora sem cadastro!",
                "keywords_base": self.base_keywords + ["ferramenta online", "calculadora", "grátis"]
            }
        }
    
    def extract_keywords_from_content(self, content: str, max_keywords: int = 10) -> List[str]:
        """Extrai palavras-chave relevantes do conteúdo"""
        if not content:
            return []
        
        # Remove HTML tags
        clean_content = re.sub(r'<[^>]+>', '', content.lower())
        
        # Lista de palavras-chave técnicas relevantes
        tech_keywords = [
            "python", "javascript", "react", "vue", "angular", "node.js", "flask",
            "django", "api", "rest", "graphql", "database", "sql", "nosql",
            "mongodb", "postgresql", "mysql", "redis", "docker", "kubernetes",
            "aws", "azure", "cloud", "serverless", "microservices", "devops",
            "ci/cd", "git", "github", "artificial intelligence", "machine learning",
            "deep learning", "neural networks", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "data science", "big data",
            "blockchain", "cryptocurrency", "iot", "mobile development",
            "android", "ios", "react native", "flutter", "kotlin", "swift"
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in clean_content and keyword not in found_keywords:
                found_keywords.append(keyword)
                if len(found_keywords) >= max_keywords:
                    break
        
        return found_keywords
    
    def get_category_seo(self, category_slug: str, category_name: str) -> SEOData:
        """Gera SEO para páginas de categoria"""
        category_keywords = self.category_keywords.get(category_slug, [])
        
        description_map = {
            "inteligencia_artificial": "inteligência artificial, machine learning e deep learning",
            "programacao": "programação, algoritmos e desenvolvimento de software",
            "web_development": "desenvolvimento web, frontend e backend",
            "ferramentas": "ferramentas online e utilitários para desenvolvedores",
            "mobile": "desenvolvimento mobile e aplicativos",
            "cloud": "cloud computing e infraestrutura"
        }
        
        category_desc = description_map.get(category_slug, category_name.lower())
        
        return SEOData(
            title=f"{category_name} - Blog Mente Magna",
            description=f"Artigos e tutoriais sobre {category_desc}. Conteúdo especializado para desenvolvedores e entusiastas de tecnologia.",
            keywords=self.base_keywords + category_keywords + [category_name.lower()],
            schema_type="CollectionPage"
        )
    
    def get_post_seo(self, post_title: str, post_content: str, post_excerpt: str = None, category: str = None) -> SEOData:
        """Gera SEO para posts individuais"""
        # Extrair palavras-chave do conteúdo
        content_keywords = self.extract_keywords_from_content(post_content)
        
        # Adicionar palavras-chave da categoria se especificada
        category_keywords = []
        if category:
            category_keywords = self.category_keywords.get(category, [])
        
        # Gerar descrição
        description = post_excerpt or (post_content[:160] + "..." if len(post_content) > 160 else post_content)
        description = re.sub(r'<[^>]+>', '', description)  # Remove HTML
        
        all_keywords = list(set(self.base_keywords + content_keywords + category_keywords))
        
        return SEOData(
            title=f"{post_title} - Mente Magna",
            description=description,
            keywords=all_keywords,
            schema_type="Article"
        )
    
    def get_tool_seo(self, tool_name: str, tool_description: str, tool_type: str) -> SEOData:
        """Gera SEO para ferramentas/calculadoras"""
        tool_keywords = {
            "calculadora": ["calculadora online", "calcular", "matemática", "fórmulas"],
            "cid": ["cid", "classificação internacional doenças", "código cid", "diagnóstico"],
            "cbo": ["cbo", "classificação brasileira ocupações", "profissões", "código cbo"],
            "conversor": ["conversor", "conversão", "unidades", "medidas"],
            "gerador": ["gerador", "criar", "gerar", "automático"],
            "validador": ["validador", "validar", "verificar", "cpf", "cnpj"]
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
    if page_type == "category":
        seo_data = seo_manager.get_category_seo(
            kwargs.get('category_slug', ''),
            kwargs.get('category_name', '')
        )
    elif page_type == "post":
        seo_data = seo_manager.get_post_seo(
            kwargs.get('post_title', ''),
            kwargs.get('post_content', ''),
            kwargs.get('post_excerpt', ''),
            kwargs.get('category', '')
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