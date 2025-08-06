from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Kurs tavsifi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="Rasm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0

    @property
    def total_lessons(self):
        return self.lesson_set.count()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    title = models.CharField(max_length=200, verbose_name="Dars nomi")
    description = models.TextField(verbose_name="Dars tavsifi")

    # URL orqali yuklash (ixtiyoriy)
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")

    # Fayl orqali yuklash (kompyuterdan)
    video_file = models.FileField(
        upload_to='lesson_videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])],
        verbose_name="Video fayl"
    )

    duration = models.IntegerField(help_text="Daqiqalarda", verbose_name="Davomiyligi")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_free = models.BooleanField(default=False, verbose_name="Bepul")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan sana")

    class Meta:
        verbose_name = "Foydalanuvchi kursi"
        verbose_name_plural = "Foydalanuvchi kurslari"
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Baho"
    )
    comment = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Baho"
        verbose_name_plural = "Baholar"
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.rating}"



