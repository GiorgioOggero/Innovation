"""Generate crawlable language pages from the original multilingual templates.
Requires Python 3 and lxml. Run from repository root: python tools/seo/build.py
"""
from pathlib import Path
from lxml import html, etree
import json, re

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://giorgiooggero.github.io/Innovation/'
LANGS = ['en', 'it', 'ar', 'de', 'es', 'zh']
PAGES = ['index', 'experiences', 'contents', 'book', 'contacts', 'privacy']
LABELS = {
'en': ['International Negotiation & GCC Market Entry', 'Experiences', 'Contents', 'The Charm of Doubt', 'Contacts', 'Privacy'],
'it': ['Negoziazione internazionale e mercati GCC', 'Esperienze', 'Contenuti', 'Il fascino del dubbio', 'Contatti', 'Privacy'],
'ar': ['التفاوض الدولي ودخول أسواق الخليج', 'الخبرات', 'المحتوى', 'سحر الشك', 'التواصل', 'الخصوصية'],
'de': ['Internationale Verhandlung und GCC-Markteintritt', 'Erfahrung', 'Inhalte', 'Die Faszination des Zweifels', 'Kontakt', 'Datenschutz'],
'es': ['Negociación internacional y mercados GCC', 'Experiencias', 'Contenidos', 'El encanto de la duda', 'Contacto', 'Privacidad'],
'zh': ['国际谈判与海湾市场进入', '经验', '内容', '怀疑的魅力', '联系方式', '隐私']}
DESCRIPTIONS = {
'en': ['Corporate training and advisory by Giorgio Oggero in international negotiation, export and GCC/UAE market entry.', 'Discover Giorgio Oggero’s experience in export, international sales, market development and negotiation.', 'Explore Giorgio Oggero’s articles and visual content on negotiation, export, cross-cultural communication and GCC markets.', 'Discover The Charm of Doubt by Gabriella Nembo and Giorgio Oggero, a book about communication, perspective and growth, available in English.', 'Contact Giorgio Oggero about corporate training, international negotiation, export and GCC/UAE market entry.', 'Privacy information for Giorgio Oggero’s professional website and contact by email.'],
'it': ['Formazione e consulenza di Giorgio Oggero su negoziazione internazionale, export e ingresso nei mercati GCC e UAE.', 'Scopri l’esperienza di Giorgio Oggero in export, vendite internazionali, sviluppo dei mercati e negoziazione.', 'Articoli e contenuti visivi di Giorgio Oggero su negoziazione, export, comunicazione interculturale e mercati GCC.', 'Scopri Il fascino del dubbio di Gabriella Nembo e Giorgio Oggero: comunicazione, prospettive e crescita. Disponibile anche in inglese.', 'Contatta Giorgio Oggero per formazione aziendale, negoziazione internazionale, export e ingresso nei mercati GCC e UAE.', 'Informazioni sulla privacy del sito professionale di Giorgio Oggero e sui contatti tramite email.'],
'ar': ['تدريب واستشارات مع جورجيو أوجيرو في التفاوض الدولي والتصدير ودخول أسواق الخليج والإمارات.', 'اكتشف خبرة جورجيو أوجيرو في التصدير والمبيعات الدولية وتطوير الأسواق والتفاوض.', 'مقالات ومحتوى مرئي لجورجيو أوجيرو حول التفاوض والتصدير والتواصل بين الثقافات وأسواق الخليج.', 'اكتشف كتاب سحر الشك لغابرييلا نيمبو وجورجيو أوجيرو حول التواصل ووجهات النظر والنمو، والمتاح باللغة الإنجليزية.', 'تواصل مع جورجيو أوجيرو بشأن التدريب المؤسسي والتفاوض الدولي والتصدير ودخول أسواق الخليج والإمارات.', ''],
'de': ['Corporate Training und Beratung mit Giorgio Oggero zu internationaler Verhandlung, Export und Markteintritt in GCC und VAE.', 'Entdecken Sie Giorgio Oggeros Erfahrung in Export, internationalem Vertrieb, Marktentwicklung und Verhandlung.', 'Artikel und visuelle Inhalte von Giorgio Oggero über Verhandlung, Export, interkulturelle Kommunikation und GCC-Märkte.', 'Entdecken Sie The Charm of Doubt von Gabriella Nembo und Giorgio Oggero über Kommunikation, Perspektiven und Wachstum. Auf Englisch erhältlich.', 'Kontaktieren Sie Giorgio Oggero zu Corporate Training, internationaler Verhandlung, Export und GCC/VAE-Markteintritt.', ''],
'es': ['Formación y consultoría de Giorgio Oggero en negociación internacional, exportación y entrada en los mercados GCC y EAU.', 'Descubre la experiencia de Giorgio Oggero en exportación, ventas internacionales, desarrollo de mercados y negociación.', 'Artículos y contenido visual de Giorgio Oggero sobre negociación, exportación, comunicación intercultural y mercados GCC.', 'Descubre The Charm of Doubt de Gabriella Nembo y Giorgio Oggero sobre comunicación, perspectivas y crecimiento. Disponible en inglés.', 'Contacta con Giorgio Oggero para formación empresarial, negociación internacional, exportación y entrada en los mercados GCC y EAU.', ''],
'zh': ['Giorgio Oggero 提供国际谈判、出口及海湾国家和阿联酋市场进入方面的企业培训与咨询。', '了解 Giorgio Oggero 在出口、国际销售、市场开发和谈判方面的实战经验。', '探索 Giorgio Oggero 关于谈判、出口、跨文化沟通与海湾市场的文章和视觉内容。', '了解 Gabriella Nembo 与 Giorgio Oggero 合著的 The Charm of Doubt，探讨沟通、视角与成长，现有英文版。', '联系 Giorgio Oggero，咨询企业培训、国际谈判、出口及海湾国家和阿联酋市场进入。', '']}

