from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    url(r'^view_idea/(?P<idea_id>\d+)$', views.view_idea, name='view_idea'),
    url(r'^post_idea/$', views.post_idea, name='post_idea'),
]
