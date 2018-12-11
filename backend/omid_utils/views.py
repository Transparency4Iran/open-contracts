from django.http import HttpResponse
from .sitemap import UrlNode, Sitemap
from main.models import Contract
from org.models import Executor

def get_sitemap(request):
    sitemap = Sitemap(base='https://cdb.tp4.ir/')
    sitemap.add_node(UrlNode(loc='/', priority=0.9, changefreq='monthly'))
    sitemap.add_node(UrlNode(loc='/map', priority=0.88, changefreq='weekly'))
    sitemap.add_node(UrlNode(loc='/donate', priority=0.85, changefreq='yearly'))
    sitemap.add_node(UrlNode(loc='/export', priority=0.85, changefreq='yearly'))
    sitemap.add_node(UrlNode(loc='/about', priority=0.85, changefreq='yearly'))
    sitemap.add_node(UrlNode(loc='/errors', priority=0.88, changefreq='weekly'))
    sitemap.add_node(UrlNode(loc='/statistics', priority=0.88, changefreq='weekly'))
    for contract in Contract.objects.all():
        sitemap.add_node(UrlNode(loc='/contract/'+contract.code, priority=0.7, changefreq='yearly'))
    # for executor in Executor.objects.all():
    #     sitemap.add_node(UrlNode(loc='/executor/'+str(executor.id), priority=0.6, changefreq='yearly'))

    return HttpResponse(sitemap.create_xml(), content_type='text/xml')
