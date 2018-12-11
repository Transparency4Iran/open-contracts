"""contracts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from fetch import views as fetch_views
from main import views as main_views
from org import views as org_views
from location import views as location_views
from aggregation import views as aggregation_views
from django.views.decorators.cache import cache_page
from omid_utils import views as utils_views

schema_view = get_schema_view(title='Contracts Api')
router = DefaultRouter()
router.register(r'contracts', main_views.ContractList)
router.register(r'organizations', org_views.OrganizationView)
router.register(r'executors', org_views.ExecutorView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', schema_view),
    url(r'^top_organizations/statistics', org_views.TopOrganizationsStatistics.as_view()),
    url(r'^top_organizations/',cache_page(23 * 60 * 60)( org_views.TopOrganizationsWithLeaves.as_view())),
    url(r'^people/statistics', org_views.PeopleListWithStatistics.as_view()),
    url(r'^people', cache_page(23 * 60 * 60)(org_views.PeopleList.as_view())),
    url(r'^provinces/', cache_page(23 * 60 * 60)(location_views.ProvinceList.as_view())),
    url(r'^general_rules/', cache_page(23 * 60 * 60)(main_views.GeneralRuleList.as_view())),
    url(r'^categories/', cache_page(23 * 60 * 60)(main_views.CategoryList.as_view())),
    url(r'^credit_sources/', cache_page(23 * 60 * 60)(main_views.CreditSourceList.as_view())),
    url(r'^aggregate/top_organization/year',cache_page(23 * 60 * 60)( aggregation_views.OrganizationYear.as_view())),
    url(r'^aggregate/top_organization/month', cache_page(23 * 60 * 60)(aggregation_views.OrganizationMonth.as_view())),
    url(r'^aggregate/province', cache_page(23 * 60 * 60)(aggregation_views.OnProvince.as_view())),
    url(r'^aggregate/town', cache_page(23 * 60 * 60)(aggregation_views.OnTown.as_view())),
    url(r'^aggregate/city', aggregation_views.OnCity.as_view()),
    url(r'^aggregate/percentile/executors', aggregation_views.ExecutorPercentile.as_view()),
    url(r'^aggregate/percentile', aggregation_views.Percentile.as_view()),
    url(r'^aggregate/stat', cache_page(23 * 60 * 60)(aggregation_views.StatView.as_view())),
    url(r'^aggregate/error_spectrum', aggregation_views.ErrorSpectrumView.as_view()),
    url(r'^aggregate/daily_fetch_per_top_organization', cache_page(23 * 60 * 60)(aggregation_views.DailyFetchPerTopOrganizationView.as_view())),
    url(r'^', include(router.urls)),
    url(r'^attempts', cache_page(23 * 60 * 60)(fetch_views.AttemptList.as_view())),
    url(r'^raw/detail/(?P<id>\d+)$', fetch_views.raw_detail),
    url(r'^raw/(?P<id>\d+)$', fetch_views.raw),
    url(r'^force_check$', fetch_views.force_check),
    url(r'^fetch_details', fetch_views.force_fetch_detail_pages),
    url(r'^force_read', main_views.force_read),
    url(r'^sitemap.xml', utils_views.get_sitemap),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
