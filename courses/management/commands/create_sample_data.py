from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Lesson
from decimal import Decimal

class Command(BaseCommand):
    help = 'Test ma\'lumotlarini yaratish'

    def handle(self, *args, **options):
        # Kategoriyalar yaratish
        categories = [
            {
                'name': 'Dasturlash',
                'description': 'Dasturlash tillari va texnologiyalari'
            },
            {
                'name': 'Dizayn',
                'description': 'Grafik va web dizayn'
            },
            {
                'name': 'Biznes',
                'description': 'Biznes va marketing'
            },
            {
                'name': 'Til o\'rganish',
                'description': 'Chet tillarini o\'rganish'
            }
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Kategoriya yaratildi: {category.name}')

        # O'qituvchi yaratish
        instructor, created = User.objects.get_or_create(
            username='instructor',
            defaults={
                'email': 'instructor@example.com',
                'first_name': 'Professional',
                'last_name': 'O\'qituvchi'
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()
            self.stdout.write(f'O\'qituvchi yaratildi: {instructor.username}')

        # Kurslar yaratish
        courses_data = [
            {
                'title': 'Python dasturlash asoslari',
                'description': 'Python dasturlash tilini noldan boshlab o\'rganing. Bu kurs sizga Python asoslarini, sintaksisini va dasturlash mantiqini o\'rgatadi.',
                'category': 'Dasturlash',
                'price': Decimal('299000'),
                'lessons': [
                    {'title': 'Python haqida umumiy ma\'lumot', 'description': 'Python dasturlash tili haqida asosiy ma\'lumotlar', 'duration': 15, 'is_free': True},
                    {'title': 'O\'zgaruvchilar va ma\'lumot turlari', 'description': 'Python\'da o\'zgaruvchilar va ularning turlari', 'duration': 25, 'is_free': False},
                    {'title': 'Shartli operatorlar', 'description': 'if, elif, else operatorlari', 'duration': 30, 'is_free': False},
                    {'title': 'Tsikllar', 'description': 'for va while tsikllari', 'duration': 35, 'is_free': False},
                ]
            },
            {
                'title': 'Web dizayn asoslari',
                'description': 'HTML, CSS va JavaScript yordamida zamonaviy web saytlar yarating. Responsive dizayn va UX/UI tamoyillarini o\'rganing.',
                'category': 'Dizayn',
                'price': Decimal('199000'),
                'lessons': [
                    {'title': 'HTML asoslari', 'description': 'HTML markup tilini o\'rganish', 'duration': 20, 'is_free': True},
                    {'title': 'CSS stillar', 'description': 'CSS yordamida dizayn yaratish', 'duration': 30, 'is_free': False},
                    {'title': 'Responsive dizayn', 'description': 'Mobil qurilmalarga moslashuvchan dizayn', 'duration': 25, 'is_free': False},
                ]
            },
            {
                'title': 'Digital marketing',
                'description': 'Zamonaviy marketing strategiyalari va ijtimoiy tarmoqlarda reklama berish usullarini o\'rganing.',
                'category': 'Biznes',
                'price': Decimal('399000'),
                'lessons': [
                    {'title': 'Marketing asoslari', 'description': 'Marketing va uning turlari haqida', 'duration': 20, 'is_free': True},
                    {'title': 'Ijtimoiy tarmoqlarda reklama', 'description': 'Facebook, Instagram reklamalari', 'duration': 40, 'is_free': False},
                    {'title': 'SEO optimizatsiya', 'description': 'Qidiruv tizimlarida yuqori o\'rinlarda bo\'lish', 'duration': 35, 'is_free': False},
                ]
            },
            {
                'title': 'Ingliz tili boshlang\'ich',
                'description': 'Ingliz tilini noldan boshlab o\'rganing. Grammatika, so\'zlashuv va tinglash ko\'nikmalarini rivojlantiring.',
                'category': 'Til o\'rganish',
                'price': Decimal('0'),
                'lessons': [
                    {'title': 'Alifbo va talaffuz', 'description': 'Ingliz alifbosi va tovushlar', 'duration': 15, 'is_free': True},
                    {'title': 'Oddiy gap tuzish', 'description': 'Present Simple zamonini o\'rganish', 'duration': 25, 'is_free': True},
                    {'title': 'Kundalik so\'zlashuv', 'description': 'Oddiy so\'zlashuv iboralari', 'duration': 20, 'is_free': True},
                ]
            }
        ]

        for course_data in courses_data:
            category = Category.objects.get(name=course_data['category'])
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'category': category,
                    'instructor': instructor,
                    'price': course_data['price']
                }
            )
            
            if created:
                self.stdout.write(f'Kurs yaratildi: {course.title}')
                
                # Darslar yaratish
                for lesson_data in course_data['lessons']:
                    lesson = Lesson.objects.create(
                        course=course,
                        title=lesson_data['title'],
                        description=lesson_data['description'],
                        duration=lesson_data['duration'],
                        is_free=lesson_data['is_free'],
                        video_url='https://www.youtube.com/embed/dQw4w9WgXcQ'  # Test video
                    )
                    self.stdout.write(f'  - Dars yaratildi: {lesson.title}')

        self.stdout.write(self.style.SUCCESS('Barcha test ma\'lumotlari muvaffaqiyatli yaratildi!')) 