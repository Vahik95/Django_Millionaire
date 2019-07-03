from django.conf import settings
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Question, Answer, GameRecord
from django.contrib.auth.decorators import login_required
import sys


class HomeView(View):
    login_required = True
    def get(self, request):
        game_records = GameRecord.objects.values().distinct().order_by('-score')[:10]
        user_best_score = GameRecord.objects.values().filter(user_name=request.user.first_name, user_surname=request.user.last_name).order_by('-score')[:1]
        
        context = {
            'records': game_records,
            'best_score': user_best_score,
        }
        return render(request, 'game/home.html', context)

    def post(self, request):
        pass

class AddQuestionView(View):
    login_required = True
    def get(self, request):
        return render(request, 'game/add_question.html')

    def post(self, request):
        question = Question()
        question.text = request.POST['text']
        question.weight = request.POST['weight']
        question.save()
        messages.success(request, 'The question is added')
        return render(request, 'game/add_question.html')

class AddAnswerView(View):
    login_required = True
    def get(self, request):

        return render(request, 'game/add_answer.html')

    def post(self, request):
        answer = Answer()
        answer.text = request.POST['text']
        question = get_object_or_404(Question, pk=request.POST['question'])
        answer.question = question
        if 'right' in request.POST:
            answer.right = True
        else:
            answer.right = False
        answer.save()
        messages.success(request, 'The answer is added')
        return render(request, 'game/add_answer.html')

class ModifyQuestionView(View):
    login_required = True

    def get(self, request):

        return render(request, 'game/modify_question.html')

    def post(self, request):

        return render(request, 'game/modify_question.html')

class ModifyAnswerView(View):
    login_required = True

    def get(self, request):

        return render(request, 'game/modify_answer.html')

    def post(self, request):

        return render(request, 'game/modify_answer.html')


class EditQuestionView(View):
    login_required = True

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        context = {
            'question': question,
        }
        return render(request, 'game/edit_question.html', context)

    def post(self, request,question_id):
        question = Question.objects.get(pk=question_id)
        question.text = request.POST['text']
        question.weight = int(request.POST['weight'])
        question.save()
        messages.success(request, 'Question is edited successfully!')
        return render(request, 'game/modify_question.html')

class EditAnswerView(View):
    login_required = True

    def get(self, request, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        context = {
            'answer': answer,
        }
        return render(request, 'game/edit_answer.html', context)

    def post(self, request,answer_id):
        answer = Answer.objects.get(pk=answer_id)
        answer.text = request.POST['text']
        question = Question.objects.get(pk=request.POST['question'])
        answer.question = question
        if 'right' in request.POST:
            answer.right = True
        else:
            answer.right = False
        answer.save()
        messages.success(request, 'Answer is edited successfully!')
        return render(request, 'game/modify_answer.html')

class DeleteQuestionView(View):
    login_required = True

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        question.delete()
        messages.success(request, 'Question is deleted successfully!')
        return render(request, 'game/modify_question.html')

class DeleteAnswerView(View):
    login_required = True

    def get(self, request, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        answer.delete()
        messages.success(request, 'Answer is deleted successfully!')
        return render(request, 'game/modify_answer.html')


class GameView(View):
    login_required = True
    questions = Question.randoms
    questions = questions.random(6)
    answers = Answer.objects.filter(question__in=questions)
    score = 0
    n = 1

    def get(self, request):
        context = {
            'answers': self.answers,
            'questions': self.questions[GameView.n],
            'score': GameView.score,
        }
        return render(request, 'game/game.html', context)

    def post(self, request):
        if GameView.n < 5:
            if request.POST.get(str(self.questions[GameView.n].id)):
                answer_check = Answer.objects.get(id=request.POST.get(str(self.questions[GameView.n].id)))
                if answer_check.right == True:
                    messages.success(request, 'The answer was right')
                    GameView.score += self.questions[GameView.n].weight
                else:
                    messages.warning(request, 'The answer was wrong')
                GameView.n += 1
                context = {
                    'answers': self.answers,
                    'questions': self.questions[GameView.n],
                    'score': GameView.score,
                }
                return render(request, 'game/game.html', context)
            else:
                messages.warning(request, 'Choose smth !!!')
                context = {
                    'answers': self.answers,
                    'questions': self.questions[GameView.n],
                    'score': GameView.score,
                }
                return render(request, 'game/game.html', context)
        else:
            game_record = GameRecord()
            game_record.user_name = request.user.first_name
            game_record.user_surname = request.user.last_name
            game_record.score = GameView.score
            game_record.save()
            context = {
                'score': GameView.score,
            }
            GameView.score = 0
            GameView.n = 1
            return render(request, 'game/finish.html', context)
