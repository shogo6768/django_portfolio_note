from itertools import chain

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from blogs.models import PostModel, Category 
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

from .models import CustomUser, Like, History
from .forms import LoginForm, CreateForm
from django import template
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging

# logger定義
logger = logging.getLogger(__name__)

   
def save_history(request, pk):
    if request.user.is_authenticated:
        user = request.user
        look_post = PostModel.objects.get(pk=pk)
        history = History.objects.filter(Q(user=user) & Q(post=look_post))
        
        if history:
            history.delete()
            history = History.objects.create(user=user, post=look_post)
        else:
            history = History.objects.create(user=user, post=look_post)

    return redirect('post_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def like(request, pk):
    post = PostModel.objects.get(pk=pk)
    user = request.user
    like_object = Like.objects.filter(Q(user=user) & Q(post=post))
    if like_object:
        like_object.delete()
    else:
        like_object = Like.objects.create(user=user, post=post)
    return redirect('post_detail', pk=pk)



class CreateUser(View):
    def get(self, request, *args, **kwargs):
        allcats = Category.objects.filter(parent=None)
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)
        context = {'form': CreateForm(), 'allcats': allcats}
        return render(request, 'accounts/create.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")
        # リクエストからフォームを作成
        form = CreateForm(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'accounts/create.html', {'form': form})
        # 保存する前に一旦取り出す
        user = form.save(commit=False)
        # パスワードをハッシュ化してセット
        user.set_password(form.cleaned_data['password'])
        # ユーザーオブジェクトを保存
        user.save()
        # ログイン処理（取得した Userオブジェクトをセッションに保存 & Userデータを更新）
        auth_login(request, user)

        return redirect('mypage', pk=request.user.id)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        allcats = Category.objects.filter(parent=None)
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)

        # 1/4 斉藤allcats追加
        context = {
            'form': LoginForm(),
            'allcats': allcats
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = LoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'accounts/login.html', {'form': form})
        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()
        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)
        # フラッシュメッセージを画面に表示
        messages.info(request, "ログインしました。")

        return redirect('mypage', pk=request.user.id)


login = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(id={}) has logged out.".format(request.user.id))
            # ログアウト処理
            auth_logout(request)
        # フラッシュメッセージを画面に表示
        messages.info(request, "ログアウトしました。")

        return redirect(reverse('toppage'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context


logout = LogoutView.as_view()



@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class MypageView(View):
    model = CustomUser

    def get(self, request, pk, *args, **kwargs):
        likes = Like.objects.filter(user=request.user).order_by('-created_at')
        histories = History.objects.filter(
            user=request.user).order_by('-created_at')
        recommend_posts = []
        cats = []
        histories_for_recommend = histories.order_by('-created_at')[:3]

        allcats = Category.objects.filter(parent=None)

        for history in histories_for_recommend:
            cat = history.post.category
            cats.append(cat)
        cats_unique = list(set(cats))

        for cat in cats_unique:
            posts = PostModel.objects.filter(
                category=cat).order_by('-created_at')[:3]
            recommend_posts = chain(recommend_posts, posts)

        return render(request, 'accounts/mypage.html', {'like_posts': likes, 'history_posts': histories, 'recommend_posts': recommend_posts, 'allcats': allcats})

mypage = MypageView.as_view()


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class Resign(TemplateView):
    template_name = 'accounts/resign.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class ResConduct(View):
    def get(self, request, pk, *args, **kwargs):
        if (request.user.is_authenticated) & (request.user.pk == self.kwargs['pk']):
            user = request.user
            user.delete()
            return redirect(reverse('resign_complete'))


class ResComplete(TemplateView):
    template_name = 'accounts/resign_complete.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context

def guest_login(request):
    user = CustomUser.objects.get(username='guestuser')
    auth_login(request, user)
    return redirect('mypage', pk=request.user.id)




