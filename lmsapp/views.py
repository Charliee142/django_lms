from django.shortcuts import render,  redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import *
from django.http import HttpResponse, JsonResponse,  Http404
from lmsapp.models import *
from django.template.loader import render_to_string
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from time import time
import datetime
from lmsproject.settings import *
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import razorpay # For Razorpay integration
#import stripe  # For Stripe integration
from razorpay import Client
from django.views import View
from django.db.models import Avg, Count
from django.http import FileResponse, Http404
from django.db import IntegrityError
#from zoomus import ZoomClient
import os
from django.db.models import Q
from .decorators import instructor_required
from django.db.models import Avg

#stripe.api_key = settings.STRIPE_SECRET_KEY  # Stripe API key
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET)) # razorpay API key
#client = ZoomClient('API_KEY', 'API_SECRET') # for zoom 
#client = razorpay.Client(auth=("rzp_test_1AcMMVMSYJKKXP", "nVEmjkJo6nDLxs7ke2PTs5Gq"))


def index(request):
    category = Category.objects.all().order_by('id')[:5]  # Get first 5 categories
    # Get all published courses, ordered by newest first
    course = Course.objects.filter(status='Publish').order_by('-id')  # Get all published courses

  

    #is_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()

    context = {
        'category': category,
        'course': course,
        #'is_enrolled': is_enrolled,
    }
    return render(request, 'lmsapp/index.html', context)


def single_course(request):
    category = Category.get_all_category(Category)
    course = Course.objects.all()
    #is_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()

    level = Level.objects.all()
    freecourse_count = Course.objects.filter(price= 0) .count()
    paidcourse_count = Course.objects.filter(price__gte = 1) .count()

    context ={
        'category':category,
        'course':course, 
        #'is_enrolled': is_enrolled,
        'level':level, 
        'freecourse_count':freecourse_count,
        'paidcourse_count':paidcourse_count,
    }
    return render(request, 'lmsapp/single_course.html', context)


def course_details(request, slug):

    # Fetch categories
    category = Category.get_all_category(Category)

    # Calculate the total time duration of the course videos
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))

    # Fetch the course object based on the slug
    course = get_object_or_404(Course, slug=slug)
    total_reviews = course.reviews.count()

    
    # Initialize rating breakdown (1 to 5 stars) with 0 counts
    rating_breakdown = {i: 0 for i in range(1, 6)}
    
    # Populate the actual counts from the database
    for item in course.reviews.values('rating').annotate(count=Count('id')).order_by('-rating'):
        rating_breakdown[item['rating']] = item['count']
    
    # Convert to a list of dictionaries
    rating_breakdown_list = [{'rating': i, 'count': count} for i, count in rating_breakdown.items()]

    # Get average rating and number of reviews
    reviews_summary = course.reviews.aggregate( avg_rating=Avg('rating'), total_reviews=Count('id'))
    rating_breakdown = course.reviews.values('rating').annotate(count=Count('id')).order_by('-rating')
    reviews = course.reviews.all()

    # Check if the user is enrolled in the course
    if request.user.is_authenticated:
        try:
            check_enroll = UserCourse.objects.get(user=request.user, course=course)
        except UserCourse.DoesNotExist:
            check_enroll = None
    else:
        check_enroll = None

    # Now that `course` is a single object, you can safely access `course.category`
    related_courses = Course.objects.select_related('category').filter(category=course.category).exclude(slug=course.slug)[:4]

    # Fetch the latest courses
    latest_courses = Course.objects.all().select_related('category').order_by('-created_at').exclude(slug=course.slug)[:5]

    # Prepare the context for rendering
    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'related_courses': related_courses,
        'latest_courses': latest_courses,
        'reviews_summary': reviews_summary,  # avg_rating and total_reviews
        'reviews': reviews,
        'total_reviews': total_reviews,
        'rating_breakdown': rating_breakdown_list,
    }

    # Render the course details page
    return render(request, 'lmsapp/course_details.html', context)


"""def filter_data(request):
    # Get filter values from the request (if any)
    category = request.GET.getlist('category[]')
    print("category")
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    # Start with all courses
    course = Course.objects.all()

    # Apply category filter if provided
    if category:
        course = course.filter(category__id__in=category)
    
    # Apply level filter if provided
    if level:
        course = course.filter(level__id__in=level)
    
    # Apply price filter based on the provided price option
    if price == ['PriceFree']:
        course = course.filter(price=0)
    elif price == ['PricePaid']:
        course = course.filter(price__gte=1)
    elif price == ['PriceAll']:
        pass  # No need to filter for "PriceAll" since we're already querying all courses

    # Optionally order courses (this example orders by latest added)
    course = course.order_by('-id')

    # Prepare the context for the template rendering
    context = {
        'course': course,
    }

    # Render the filtered courses to the template and return as JSON
    rendered_template = render_to_string('ajax/course.html', context)
    
    return JsonResponse({'data': rendered_template})"""

