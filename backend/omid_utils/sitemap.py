from xml.dom import minidom
from urllib.parse import urljoin


class UrlNode:

    def __init__(self, loc=None, priority=None, changefreq=None):
        self.loc = loc
        self.priority = priority
        self.changefreq = changefreq


class Sitemap:
    def __init__(self, base):
        self.base = base
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def create_xml(self):
        doc = minidom.Document()
        urlset = doc.createElement('urlset')
        urlset.setAttribute('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9")
        doc.appendChild(urlset)
        for node in self.nodes:
            if node.loc:
                url = doc.createElement('url')
                loc = doc.createElement('loc')
                loc_text = doc.createTextNode(urljoin(self.base, node.loc))
                loc.appendChild(loc_text)
                url.appendChild(loc)
                if node.priority:
                    priority = doc.createElement('priority')
                    priority_text = doc.createTextNode(str(node.priority)[:4])
                    priority.appendChild(priority_text)
                    url.appendChild(priority)
                if node.changefreq:
                    changefreq = doc.createElement('changefreq')
                    changefreq_text = doc.createTextNode(node.changefreq)
                    changefreq.appendChild(changefreq_text)
                    url.appendChild(changefreq)
                urlset.appendChild(url)
        return doc.toprettyxml(indent="  ", encoding='utf-8')


def notify_sitemap_to_google():
    import requests
    requests.get('http://google.com/ping?sitemap=https://cdn.tp4.ir/api/sitemap.xml')
    print('notified to google')
