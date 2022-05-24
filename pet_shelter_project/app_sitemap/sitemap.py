from django.contrib.sitemaps import Sitemap
# from app_housing.models import Housing
# from app_rss.models import News


class DjsaleSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	# def items(self):
	# 	return Housing.objects.all()
