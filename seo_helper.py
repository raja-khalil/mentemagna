# seo_helper.py - Ferramentas para SEO e Google Search Console
import requests
from datetime import datetime
import os

class SEOHelper:
    """Classe helper para otimizações de SEO"""
    
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
    
    def ping_google_sitemap(self):
        """Avisa o Google sobre atualizações no sitemap"""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        ping_url = f"http://www.google.com/ping?sitemap={sitemap_url}"
        
        try:
            response = requests.get(ping_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Google notificado sobre sitemap: {sitemap_url}")
                return True
            else:
                print(f"⚠️ Erro ao notificar Google: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao conectar com Google: {e}")
            return False
    
    def ping_bing_sitemap(self):
        """Avisa o Bing sobre atualizações no sitemap"""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        ping_url = f"http://www.bing.com/ping?sitemap={sitemap_url}"
        
        try:
            response = requests.get(ping_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Bing notificado sobre sitemap: {sitemap_url}")
                return True
            else:
                print(f"⚠️ Erro ao notificar Bing: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao conectar com Bing: {e}")
            return False
    
    def validate_sitemap(self):
        """Valida se o sitemap está acessível e bem formado"""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        
        try:
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                # Verificar se é XML válido
                if '<?xml' in response.text and '<urlset' in response.text:
                    print(f"✅ Sitemap válido: {sitemap_url}")
                    return True
                else:
                    print(f"❌ Sitemap com formato inválido")
                    return False
            else:
                print(f"❌ Sitemap inacessível: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao validar sitemap: {e}")
            return False
    
    def validate_robots(self):
        """Valida se o robots.txt está acessível"""
        robots_url = f"{self.base_url}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                if 'User-agent:' in response.text and 'Sitemap:' in response.text:
                    print(f"✅ Robots.txt válido: {robots_url}")
                    return True
                else:
                    print(f"⚠️ Robots.txt com formato básico")
                    return True
            else:
                print(f"❌ Robots.txt inacessível: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao validar robots.txt: {e}")
            return False
    
    def generate_google_verification_file(self, verification_code):
        """Gera arquivo de verificação do Google Search Console"""
        filename = f"google{verification_code}.html"
        content = f"google-site-verification: google{verification_code}.html"
        
        try:
            # Salvar na pasta static para ser acessível
            filepath = os.path.join('static', filename)
            with open(filepath, 'w') as f:
                f.write(content)
            
            print(f"✅ Arquivo de verificação criado: {filename}")
            print(f"📱 Acesse: {self.base_url}/{filename}")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar arquivo de verificação: {e}")
            return False
    
    def check_seo_basics(self):
        """Verifica itens básicos de SEO"""
        print("\n🔍 VERIFICAÇÃO SEO BÁSICA")
        print("=" * 50)
        
        checks = [
            ("Sitemap XML", self.validate_sitemap()),
            ("Robots.txt", self.validate_robots()),
        ]
        
        # Verificar páginas importantes
        important_pages = [
            '/',
            '/blog',
            '/sobre',
            '/contato',
            '/termos',
            '/privacidade'
        ]
        
        for page in important_pages:
            url = f"{self.base_url}{page}"
            try:
                response = requests.get(url, timeout=10)
                status = response.status_code == 200
                checks.append((f"Página {page}", status))
            except:
                checks.append((f"Página {page}", False))
        
        # Mostrar resultados
        for check_name, status in checks:
            icon = "✅" if status else "❌"
            print(f"{icon} {check_name}")
        
        # Resumo
        passed = sum(1 for _, status in checks if status)
        total = len(checks)
        print(f"\n📊 Resultado: {passed}/{total} verificações passaram")
        
        if passed == total:
            print("🎉 Seu site está otimizado para SEO!")
        elif passed >= total * 0.8:
            print("👍 Bom! Alguns ajustes menores podem melhorar.")
        else:
            print("⚠️ Várias melhorias de SEO são necessárias.")
        
        return passed / total

# Função utilitária para usar no Flask
def notify_search_engines(base_url):
    """Notifica motores de busca sobre atualizações"""
    seo = SEOHelper(base_url)
    
    print("\n📡 NOTIFICANDO MOTORES DE BUSCA")
    print("=" * 50)
    
    seo.ping_google_sitemap()
    seo.ping_bing_sitemap()
    
    print("✅ Notificações enviadas!")

# Script para executar verificações
if __name__ == "__main__":
    # Para testes locais
    seo = SEOHelper("http://localhost:5000")
    seo.check_seo_basics()
    
    # Para notificar quando estiver online
    # notify_search_engines("https://seudominio.com")