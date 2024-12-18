from django.db import models
from django.contrib.auth.models import User

class QuizGenre(models.Model):
    """
    Model to represent different quiz genres/categories
    """
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class QuizQuestion(models.Model):
    """
    Model to store quiz questions with genre support
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]
    question_text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    genre = models.ForeignKey(QuizGenre, related_name='questions', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.question_text[:50]} - {self.genre.name if self.genre else 'No Genre'}"

class QuizOption(models.Model):
    """
    Model to store multiple choice options for each question
    """
    question = models.ForeignKey(QuizQuestion, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class QuizSession(models.Model):
    """
    Model to track quiz sessions with genre support
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(QuizGenre, on_delete=models.SET_NULL, null=True)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"Quiz Session for {self.user.username} - {self.genre.name if self.genre else 'Mixed'}"

class QuizAttempt(models.Model):
    """
    Model to track individual question attempts in a quiz session
    """
    session = models.ForeignKey(QuizSession, related_name='attempts', on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt for {self.question.question_text[:30]}"