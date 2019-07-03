from .models import Question, Answer

def info_processor(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()

    return {'questions': questions, 'answers': answers}
