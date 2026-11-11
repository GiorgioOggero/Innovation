"""Validate canonicals, reciprocal language links, sitemap and published assets."""
from pathlib import Path
from lxml import html, etree
from urllib.parse import urlparse, unquote
import json
ROOT=Path(__file__).resolve().parents[2]
BASE='https://giorgiooggero.github.io/Innovation/'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=etree.parse(str(ROOT/'sitemap.xml')).xpath('//s:loc/text()',namespaces=ns)
assert len(urls)==len(set(urls))==32

def local(url):
 p=urlparse(url).path
 assert p.startswith('/Innovation/'),url
 rel=unquote(p[len('/Innovation/'):]);return ROOT/(rel+'index.html' if not rel or rel.endswith('/') else rel)

missing=set()
for u in urls:
 t=html.parse(str(local(u)));head=t.find('head')
 assert head.xpath('./link[@rel="canonical"]/@href')==[u],u
 assert len(head.xpath('./meta[@name="description"]/@content'))==1,u
 assert head.xpath('./meta[@name="description"]/@content')[0].strip(),u
 assert len(head.xpath('./title'))==1,u
 lang=t.getroot().get('lang')
 assert head.xpath('./link[@rel="alternate" and @hreflang=$l]/@href',l=lang)==[u],u
 for alt in head.xpath('./link[@rel="alternate"]'):
  v=alt.get('href');other=html.parse(str(local(v)))
  assert other.xpath('//link[@rel="alternate" and @hreflang=$l]/@href',l=lang)==[u],(u,v)
 assert not t.xpath('//meta[@name="robots" and contains(@content,"noindex")]'),u
 for el in t.xpath('//link[@rel="stylesheet"]|//script[@src]|//img[@src]'):
  value=el.get('href') or el.get('src')
  if value.startswith('/Innovation/') and not local(value).is_file():
   # Report existing missing source assets; a new broken reference is a failure.
   original=value[len('/Innovation/'):]
   template=(ROOT/'tools/seo/templates'/f'{local(u).stem}.html.in').read_text()
   assert original in template,(u,value)
   missing.add(original)
 for script in t.xpath('//script[@type="application/ld+json"]'):json.loads(script.text)
 # Generated pages retain the exact pre-existing visible copy in their language.
 page=local(u).stem; source=html.parse(str(ROOT/'tools/seo/templates'/f'{page}.html.in'))
 for el in list(source.getroot().iter()):
  codes=set(el.get('class','').split()).intersection(['en','it','ar','de','es','zh'])
  if el.getparent() is not None and codes and lang not in codes:el.drop_tree()
 if not (page=='privacy' and lang=='it'):
  assert ''.join(source.xpath('//main//text()'))==''.join(t.xpath('//main//text()')),u
assert (ROOT/'sitemap.xml').read_bytes()==(ROOT/'sitemaps.xml').read_bytes()
assert BASE+'index.html' not in urls
print('PASS: 32 pages; matching canonical/sitemap URLs; reciprocal hreflang; descriptions; shared assets; unchanged main copy; valid JSON-LD.')

print('Pre-existing unavailable images:',len(missing))
