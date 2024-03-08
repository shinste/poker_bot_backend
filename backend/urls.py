from django.urls import path
from .views.initialize import Initialize
from .views.ai_move import AIMove
from .views.ai_suggestion import Suggestion
from django.contrib import admin

urlpatterns = [
    path('initiate/', Initialize.as_view(), name="initialize game"),
    path('ai_move/', AIMove.as_view(), name="move"),
    path('ai_suggest/', Suggestion.as_view(), name="suggestion"),
    path('', admin.site.urls, name="homepage"),
]