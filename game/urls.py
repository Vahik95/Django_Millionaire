# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('game/', GameView.as_view(), name='game'),
    path('AddQuestionView/', AddQuestionView.as_view(), name='add_question'),
    path('AddAnswerView/', AddAnswerView.as_view(), name='add_answer'),
    path('ModifyQuestionView/', ModifyQuestionView.as_view(), name='modify_question'),
    path('ModifyAnswerView/', ModifyAnswerView.as_view(), name='modify_answer'),
    path('EditQuestionView/<int:question_id>', EditQuestionView.as_view(), name='edit_question'),
    path('EditAnswerView/<int:answer_id>', EditAnswerView.as_view(), name='edit_answer'),
    path('DeleteQuestionView/<int:question_id>', DeleteQuestionView.as_view(), name='delete_question'),
    path('DeleteAnswerView/<int:answer_id>', DeleteAnswerView.as_view(), name='delete_answer'),
]
