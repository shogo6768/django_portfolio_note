from django.urls import path
from .views import  QuestionCreate, QuestionList, questionAnswer, QuestionUpdate, AnswerUpdate,\
                    QuestionDelete,  AnswerDelete, QuestionRequest


urlpatterns = [
    path('question_create', QuestionCreate.as_view(), name='question_create'),
    path('question_list/<int:pk>', QuestionList.as_view(), name='question_list'),
    path('question_answer/<int:pk>', questionAnswer, name='question_answer'),
    path('question_answer/<int:pk>/question_update',
         QuestionUpdate.as_view(), name='question_update'),
    path('question_answer/<int:pk>/question_request',
         QuestionRequest, name='question_request'),
    path('question_answer/<int:pk>/answer_update/<int:answer_pk>',
         AnswerUpdate.as_view(), name='answer_update'),
    path('question_answer/<int:pk>/question_delete',
         QuestionDelete.as_view(), name='question_delete'),
    path('question_answer/<int:pk>/answer_delete/<int:answer_pk>',
         AnswerDelete.as_view(), name='answer_delete'),
]

