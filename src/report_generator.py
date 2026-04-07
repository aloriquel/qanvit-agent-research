import requests
import json
from config import GEMINI_API_KEY, REPORT_LANGUAGE

class ReportGenerator:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        # Use v1beta and gemini-2.5-flash (confirmed available via browser)
        self.model_name = "models/gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_name}:generateContent?key={self.api_key}"
        print(f"Using Gemini URL: {self.url.split('?')[0]}?key=HIDDEN")

    def generate_report(self, search_results):
        """Synthesize search results into a 1-page structured report using REST API."""
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            return self._generate_fallback_report(search_results)

        prompt = f"""
        Actúa como un analista de mercado experto para la startup 'Duale' (www.duale.es).
        Duale es un copilot de IA para FP Dual que ayuda a la inclusión de alumnos con NEE (Necesidades Educativas Especiales).
        
        A partir de los siguientes resultados de búsqueda REALES de esta semana (que incluyen el contenido extraído de las webs), redacta un informe de 1 página bien organizado en HTML.
        
        Resultados de búsqueda (Contenido extraído):
        {search_results}
        
        El informe debe ser EXTREMADAMENTE ESPECÍFICO. No acepto generalidades.
        Si mencionas un competidor, di qué está haciendo. Si mencionas una ayuda, di el nombre, plazo y cuantía si aparece.
        Si mencionas una noticia, di la fecha y el medio.
        
        Estructura:
        1. COMPETIDORES (Nuevos o movimientos detectados).
        2. TENDENCIAS Y NOTICIAS RECIENTES (FP, IA en inclusión).
        3. AYUDAS Y FINANCIACIÓN (Convocatorias abiertas, BOE, diarios oficiales, NextGen).
        4. PROYECTOS PÚBLICOS Y LICITACIONES (Ministerio, Consejerías).
        Actúa como un Analista de Innovación Senior de 'Qanvit' (www.qanvit.com), una plataforma de Corporate Venture que utiliza agentes IA para conectar grandes corporaciones con startups para resolver retos de innovación corporativa.
        
        A partir de los siguientes resultados de búsqueda web de esta semana sobre corporate venture y startups:
        {search_results}
        
        Redacta un informe ejecutivo (Executive Summary) de 1 página en HTML. 
        Este informe será leído por directivos de Qanvit. El tono debe ser profesional, analítico y directo, destacando "señales de mercado".
        
        REQUISITOS DEL INFORME:
        - NO inventes datos. Usa SOLO la información proporcionada. Si no hay datos, indícalo.
        - Cuerpo en HTML (sólo el contenido, sin <html> ni <body>).
        - Estructura sugerida:
          1. <h2>Movimientos Estratégicos y CVC</h2> (tendencias de corporate venture, nuevos fondos).
          2. <h2>Startups y Ecosistemas de Innovación</h2> (nuevas startups B2B, programas de aceleración, hubs).
          3. <h2>Oportunidades Qanvit</h2> (cómo Qanvit puede aprovechar esta información).
        - Usa listas (<ul><li>) para resumir puntos clave y pon en negrita los nombres de corporaciones y startups clave.
        - INCLUYE SIEMPRE UN ENLACE a la noticia original. Para los enlaces crudos de la información usa: <a href="ENLACE" target="_blank">[Fuente]</a>.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        try:
            print("Generating report via Gemini REST API...")
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Extract text from response
            if "candidates" in data and len(data["candidates"]) > 0:
                html_report = data["candidates"][0]["content"]["parts"][0]["text"]
                return html_report.replace("```html", "").replace("```", "").strip()
            else:
                print("No candidates found in Gemini response.")
                return self._generate_fallback_report(search_results)
                
        except Exception as e:
            print(f"Error generating report with Gemini REST API: {e}")
            return self._generate_fallback_report(search_results)

    def generate_linkedin_post(self, search_results):
        """Generate a LinkedIn newsletter post from the search results."""
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            return "No se pudo generar el post de LinkedIn porque la API de Gemini no está configurada."

        prompt = f"""
        Actúa como el Community Manager de 'Qanvit' (www.qanvit.com).
        
        A partir de los siguientes resultados de búsqueda de esta semana, redacta un POST DE LINKEDIN brillante, estilo "Newsletter Semanal de Innovación" que resuma la actualidad del corporate venture y open innovation para un público muy profesional (directores de innovación, fundadores de startups, inversores).
        
        Resultados de búsqueda:
        {search_results}
        
        Instrucciones para el POST:
        - Tono: Ejecutivo, prospectivo y orientado al negocio (🚀) y la colaboración (🤝).
        - Estructura: 
          1. Gancho inicial potente sobre el estado de la innovación corporativa.
          2. Tres viñetas (bullets) con los movimientos clave (fondos, startups, retos).
          3. Reflexión final: el rol de Qanvit como agente vinculante entre corporaciones y startups.
          4. Llamada a la acción animando al debate o visitar qanvit.com.
        - Longitud óptima para lectura móvil.
        - Hashtags: #CorporateVenture #OpenInnovation #Startups #Qanvit #BusinessEcosystem
        - Idioma: Español.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        try:
            print("Generating LinkedIn post via Gemini REST API...")
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "candidates" in data and len(data["candidates"]) > 0:
                post_text = data["candidates"][0]["content"]["parts"][0]["text"]
                return post_text.strip()
            else:
                return "Error: No se encontró contenido en la respuesta de Gemini."
        except Exception as e:
            print(f"Error generating LinkedIn post: {e}")
            return f"Error: {e}"

    def _generate_fallback_report(self, search_results):
        """Simple fallback if Gemini is not available."""
        html = "<h1>Informe Semanal de Mercado - Duale</h1>"
        html += "<p>Nota: Este es un informe simplificado (Error en Gemini API o clave no configurada).</p>"
        for query, urls in search_results.items():
            html += f"<h3>{query}</h3><ul>"
            for url in urls:
                html += f"<li><a href='{url}'>{url}</a></li>"
            html += "</ul>"
        return html
