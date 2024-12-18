import random
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import QuizAttempt, QuizGenre, QuizOption,QuizQuestion, QuizSession

# Create your views here.
def signUp(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                auth_login(request,user)
                messages.success(request, 'Account registered successfully!!')
                return HttpResponseRedirect('/home')
        else:
            form = UserCreationForm() 
        return render(request,'quiz/form.html',{'form':form,'link' : 'login','name':'Sign Up'})
    except:
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/signup')

def login(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Logged in successfully!!')
                    return HttpResponseRedirect('/home')
        else:
            form = AuthenticationForm()
        return render(request, 'quiz/form.html', {'form': form,"link":'signup','name':'Login'})
    except:
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def home(request):
    genre = QuizGenre.objects.all()
    return render(request,'quiz/home.html',{"genre":genre})
  
@login_required(login_url='/login')
def quiz(request,genre):
    try:
        genre = QuizGenre.objects.get(name=genre)
        questions = QuizQuestion.objects.filter(genre=genre).order_by('difficulty')
        session = QuizSession.objects.filter(user=request.user,is_active=True).first()
        index = 1
        quiz_data = []
        for question in questions:
            options = QuizOption.objects.filter(question=question)
            quiz_data.append({
                'id':question.id,
            'question_text': question.question_text,
            'difficulty': question.difficulty,
            'options':options,
        })
        if request.method=='POST':
            question_id = request.POST.get('id')
            selected_option = request.POST.get('selectedOption')
            selected_option = QuizOption.objects.filter(option_text=selected_option).first()
            question = QuizQuestion.objects.get(id=question_id)
            attempt = QuizAttempt.objects.create(session=session,question = question,selected_option=selected_option)
            options = QuizOption.objects.filter(question=question)
            correct = [op for op in options if op.is_correct]

            if selected_option in correct:
                attempt.is_correct=True
                session.correct_answers += 1
                attempt.save()  
            else:
                session.incorrect_answers += 1
    
            session.save()

            attempted = QuizAttempt.objects.filter(session=session)

            index=int(request.POST.get('index'))+1
            print(index)
            if len(quiz_data) < index:
                print('Yess')
                session.is_active=False
                session.save()
                papers = [{
                    'left': random.randint(0, 100),
                    'delay': random.randint(1, 5)  
                } for _ in range(30)]  # List of dictionaries with random values
                print('yessssssssssssssssssssssssssssssss')
                return render(request,'quiz/endPage.html',{'session':session,'attempted': attempted,'papers':papers})
            return render(request,'quiz/quiz.html',{'genre':genre.name,"question":quiz_data[index-1],'index':index,'numbers':[1,2,3,4]})

        elif not session:
            session = QuizSession.objects.create(user=request.user,genre=genre,total_questions=len(questions))
        return render(request,'quiz/quiz.html',{'genre':genre.name,"question":quiz_data[index-1],'index':index,'numbers':[1,2,3,4]})
    except:
        if session:
            session.is_active = False
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/home')

@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    sessions = QuizSession.objects.filter(user = user)
    print(sessions)
    return render(request,'quiz/dashboard.html',{"user":user,"sessions":sessions})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    messages.error(request, 'Logged out.')
    return HttpResponseRedirect('/login')