def languages(page): return LANGS if page != 'privacy' else ['en', 'it']
def path(page, lang): return ('' if lang == 'en' else lang + '/') + ('' if page == 'index' else page + '.html')
def url(page, lang): return BASE + path(page, lang)
def classes(el): return set(el.get('class','').split())

def build(page, lang):
    tree = html.fromstring((ROOT/'tools/seo/templates'/f'{page}.html.in').read_text())
    tree.set('lang',lang); tree.set('dir','rtl' if lang=='ar' else 'ltr')
    body=tree.find('body'); body.set('class','lang-'+lang+(' rtl' if lang=='ar' else ''))
    for el in list(tree.iter()):
        if el.getparent() is not None and classes(el).intersection(LANGS) and lang not in classes(el): el.drop_tree()
    for el in tree.xpath('//script[@id="language-selector-fallback"]'): el.drop_tree()
    head=tree.find('head')
    for el in head.xpath('./title|./meta[@name="description"]|./link[@rel="canonical"]|./link[@rel="alternate"]|./meta[@property="og:title" or @property="og:description" or @property="og:url"]'): head.remove(el)
    i=PAGES.index(page); title=LABELS[lang][i]+' | Giorgio Oggero'
    etree.SubElement(head,'title').text=title
    etree.SubElement(head,'meta',name='description',content=DESCRIPTIONS[lang][i])
    etree.SubElement(head,'link',rel='canonical',href=url(page,lang))
    for code in languages(page): etree.SubElement(head,'link',rel='alternate',hreflang=code,href=url(page,code))
    etree.SubElement(head,'link',rel='alternate',hreflang='x-default',href=url(page,'en'))
    for prop,val in [('og:title',title),('og:description',DESCRIPTIONS[lang][i]),('og:url',url(page,lang))]: etree.SubElement(head,'meta',property=prop,content=val)
    # Absolute site paths keep shared images, styles, PDFs and scripts valid at every depth.
    for el in tree.iter():
        for attr in ['href','src']:
            value=el.get(attr)
            if not value or re.match(r'^(?:[a-z]+:|//|/|#)',value,re.I): continue
            raw=value.split('?')[0].split('#')[0]
            if raw in [p+'.html' for p in PAGES]:
                target=raw[:-5]; code=lang if lang in languages(target) else 'en'
                suffix=value[len(raw):]; el.set(attr,'/Innovation/'+path(target,code)+suffix)
            else: el.set(attr,'/Innovation/'+value)
    # Links work without JS; keep exact button appearance using the existing CSS.
    for button in tree.xpath('//*[@data-lang]'):
        code=button.get('data-lang'); target_lang=code if code in languages(page) else 'en'
        button.tag='a';button.set('href','/Innovation/'+path(page,target_lang));button.set('hreflang',target_lang)
        if code==lang: button.set('aria-current','page')
        button.set('aria-label',{'en':'English','it':'Italiano','ar':'العربية','de':'Deutsch','es':'Español','zh':'中文'}[code])
    if page=='privacy' and lang=='it':
        tree.xpath('//main//h1')[0].text='Informativa sulla privacy'
    for script in head.xpath('./script[@type="application/ld+json"]'):
        data=json.loads(script.text);data['url']=url(page,lang)
        # This describes the English book edition, even on translated landing pages.
        script.text=json.dumps(data,ensure_ascii=False)
    destination=ROOT/(('' if lang=='en' else lang+'/')+page+'.html')
    destination.parent.mkdir(exist_ok=True)
    destination.write_text('<!doctype html>\n'+html.tostring(tree,encoding='unicode',method='html'))
    return url(page,lang)

urls=[build(page,lang) for page in PAGES for lang in languages(page)]
ns='http://www.sitemaps.org/schemas/sitemap/0.9'
sitemap=etree.Element('{'+ns+'}urlset',nsmap={None:ns})
for value in urls:
    entry=etree.SubElement(sitemap,'{'+ns+'}url');etree.SubElement(entry,'{'+ns+'}loc').text=value
# Never manufacture modification dates; add them only when known for the content.
(ROOT/'sitemap.xml').write_bytes(etree.tostring(sitemap,xml_declaration=True,encoding='UTF-8',pretty_print=True))
# Keep the historical misspelled submitted URL usable, rather than returning 404.
(ROOT/'sitemaps.xml').write_bytes((ROOT/'sitemap.xml').read_bytes())
print(f'Generated {len(urls)} canonical pages and two equivalent sitemap endpoints.')
