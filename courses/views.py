from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Course, Category, Lesson, UserCourse, Rating
from .forms import RatingForm

def course_list(request):
    """Asosiy sahifada kurslar ro'yxati"""
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    
    # Qidiruv
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Kategoriya filteri
    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)
    
    # Sahifalash
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_id):
    """Kurs detail sahifasi"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    lessons = course.lesson_set.all()
    
    # Foydalanuvchi kursni sotib olganmi
    user_has_course = False
    if request.user.is_authenticated:
        user_has_course = UserCourse.objects.filter(user=request.user, course=course).exists()
    
    # Foydalanuvchining bahosi
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, course=course).first()
    
    # Baho berish
    if request.method == 'POST' and request.user.is_authenticated:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                user=request.user,
                course=course,
                defaults={'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
            )
            if not created:
                rating.rating = form.cleaned_data['rating']
                rating.comment = form.cleaned_data['comment']
                rating.save()
            messages.success(request, 'Bahoyingiz saqlandi!')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = RatingForm(instance=user_rating)
    
    context = {
        'course': course,
        'lessons': lessons,
        'user_has_course': user_has_course,
        'form': form,
        'user_rating': user_rating,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def lesson_detail(request, course_id, lesson_id):
    """Dars detail sahifasi"""
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Foydalanuvchi kursni sotib olganmi yoki dars bepulmi
    user_has_course = UserCourse.objects.filter(user=request.user, course=course).exists()
    if not lesson.is_free and not user_has_course:
        messages.error(request, 'Bu darsni ko\'rish uchun kursni sotib olishingiz kerak!')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Keyingi va oldingi darslar
    lessons = list(course.lesson_set.all())
    current_index = lessons.index(lesson)
    next_lesson = lessons[current_index + 1] if current_index < len(lessons) - 1 else None
    prev_lesson = lessons[current_index - 1] if current_index > 0 else None
    
    context = {
        'course': course,
        'lesson': lesson,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
    }
    return render(request, 'courses/lesson_detail.html', context)

@login_required
def purchase_course(request, course_id):
    """Kurs sotib olish"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Foydalanuvchi allaqachon kursni sotib olganmi
    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Siz allaqachon bu kursni sotib olgansiz!')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Bu yerda to'lov tizimi integratsiya qilinadi
    # Hozircha oddiy sotib olish
    UserCourse.objects.create(user=request.user, course=course)
    messages.success(request, f'{course.title} kursi muvaffaqiyatli sotib olindi!')
    
    return redirect('courses:course_detail', course_id=course.id)

@login_required
def my_courses(request):
    """Foydalanuvchining sotib olgan kurslari"""
    user_courses = UserCourse.objects.filter(user=request.user).select_related('course')
    
    context = {
        'user_courses': user_courses,
    }
    return render(request, 'courses/my_courses.html', context)



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm  # LoginForm ni ishlatyapsiz deb taxmin qilaman

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('courses:course_list')  # yoki kerakli sahifaga
            else:
                messages.error(request, 'Login yoki parol noto‘g‘ri!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})