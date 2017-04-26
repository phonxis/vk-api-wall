from django.shortcuts import render, redirect
from django.views.generic.base import View
from datetime import datetime, timedelta
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from social_django.models import UserSocialAuth
import random
import vk



class Index(CsrfExemptMixin, View):
    # главная страница с кнопкой авторизации и списком групп
    def get(self, request):
        return render(request, "groups/main.html", {})


class GetUserGroups(CsrfExemptMixin, JsonRequestResponseMixin, View):
    # получение списка групп пользователя
    def get(self, request):
        if request.user.is_authenticated():
            # получаем токен
            user_data = UserSocialAuth.objects.get(user=request.user)
            token = user_data.extra_data['access_token']
            # создаем сессию и связываем ее с vk API
            session = vk.Session(access_token=token)
            vk_api = vk.API(session, v='5.63')
            # получаем список всех групп пользователя
            groups = vk_api.groups.get(user_id=user_data.uid, extended=1)
            # возвращаем список групп
            return self.render_json_response({'data': groups['items']})
        else:
            # пользователь не авторизован
            return None


class GetGroupWall(View):
    # отображение страницы со стеной определенной группы
    def get(self, request, group_id):
        if request.user.is_authenticated():
            return render(request, "groups/group_wall.html", {'group_id': group_id})
        else:
            return redirect("index")


class LoadGroupWall(CsrfExemptMixin, JsonRequestResponseMixin, View):
    # загрузка стены группы
    def get(self, request, group_id):
        if request.user.is_authenticated():
            # получаем токен
            user_data = UserSocialAuth.objects.get(user=request.user)
            token = user_data.extra_data['access_token']
            # создаем сессию и связываем ее с vk API
            session = vk.Session(access_token=token)
            vk_api = vk.API(session, v='5.63')
            # формируем id группы (со знаком -)
            group_id = '-{}'.format(group_id)
            # получение 5ти последних постов со стены группы
            posts = vk_api.wall.get(owner_id=group_id, count=5)
            # возвращаем список групп
            return self.render_json_response(posts['items'])
        else:
            # will added django message
            return None


class GetEmbedVideo(CsrfExemptMixin, JsonRequestResponseMixin, View):
    # загрузка видеозаписей
    def get(self, request, owner_id, video_id):
        if request.user.is_authenticated():
            # получаем токен
            user_data = UserSocialAuth.objects.get(user=request.user)
            token = user_data.extra_data['access_token']
            # создаем сессию и связываем ее с vk API
            session = vk.Session(access_token=token)
            vk_api = vk.API(session, v='5.63')
            # формируем ссылку видеозаписи
            video_url = "{}_{}".format(owner_id, video_id)
            # получаем видеозаписи для текущих постов
            video = vk_api.video.get(videos=video_url)
            # возвращаем список видеозаписей
            return self.render_json_response(video['items'])
        else:
            # will added django message
            return None


class LoadPrevPosts(CsrfExemptMixin, JsonRequestResponseMixin, View):
    # загрузка следующих постов со стены группы
    def get(self, request, group_id, offset):
        if request.user.is_authenticated():
            # получаем токен
            user_data = UserSocialAuth.objects.get(user=request.user)
            token = user_data.extra_data['access_token']
            # создаем сессию и связываем ее с vk API
            session = vk.Session(access_token=token)
            vk_api = vk.API(session, v='5.63')
            # формируем id группы
            group_id = '-{}'.format(group_id)
            # получаем 5 следующих постов
            posts = vk_api.wall.get(owner_id=group_id, count=5, offset=int(offset))
            # возвращаем посты
            return self.render_json_response(posts['items'])
        else:
            # will added django message
            return None
