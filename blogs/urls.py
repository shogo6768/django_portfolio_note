from django.urls import path
from .views import PostDetail, searchfunc, AllContents, categoryfunc, RankingList, contact 

urlpatterns = [
    path('post/<int:pk>/detail/', PostDetail.as_view(), name='post_detail'),
    path('searchresult/',  searchfunc, name='search'),
    path('all_contents/', AllContents.as_view(), name='all_contents'),
    path('category/<str:slug>/', categoryfunc, name='category'),
    path('ranking/', RankingList.as_view(), name='ranking'),
    path('contact/', contact, name='contact'),
]
