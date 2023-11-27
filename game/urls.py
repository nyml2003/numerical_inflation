from django.urls import path
import game.views
urlpatterns = [
    path("init/", game.views.init, name="init"),
    path("get_role_list/", game.views.get_role_list, name="get_role_list"),
    path("get_fight_couple/", game.views.get_fight_couple, name="get_fight_couple"),
    path("handle_fight/", game.views.handle_fight, name="handle_fight"),
    ]