def filter_data(request):
    # Get filter values from the request (if any)
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['PriceFree']:
        course = Course.objects.filter(price = 0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte = 1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in = category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    context = {
        'course':course,
    }
    t = render_to_string('ajax/course.html', context)
    return JsonResponse({'data': t})
        

@login_required
def checkout(request, slug):
    course = get_object_or_404(Course, slug=slug)
    category = Category.objects.all()
    action = request.GET.get('action')
    order = None

    # Free Enrollment Logic
    if course.price == 0:
        UserCourse.objects.get_or_create(user=request.user, course=course)
        messages.success(request, "Course successfully enrolled for free!")
        return redirect('my_course')
    
    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')

            amount_cal = course.price - (course.price * course.discount / 100)
            amount = int(amount_cal) * 100
            currency = 'USD'
            notes = {
                'name': f'{first_name} {last_name}',
                'phone': phone,
            }
            receipt = f'charliee_{int(time())}'
            order = client.order.create(
                {
                'amount': amount,
                 'currency': currency, 
                 'notes': notes, 
                 'receipt': receipt,
                }
            )
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                order_id=order['id'],
            )
            payment.save()
    context = {
        'category': category,
        'course': course,
        'order': order,
    }
    return render(request, 'checkout/checkout.html', context)


@csrf_exempt
def verify_payment(request):
    course = Course.objects.all()
    if request.method == "POST":
        data = request.POST

        try:
            client = razorpay.Client(auth=("rzp_test_1AcMMVMSYJKKXP", "nVEmjkJo6nDLxs7ke2PTs5Gq"))
            client.utility.verify_payment_signature(data)

            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')

            # Fetch the payment object
            payment = get_object_or_404(Payment, order_id=razorpay_order_id)

            # Update payment details
            payment.payment_id = razorpay_payment_id
            payment.status = 'completed'
            payment.save()

            # Create the UserCourse record
            UserCourse.objects.get_or_create(user=payment.user, course=payment.course)

            messages.success(request, "Payment successfully verified!")
            context = {
                'data': data,
                'payment': payment,
                'course': course,

            }
            return render(request, 'verify_payment/payment_success.html', context)

        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed. Invalid signature.")
            return render(request, 'verify_payment/payment_fail.html')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'verify_payment/payment_fail.html')

    return render(request, 'verify_payment/payment_fail.html')



def page_not_found(request):
    category = Category.get_all_category(Category)

    context = {
        'category':category,
    }
    return render(request, 'error/404.html', context)


def my_course(request):
    # Fetch the courses the user is enrolled in
    course = UserCourse.objects.filter(user = request.user).select_related('course')
    
    context = {
        'course': course,
    }
    return render(request, 'mycourse/my_course.html', context)


def watch_course(request, slug):
    # Fetch the course using slug or return 404 if not found
    course = get_object_or_404(Course, slug=slug)

    # Get the lecture ID from the query parameters
    lecture_id = request.GET.get('lecture')

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Check if the user is enrolled in the course
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course)
    except UserCourse.DoesNotExist:
        return redirect('404')  # Redirect to 404 if user is not enrolled

    # Fetch the video for the given lecture ID
    try:
        video = Video.objects.get(id=lecture_id)
    except Video.DoesNotExist:
        raise Http404("Video not found")

    # Context to pass to the template
    context = {
        'course': course,
        'video': video,
       
    }
    return render(request, 'lmsapp/watch_course.html', context)


def submit_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user_id=request.user.id, course_id=course_id)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated successfully.')
                return redirect(url)
        except Review.DoesNotExist:
            print("Review does not exist for this user and course.")  # Debugging
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.title = form.cleaned_data['title']
                data.content = form.cleaned_data['content']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR', '')  # Capture user's IP address
                data.course = course  # Assign the course
                data.user = request.user # Assign the user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted successfully.')
                return redirect(url)
    else:
        form = ReviewForm()

    context = {
        'course': course,
        'form': form
    }
    return render(request, 'lmsapp/submit_review.html', context)


