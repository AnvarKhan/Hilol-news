from django.views.generic import ListView, DetailView, TemplateView
from .models import News, Category
from django.shortcuts import render, get_object_or_404


class BlogListView(ListView):
	"""Blog List"""
	model = News
	template_name = 'home.html'


def category(request, category_id):
	string = Category.objects.get(pk=category_id)
	string1 = News.objects.all().filter(category_id=category_id)
	if len(string1) > 0:
		b = string1[0]
	else:
		b = {}
	states = {
		'asd': string1,
		'st': string,
		'b': b
	}
	return render(request, "art.html", states)


def post_detail(request, news_id):
	stri = get_object_or_404(News, pk=news_id)
	string1 = News.objects.all().filter(category_id=news_id)
	ctx = {
		"new": stri,
		"asd": string1,
	}
	return render(request, "post_detail.html", ctx)
