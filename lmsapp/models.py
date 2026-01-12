from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.utils import timezone
timezone.now

#python manage.py makemigrations
#python manage.py migrate

class Profile(models.Model):#for instructor
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to="media/author", blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_full_name(self):
        return self.user.get_full_name() or self.user.username


class Level(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name
    

class Language(models.Model):
    language = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.language
    
    
class Category(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def get_all_category(self):
        return Category.objects.all().order_by('id')
    
    
class Course(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )
    title = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to='media/featured_img/', null=True)
    featured_video = models.CharField(max_length=255, null=True)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField( null=True, default=0)
    discount = models.IntegerField(null=True)
    deadline = models.CharField(max_length=100, null=True)
    created_at = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=True, blank=True,  max_length=255)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    certificate = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title

    def get_related_courses(self):
        # Get related courses by category (excluding the current course)
        return Course.objects.filter(category=self.category).exclude(id=self.id)[:4]  # Limit to 4 related courses


class UserCourse(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title
    

class What_you_learn(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    points  = models.CharField(max_length=500)

    def __str__(self):
        return self.points
    

class Requirements(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    points  = models.CharField(max_length=500)

    def __str__(self):
        return self.points

    
class Video(models.Model):
    serial_number = models.IntegerField( null=True)
    thumbnail = models.ImageField(upload_to='Media/Yt_Thumbnail/', null=True)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson  = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=255)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    name  = models.CharField(max_length=500)
    
    def __str__(self):
        return f'{self.name}'
    
    
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    order_id =  models.CharField(max_length=255, null=True, blank=True)
    payment_id =  models.CharField(max_length=255, null=True, blank=True)
    user_course  = models.ForeignKey(UserCourse, on_delete=models.CASCADE,  null=True,)
    user  = models.ForeignKey(User, on_delete=models.CASCADE,  null=True,)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, default="Razorpay")  # Ensure this exists in the payment gateway
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Payment {self.order_id} - {self.status}"
    

class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

        
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lms_reviews', null=True)
    title = models.CharField(max_length=100)
    rating = models.FloatField()  # Rating between 1 to 5
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user} on {self.course}'


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=timezone.now)  # Link to User model
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='instructors/', null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    reviews = models.PositiveIntegerField(default=0)
    students = models.PositiveIntegerField(default=0)
    courses = models.PositiveIntegerField(default=0)
    bio = models.TextField()
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class InstructorApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    job_title = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    bio = models.TextField()
    experience = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    testimonial_text = models.TextField()
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # To avoid duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class Quiz(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    correct_answer = models.CharField(max_length=255)


class QuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class Question(models.Model):
    QUIZ_TYPE = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    )
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(choices=QUIZ_TYPE, max_length=3)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255, help_text="For MCQ, use one correct answer; for SA, store correct short answer.")
    
    def __str__(self):
        return f"{self.question_text} ({self.quiz.title})"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Assignment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.assignment.title}"


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.is_completed}"


class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField()
    quiz_scores = models.FloatField(null=True, blank=True)  # Store average quiz score
    progress_percentage = models.FloatField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.progress_percentage}%"


class LearningPath(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    courses = models.ManyToManyField(Course, through='LearningPathCourse', related_name='learning_paths')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LearningPathCourse(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  # Defines the sequence in the learning path

    class Meta:
        ordering = ['order']  # Orders the courses in the path

    def __str__(self):
        return f'{self.course.title} in {self.learning_path.name}'


class Prerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='main_course')
    prerequisite_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisite_course')

    def __str__(self):
        return f'{self.prerequisite_course.title} is a prerequisite for {self.course.title}'


class CertificateTemplate(models.Model):
    name = models.CharField(max_length=255)
    background_image = models.ImageField(upload_to='certificates/')
    template_html = models.TextField()  # Store HTML for rendering the certificate

    def __str__(self):
        return self.name


"""class Certificate(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_template = models.ForeignKey(CertificateTemplate, on_delete=models.CASCADE)
    awarded_on = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Certificate for {self.learner.username} in {self.course.title}'"""


class ForumThread(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forum_threads')
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.author.username} in {self.thread.title}'


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} at {self.timestamp}'


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')
    criteria = models.TextField()  # Optional field to define how to earn the badge

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.badge.name}'


class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.points} points'


class Poll(models.Model):
    question = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)


class PollResponse(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)


class EngagementMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    time_spent = models.DurationField()  # Store total time spent
    interactions = models.IntegerField(default=0)  # E.g., number of quiz attempts, video plays

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.time_spent} spent"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    description = models.TextField()

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date > timezone.now()


class SCORMPackage(models.Model):
    title = models.CharField(max_length=200)
    package_file = models.FileField(upload_to='scorm_packages/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class KnowledgeBase(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Can use rich text editor like CKEditor
    category = models.CharField(max_length=100, choices=[('general', 'General'), ('billing', 'Billing'), ('technical', 'Technical Support')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    STATUS_CHOICES = [('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, choices=[('general', 'General'), ('billing', 'Billing'), ('technical', 'Technical Support')])

    def __str__(self):
        return self.question