def download(request):
    # Adjust the file path without adding 'media' since MEDIA_ROOT already points to the media directory
    file_path = os.path.join(settings.MEDIA_ROOT, 'file.pdf')  # Correct path without 'media/media'

    # Debug: print the file path to verify
    print(f"Looking for file at: {file_path}")

    # Check if the file exists
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404("File not found.")


def top_instructors_view(request):
    instructors = Instructor.objects.order_by('-rating')[:5]  # Fetch the top 5 instructors 
    course = Course.objects.filter(status='Publish').order_by('-id')  # Get all published courses
    
    context = {
        'instructors': instructors,
        'course': course,
    }
    return render(request, 'instructors/instructors.html', context)


def instructor_detail_view(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    context = {
        'instructor': instructor,
    }
    return render(request, 'instructors/instructor_details.html', context)


def become_instructor(request):
    return render(request, 'instructors/become_instructor.html')


@login_required
def apply_as_instructor(request):
    try:
        # Check if user already has an application
        application = InstructorApplication.objects.get(user=request.user)
        messages.success(request, 'You have already applied as an Instructor.')
        return render(request, 'instructors/application_status.html', {'application': application})
    except InstructorApplication.DoesNotExist:
        # If no existing application, allow form submission
        if request.method == 'POST':
            form = InstructorApplicationForm(request.POST)
            if form.is_valid():
                # Save form and attach user to the application
                application = form.save(commit=False)
                application.user = request.user
                application.save()
                messages.success(request, 'Thank you! Your Application was submitted Successfully.')
                return render(request, 'instructors/application_status.html', {'application': application} )  # Redirect to a status page
        else:
            form = InstructorApplicationForm()
    return render(request, 'instructors/apply_as_instructor.html', {'form': form})


def search(request):
    query = request.GET.get('q')  # 'q' is the search term from the query parameters
    courses = None
    videos = None

    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
       # Filter videos by title (since 'description' does not exist in Video)
        videos = Video.objects.filter(
            Q(title__icontains=query) | Q(youtube_id__icontains=query)  # Adjust fields based on the actual model
        )

    context = {
        'courses': courses,
        'videos': videos,
        'query': query,
    }
    return render(request, 'lmsapp/search_results.html', context)


def testimonials_view(request):
    testimonials = Testimonial.objects.all()
    
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'testimonials/testimonials.html', context)


@login_required
def add_to_wishlist(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Try to create the wishlist item. If it already exists, the 'created' flag will be False.
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, course=course)
    
    if created:
        messages.success(request, 'This Course has been added to your wishlist.')
    else:
        messages.error(request, 'This Course is already in your wishlist.')
    
    # Redirect to the course detail page using the correct view name 'course_detail'.
    return redirect('course_details', slug=course.slug)


@login_required
def remove_from_wishlist(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, course=course)
    wishlist_item.delete()
    messages.success(request, 'This Course has been removed from your wishlist.')
    return redirect('wishlist')  # Redirect to wishlist page


@login_required
def wishlist(request):
    wishlist_courses = Wishlist.objects.filter(user=request.user).select_related('course')
    return render(request, 'wishlist/wishlist.html', {'wishlist_courses': wishlist_courses})


def contact(request):
    return render(request, 'lmsapp/contact.html')


def about(request):
    return render(request, 'lmsapp/about.html')


def search_course(request):
    category = Category.get_all_category(Category)

    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
   
    context = {
        'course':course,
        'category':category,
    }
    return render(request, 'search/search.html', context)


@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'account/profile.html', {'profile': profile})


@instructor_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user.instructor)
    return render(request, 'instructor/dashboard.html', {'courses': courses})


@instructor_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.instructor
            course.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    return render(request, 'instructor/create_course.html', {'form': form})


@instructor_required
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id, instructor=request.user.instructor)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'instructor/edit_course.html', {'form': form})


@instructor_required
def add_module(request, course_id):
    course = Course.objects.get(id=course_id, instructor=request.user.instructor)
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('edit_course', course_id=course.id)
    else:
        form = ModuleForm()
    return render(request, 'instructor/add_module.html', {'form': form, 'course': course})


