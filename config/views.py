from django.shortcuts import render, redirect
from django.views import View

from blogs.models import Category


class TopPage(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はトップ画面へリダイレクト
        allcats = Category.objects.filter(parent=None)
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)
        return render(request, 'toppage.html', {'allcats': allcats})