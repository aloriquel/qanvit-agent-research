import anthropic
from config import ANTHROPIC_API_KEY, REPORT_LANGUAGE

MODEL = "claude-haiku-4-5-20251001"

# === COMPANY CONTEXT ===
# Qanvit (www.qanvit.com) is an AI agents platform for Corporate Venture and Open Innovation.
# Core product: Connects corporates, technology parks and clusters with the right startups
# for their innovation challenges using autonomous AI agents.
# Target customers:
#   - Large corporations with innovation/CVC departments
#   - Technology parks (parques tecnológicos) and science clusters
#   - Innovation hubs looking to run open challenges
# Key differentiators:
#   - AI-automated matching between corporates and startups
#   - Not just a directory — agents actively qualify and recommend startups
#   - Serves as deal-flow infrastructure for CVC and open innovation programs
# Competitors: Dealroom, F6S, Open Innovation platforms, Wayra (Telefónica), CVC arms of large corps
# Key market signals to monitor:
#   - CVC fund announcements and new investment programs in Spain/Europe
#   - New open innovation challenges launched by corporations
#   - Startup funding rounds (Series A+ in Spain/Europe, esp. B2B/DeepTech)
#   - New tech parks or clusters launching innovation programs
#   - AI for corporate-startup matching / deal-flow automation tools (competitors)
#   - Policy: PERTE, CDTI programas, Ley de Startups updates

COMPANY_CONTEXT = """
CONTEXTO DE EMPRESA:
Qanvit (www.qanvit.com) es una plataforma de agentes de IA para Corporate Venture e Innovación Abierta.
- PRODUCTO: Agentes de IA que conectan automáticamente corporados, parques tecnológicos y clústeres con las startups más adecuadas para sus retos de innovación. Va más allá de un directorio: los agentes cualifican y recomiendan activamente.
- CLIENTES: (1) Grandes corporaciones con departamentos de CVC o innovación, (2) Parques tecnológicos y clústeres que organizan programas de open innovation, (3) Hubs de innovación que buscan deal-flow de startups.
- DIFERENCIADORES: Matching IA automatizado (no solo búsqueda manual). Infraestructura de deal-flow para CVC y open innovation.
- COMPETIDORES: Dealroom, F6S, plataformas de open innovation, Wayra (Telefónica), brazos CVC de grandes corporaciones, Corporate Innovation firms.
- ETAPA: Startup en fase de tracción, buscando primeros clientes corporativos y alianzas con parques tecnológicos.
"""


def _compact_results(search_results, max_items_per_query=3, max_title_chars=120):
    """Serialize search results compactly to keep prompt size manageable."""
    lines = []
    for query, items in search_results.items():
        lines.append(f"[{query}]")
        for item in items[:max_items_per_query]:
            content = item.get("content", "")
            parts = content.split("\n")
            title = parts[0][:max_title_chars] if parts else ""
            url = item.get("url", "")[:200]
            lines.append(f"  - {title} | {url}")
    return "\n".join(lines)


def _call_claude(prompt):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        print("Calling Claude API...")
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        text = message.content[0].text
        return text.replace("```html", "").replace("```", "").strip()
    except Exception as e:
        print(f"Claude API error: {e}")
        return None


class ReportGenerator:
    def generate_report(self, search_results):
        prompt = f"""Eres el analista de inteligencia de mercado interno de Qanvit. Tienes acceso al siguiente contexto de empresa:

{COMPANY_CONTEXT}

A partir de los siguientes resultados de búsqueda de esta semana:
{_compact_results(search_results)}

Redacta un informe de inteligencia semanal en HTML puro (sin <html> ni <body>).
El informe debe ser ESPECÍFICO y ACCIONABLE. Nombra fondos, startups, corporaciones y events concretos con fechas e importes reales.

ESTRUCTURA OBLIGATORIA:

<h2>🏦 Movimientos CVC y Fondos de Inversión</h2>
Nuevos fondos de Corporate Venture Capital anunciados, rondas de inversión en España/Europa, programas de inversión corporativa.
Menciona: nombre del fondo/programa, corporación patrocinadora, tamaño del fondo, foco sectorial.

<h2>🚀 Startups y Ecosistema de Innovación</h2>
Startups B2B destacadas que han levantado capital o lanzado productos esta semana en España/Europa.
Nuevos programas de aceleración o open challenges lanzados por corporaciones o parques tecnológicos.
Menciona: nombre de la startup, sector, ronda y cuantía. ¿Podrían ser candidatas para retos de empresas clientes de Qanvit?

<h2>🏢 Corporaciones Buscando Innovación</h2>
Grandes empresas que han anunciado programas de innovación abierta, búsqueda de startups, o retos corporativos.
Estas son OPORTUNIDADES DE VENTA DIRECTA para Qanvit.

<h2>⚙️ Tecnología y Competidores</h2>
Nuevas herramientas o plataformas de deal-flow, CVC management, o corporate-startup matching.
¿Algún competidor (Dealroom, F6S, etc.) ha lanzado algo nuevo? ¿Qué implica para Qanvit?

<h2>🎯 Oportunidades Clave para Qanvit esta semana</h2>
3-5 acciones concretas: contactar con X corporación, presentarse a Y programa, vigilar Z convocatoria.

REGLAS DE FORMATO:
- Usa <ul><li> para bullets. Pon en <strong> nombres de corporaciones, fondos y startups.
- Incluye el enlace fuente: <a href="URL" target="_blank">[Fuente]</a>
- Si no hay datos para una sección: <p><em>Sin noticias relevantes esta semana.</em></p>
- Idioma: Español."""

        result = _call_claude(prompt)
        if result:
            return result
        return self._fallback(search_results)

    def generate_linkedin_post(self, search_results):
        prompt = f"""Eres el Community Manager de Qanvit (www.qanvit.com), plataforma de agentes IA para Corporate Venture.

{COMPANY_CONTEXT}

Basándote en estos resultados de búsqueda de esta semana:
{_compact_results(search_results)}

Redacta un post de LinkedIn semanal de máximo 300 palabras. Público: directores de innovación, responsables de CVC, fundadores de startups B2B, gestores de parques tecnológicos.

Estructura:
1. Dato o tendencia de la semana que llame la atención (cifra concreta, movimiento de mercado).
2. 3 señales relevantes del ecosistema CVC/startups (con nombres y datos reales).
3. Reflexión sobre el rol de Qanvit como infraestructura de deal-flow para la innovación corporativa.
4. CTA: debate o visitar qanvit.com.

Tono: Ejecutivo, analítico, con autoridad de mercado. Sin ser vendedor. Saltos de línea frecuentes.
Hashtags: #CorporateVenture #OpenInnovation #Startups #Qanvit #InnovaciónCorporativa
Idioma: Español."""

        result = _call_claude(prompt)
        return result or "Post no disponible esta semana."

    def _fallback(self, search_results):
        html = "<h1>Informe Qanvit — Datos Recopilados</h1>"
        html += "<p><em>El motor de IA no pudo conectar esta semana. Aquí están los datos en bruto:</em></p>"
        for query, items in search_results.items():
            html += f"<h3>🔍 {query}</h3><ul>"
            for item in items:
                if isinstance(item, dict):
                    url = item.get('url', '#')
                    content = item.get('content', '')[:300]
                    html += f"<li><a href='{url}' target='_blank'>[Fuente]</a> — {content}</li>"
            html += "</ul>"
        return html