@instructor_required
def edit_module(request, module_id):
    module = Module.objects.get(id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_detail', module_id=module.id)
    else:
        form = ModuleForm(instance=module)
    return render(request, 'instructor/edit_module.html', {'form': form, 'module': module})


@instructor_required
def add_lesson(request, module_id):
    module = Module.objects.get(id=module_id)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('edit_module', module_id=module.id)
    else:
        form = LessonForm()
    return render(request, 'instructor/add_lesson.html', {'form': form, 'module': module})


@instructor_required
def edit_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('edit_module', module_id=lesson.module.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'instructor/edit_lesson.html', {'form': form, 'lesson': lesson})


def instructor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'instructor'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')  # Redirect to homepage or a custom error page
    return wrapper_func


def complete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course
    profile = request.user.profile
    
    # Assume progress is stored as {'course_id': completion_percentage}
    progress = profile.progress
    lessons_completed = len(profile.completed_courses.filter(course=course))
    total_lessons = course.lesson_set.count()

    # Calculate progress
    progress[course.id] = (lessons_completed / total_lessons) * 100
    profile.progress = progress
    profile.save()

    return redirect('course_details', course.slug)


def send_enrollment_email(user, course):
    subject = f"Enrollment Confirmation for {course.title}"
    message = f"Hi {user.username},\n\nYou have successfully enrolled in {course.title}.\n\nEnjoy learning!"
    from_email = 'noreply@example.com'
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)


def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    
    if request.method == 'POST':
        form = QuizSubmissionForm(request.POST, quiz=quiz)
        if form.is_valid():
            feedback = []
            correct_answers = 0
            total_questions = quiz.questions.count()
            
            for question in quiz.questions.all():
                user_answer = form.cleaned_data.get(f'question_{question.pk}')
                if question.question_type == 'MCQ' or question.question_type == 'TF':
                    correct_choice = Choice.objects.get(pk=user_answer)
                    if correct_choice.is_correct:
                        correct_answers += 1
                    else:
                        feedback.append(f"Incorrect: {question.question_text}")
                elif question.question_type == 'SA':
                    if user_answer.lower() == question.correct_answer.lower():
                        correct_answers += 1
                    else:
                        feedback.append(f"Incorrect: {question.question_text}")

            # Calculate the score
            score = (correct_answers / total_questions) * 100
            return render(request, 'quiz_result.html', {'score': score, 'feedback': feedback})

    else:
        form = QuizSubmissionForm(quiz=quiz)

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'form': form})


def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.user = request.user
            submission.save()
            return redirect('assignment_success')

    else:
        form = AssignmentSubmissionForm()

    return render(request, 'assignment/submit_assignment.html', {'assignment': assignment, 'form': form})


def grade_assignment(request, submission_id):
    submission = AssignmentSubmission.objects.get(pk=submission_id)

    if request.method == 'POST':
        grade = request.POST['grade']
        feedback = request.POST['feedback']
        
        submission.grade = grade
        submission.feedback = feedback
        submission.save()

        return redirect('assignment_list')

    return render(request, 'assignment/grade_assignment.html', {'submission': submission})


def update_progress(user, course):
    total_quizzes = Quiz.objects.filter(course=course).count()
    completed_quizzes = QuizSubmission.objects.filter(user=user, quiz__course=course).count()
    
    total_assignments = Assignment.objects.filter(course=course).count()
    completed_assignments = AssignmentSubmission.objects.filter(user=user, assignment__course=course).count()
    
    total_items = total_quizzes + total_assignments
    completed_items = completed_quizzes + completed_assignments
    
    progress_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0
    
    # Update or create the progress entry for the user
    Progress.objects.update_or_create(
        user=user,
        course=course,
        defaults={'quizzes_completed': completed_quizzes, 'assignments_completed': completed_assignments, 'progress_percentage': progress_percentage}
    )


def view_learning_path(request, path_id):
    learning_path = get_object_or_404(LearningPath, id=path_id)
    courses = learning_path.courses.all().order_by('learningpathcourse__order')  # Order by sequence
    return render(request, 'learning/learning_path.html', {'learning_path': learning_path, 'courses': courses})


def check_prerequisites(user, course):
    prerequisites = Prerequisite.objects.filter(course=course)
    for prerequisite in prerequisites:
        # Check if the user has completed each prerequisite course
        completed = UserCourse.objects.filter(user=user, course=prerequisite.prerequisite_course, paid=True).exists()
        if not completed:
            return False
    return True


def award_certificate(user, course):
    template = CertificateTemplate.objects.first()  # You can allow users to select different templates
    certificate = Certificate.objects.create(
        learner=user,
        course=course,
        certificate_template=template
    )
    
    # Use the template to render the certificate with HTML
    certificate_html = render_to_string('certificate_template.html', {'user': user, 'course': course})
    return certificate


