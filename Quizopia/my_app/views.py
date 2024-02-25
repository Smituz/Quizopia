from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, alogin
from django.contrib import messages
from django.http import HttpResponse
from .models import User_info,Quetions,Quiz,Participants
import os


# Create your views here.


def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]        
        alluser = User_info.objects.all()
        for user in alluser:
            if user.username==username:
                if user.password==password:
                    alogin(request, user)
                    # request.session['user_id'] = user.id
                    request.session['username']=username
                    # user_info = User_info.objects.get(username=username)
                    return redirect("home")
                else:
                    messages.info(request, "Incorrect Password")
                    return redirect("login")
        messages.info(request, "Username Does not exist")   
    return render(request, "login.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        name=request.POST.get('name')
        password=request.POST.get('password')
        if User_info.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect("register")
        ins = User_info(username=username , email=email , password=password , name=name)
        ins.save()
        messages.info(request, "Registerd Successfully.")
        return redirect("login")
    return render(request, "register.html")

def home(request):
    username=request.session['username']
    user_info=User_info.objects.get(username=username)
    context={
        'user1' : user_info,
    }
    return render(request, "home.html" , context)

def gen_quiz(request):
    username=request.session['username']
    user_info=User_info.objects.get(username=username)
    context={
        'user1' : user_info,
    }
    if request.method=="POST":
        quiz=Quiz()
        quiz.quiz_name= request.POST.get('quiz_name')
        quiz.username=user_info
        quiz.marks_pr_que=request.POST.get('marks_per_question')
        quiz.description=request.POST.get('description')
        quiz.save()
        print(quiz.quiz_code)
        request.session['quiz_code']=quiz.quiz_code
        return render(request, "addquestion.html" ,context)
    return render(request, "generate_quiz.html" ,context)

def add_que(request):
    username=request.session['username']
    user_info=User_info.objects.get(username=username)
    quiz_code=request.session['quiz_code']
    
    quiz=Quiz.objects.get(quiz_code=quiz_code)
    print(quiz)
    context={
        'user1' : user_info,
    }
    if request.method=="POST":
        question=Quetions()
        question.quiz=quiz
        question.que= request.POST.get('que')
        question.op1=request.POST.get('op1')
        question.op2=request.POST.get('op2')
        question.op3=request.POST.get('op3')
        question.op4=request.POST.get('op4')
        question.ans=request.POST.get('ans')
       
        question.save()
        
        return render(request, "addquestion.html" ,context)
    return render(request, "generate_quiz.html" ,context)

    
   

def join_quiz(request):
    username=request.session['username']
    user_info=User_info.objects.get(username=username)
    context={
        'user1' : user_info,
    }
    if request.method=="POST":
        quiz_code=request.POST['quiz_code']
        quiz=Quiz.objects.all()
        for i in quiz:
            if(i.quiz_code==quiz_code):
                request.session['quiz_code']=quiz_code
                
                
                return redirect("play")
        messages.info(request,"Enter Correct Code")
    return render(request, "join_quiz.html",context)

def play(request):
    username=request.session['username']
    quiz_code=request.session['quiz_code']
    user_info=User_info.objects.get(username=username)
    quiz=Quiz.objects.get(quiz_code=quiz_code)
    question=Quetions.objects.filter(quiz=quiz)
    count=0

    for i in question:
        count+=1
    count1=range(count)
    context={
        'user1' : user_info,
        'quiz1' : quiz,
        'q1'    : question,
        'cnt'   : count1
    }
    return render(request,"play.html",context)


def calculate_score(request):
    if request.method == 'POST':
        # Fetch user info and quiz details
        username = request.session['username']
        user_info = User_info.objects.get(username=username)
        quiz_code = request.session['quiz_code']
        quiz = Quiz.objects.get(quiz_code=quiz_code)
        questions = Quetions.objects.filter(quiz=quiz)

        # Create a dictionary of correct answers for the quiz {question_id: correct_answer}
        correct_answers = {str(question.id): question.ans for question in questions}

        # Retrieve submitted answers from the POST data
        submitted_answers = {}
        for key, value in request.POST.items():
            if key.startswith('answer'):
                question_id = key.replace('answer', '')
                submitted_answers[question_id] = value

        # Debugging output
        print("Correct Answers:", correct_answers)
        print("Submitted Answers:", submitted_answers)

        # Calculate the score
        # score = sum(1 for question_id, submitted_answer in submitted_answers.items() if submitted_answers.get(submitted_answer) == correct_answers.get(question_id, None))
        # Sample dictionaries
        score = 0
        for i in submitted_answers:
            for j in correct_answers:
                if submitted_answers.get(i)== correct_answers.get(j):
                    score+=quiz.marks_pr_que
        
        
        # Optionally, save the user's score or any other relevant data
        participant=Participants()
        participant.username=user_info
        participant.quiz=quiz
        participant.score=score
        participant.save()
        context={
             'user1' : user_info,
             'quiz1' : quiz,
             'q1'    : questions,
             'score' :score,
        }
        return render(request,"score.html",context)

# views.py



def dashboard(request):

    username = request.session['username']
    user_info = User_info.objects.get(username=username)
    user_participations = Participants.objects.filter(username=user_info)
    
    # Create a list to store quiz names and scores
    quiz_scores = []
    for participation in user_participations:
        quiz_name = participation.quiz.quiz_name
        score = participation.score
        quiz_scores.append((quiz_name, score))
    print(quiz_scores)
    # Pass the data to the template
    context = {
        'quiz_scores': quiz_scores,
        'user1' : user_info,
    }
    
    # Render the dashboard template with the data
    return render(request, 'dashboard.html', context)

