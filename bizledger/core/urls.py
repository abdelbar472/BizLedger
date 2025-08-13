from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('fin/', GraphQLView.as_view(graphiql=True, schema=schema)),
]