def view_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    return render(request, 'view_certificate.html', {'certificate': certificate})


def complete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user_course = UserCourse.objects.get(user=request.user, course=course)
    
    if not user_course.paid:
        return HttpResponseForbidden("You must be enrolled in the course.")
    
    # Mark the course as complete
    user_course.completed = True
    user_course.save()

    # Award a certificate
    award_certificate(request.user, course)
    
    return redirect('view_certificate', certificate_id=certificate.id)


def course_forum(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    threads = course.forum_threads.all()
    return render(request, 'course_forum.html', {'course': course, 'threads': threads})


def thread_detail(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    posts = thread.posts.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.thread = thread
            post.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = PostForm()

    return render(request, 'thread_detail.html', {'thread': thread, 'posts': posts, 'form': form})


def conversations_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'conversations_list.html', {'conversations': conversations})


def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(conversation=conversation, sender=request.user, content=content)

    messages = conversation.messages.all()
    return render(request, 'conversation_detail.html', {'conversation': conversation, 'messages': messages})


def announcements_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    announcements = course.announcements.all()
    return render(request, 'announcements_list.html', {'course': course, 'announcements': announcements})


def create_announcement(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Announcement.objects.create(course=course, title=title, content=content)
        return redirect('announcements_list', course_id=course.id)

    return render(request, 'create_announcement.html', {'course': course})


def schedule_zoom_meeting(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    meeting = client.meeting.create(
        topic=f'{course.title} - Live Session',
        start_time='2023-10-22T15:00:00Z',
        duration=60,  # in minutes
        timezone='UTC',
        settings={'host_video': True, 'participant_video': True}
    )
    
    # Save meeting link in the database
    meeting_link = meeting['join_url']
    course.zoom_link = meeting_link
    course.save()

    return redirect('course_details', course_id=course.id)


def user_badges(request, user_id):
    user = get_object_or_404(User, id=user_id)
    badges = user.badges.all()
    return render(request, 'user_badges.html', {'user': user, 'badges': badges})


def leaderboard(request):
    users_with_points = UserPoints.objects.order_by('-points')[:10]  # Top 10 users
    return render(request, 'leaderboard.html', {'users_with_points': users_with_points})


def learner_progress_report(request, user_id):
    user = get_object_or_404(User, id=user_id)
    progress_reports = CourseProgress.objects.filter(user=user)
    return render(request, 'learner_progress_report.html', {'progress_reports': progress_reports, 'user': user})


def track_engagement(user, course):
    metric, created = EngagementMetric.objects.get_or_create(user=user, course=course)
    # Update interactions count or time spent
    metric.interactions += 1  # Increment interactions, e.g., on quiz submission
    metric.save()


def track_time_spent(user, course, start_time):
    metric, created = EngagementMetric.objects.get_or_create(user=user, course=course)
    end_time = datetime.datetime.now()
    time_spent = end_time - start_time
    metric.time_spent += time_spent
    metric.save()


def engagement_metrics_report(request):
    metrics = EngagementMetric.objects.all().order_by('-time_spent')
    return render(request, 'engagement_metrics_report.html', {'metrics': metrics})


def custom_reports(request):
    if request.method == 'POST':
        # Get filters from form
        course_id = request.POST.get('course')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Filter progress reports based on criteria
        reports = CourseProgress.objects.filter(course__id=course_id, completed=True)
        if start_date and end_date:
            reports = reports.filter(course__created_at__range=[start_date, end_date])

        # Generate aggregate data, like average progress or quiz scores
        average_progress = reports.aggregate(Avg('progress_percentage'))
        average_quiz_score = reports.aggregate(Avg('quiz_scores'))

        return render(request, 'custom_reports.html', {
            'reports': reports, 
            'average_progress': average_progress,
            'average_quiz_score': average_quiz_score,
        })
    return render(request, 'custom_reports.html')


def help_center(request):
    articles = KnowledgeBase.objects.all()
    context = {'articles': articles}
    return render(request, 'help_center.html', context)


def submit_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_success')
    else:
        form = SupportTicketForm()
    return render(request, 'submit_ticket.html', {'form': form})


def ticket_list(request):
    tickets = SupportTicket.objects.filter(status='open')
    return render(request, 'ticket_list.html', {'tickets': tickets})


def faq(request):
    faqs = FAQ.objects.all()
    context = {'faqs': faqs}
    return render(request, 'faq.html', context)

