from django.urls import path

import game.views

urlpatterns = [
    path("init/", game.views.init, name="init"),
    path("character/list", game.views.get_character_list, name="character_list"),
    path("character/random/<int:count>", game.views.get_character_random, name="character_random"),
]
