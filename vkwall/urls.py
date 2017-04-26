"""vkwall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.auth import views as auth
from groups import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^groups/$', views.GetUserGroups.as_view(), name="load_groups"),
    url(r'^group/(?P<group_id>\d+)/$', views.GetGroupWall.as_view(), name="get_group_wall"),
    url(r'^group/(?P<group_id>\d+)/load/$', views.LoadGroupWall.as_view(), name="load_group_wall"),
    url(r'^owner/(?P<owner_id>[\d-]+)/video/(?P<video_id>\d+)/$', views.GetEmbedVideo.as_view(), name="get_embed_video"),
    url(r'^group/(?P<group_id>\d+)/load/offset/(?P<offset>\d+)/$', views.LoadPrevPosts.as_view(), name="load_prev_posts"),

    # social auth
    url(r'^social/', include('social_django.urls', namespace='social')),

    url(r'^logout/$', auth.logout, {'next_page': '/'}, name="logout"),
]
