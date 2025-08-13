from django.urls import path
from graphene_django.views import GraphQLView
from .schema import Query, Mutation

urlpatterns = [
    path('invoice/', GraphQLView.as_view(graphiql=True, query=Query, mutation=Mutation)),
]