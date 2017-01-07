"""projekt_d1a URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django_1.views import say_hello
from django_1.views import random_result
from django_1.views import random_result2 
from django_1.views import random_result3 
from django_1.views import y_name 
from django_1.views import print_
from django_1.views import multiply     
from football.views import league_table
from football.views import games_played
from football.views import show_games
from football.views import list_players
from football.views import show_player
from football.views import show_team_statistics
from football.views import ShowPlayer2
from football.views import ShowTeam
from football.views import SetFavorite


from Forms.views import AddPlayer

from Forms.views import degrees
from Forms.views import add_game
from Forms.views import name_surname
from SesjeCookies.views import SetSession 
from SesjeCookies.views import ShowSession
from SesjeCookies.views import DeleteSession
from SesjeCookies.views import AddSession
from SesjeCookies.views import Login
from SesjeCookies.views import SetCookies
from SesjeCookies.views import ShowCookie
from SesjeCookies.views import DelCookie
from SesjeCookies.views import SetCookie2
from SesjeCookies.views import AddCookie
from SesjeCookies.views import ShowAllCookies

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello$', say_hello),
    url(r'^random$', random_result),
    url(r'^random/(?P<max_number>(\d){2,4})$',random_result2), # liczba musi mieć od 2 do 4 cyfr
    url(r'^random/(?P<min_number>(\d){2})/(?P<max_number>(\d){4})$',random_result3), 
    url(r'^hello/(?P<name1>([A-Z]){1}([a-z])+)$',y_name),
    url(r'^print$',print_),
    url(r'^multi$',multiply),
    url(r'^games$',games_played),
    url(r'^table$',league_table),
    url(r'^players$',list_players),
    url(r'^surname$',name_surname),
    url(r'^show_games/(?P<clubid>(\d)+)$',show_games),
    url(r'^show_player/(?P<player_id>(\d)+)$',show_player),
    url(r'^degrees$',degrees),
    url(r'^add$',add_game),

    url(r'^add_player$', AddPlayer.as_view()),

    url(r'^set_counter$', SetSession.as_view()),
    url(r'^show_counter$', ShowSession.as_view()),
    url(r'^del_counter$', DeleteSession.as_view()),
    url(r'^show_team_statistics/(?P<id_>(\d){1,2})$',show_team_statistics),
    url(r'^login$',Login.as_view()),
    url(r'^add_session$',AddSession.as_view()),
    url(r'^set_cookies$',SetCookies.as_view()),
    url(r'^show_cookies$',ShowCookie.as_view()),
    url(r'^del_cookies$',DelCookie.as_view()),
    url(r'^set_cookies2$',SetCookie2.as_view()),
    url(r'^show_player2$',ShowPlayer2.as_view()),
    url(r'^show_team$',ShowTeam.as_view()),
    url(r'^add_cookie$',AddCookie.as_view()),
    url(r'^all_cookie$',ShowAllCookies.as_view()),
    url(r'^set_favorite$',SetFavorite.as_view()),




    
    ]
