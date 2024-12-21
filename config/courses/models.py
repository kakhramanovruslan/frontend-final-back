from django.db import models
from django.utils import timezone

from authenticate.models import User


COURSE_CATEGORY = (
    ('adobe photoshop', 'Adobe Photoshop'),
    ('adobe illustrator', 'Adobe Illustrator'),
    ('ui/ux design', 'UI/UX Design'),
    ('web development', 'Web Development'),
    ('mobile development', 'Mobile Development'),
    ('data science', 'Data Science'),
    ('Game development', 'Game Development')
)

SHIPPING_CITIES = (
    ('almaty', 'Алматы'),
    ('astana', 'Астана'),
    ('shymkent', 'Шымкент'),
    ('karaganda', 'Караганда'),
    ('aktobe', 'Актобе'),
    ('pavlodar', 'Павлодар'),
    ('semey', 'Семей'),
    ('atyrau', 'Атырау'),
    ('uralsk', 'Уральск'),
    ('kostanay', 'Костанай'),
    ('kokshetau', 'Кокшетау'),
    ('taraz', 'Тараз'),
    ('kyzylorda', 'Кызылорда'),
    ('aktau', 'Актау'),
)


SHIPPING_COST = {
    'almaty': 2000,
    'astana': 3500,
    'shymkent': 2200,
    'karaganda': 2300,
    'aktobe': 2400,
    'pavlodar': 2300,
    'semey': 2400,
    'atyrau': 2600,
    'uralsk': 2500,
    'kostanay': 2100,
    'kokshetau': 2150,
    'taraz': 2050,
    'kyzylorda': 2250,
    'aktau': 2450,
}

SHIPPING_DELIVERY_TIME = {
    'almaty': 1,
    'astana': 3,
    'shymkent': 2,
    'karaganda': 3,
    'aktobe': 5,
    'pavlodar': 5,
    'semey': 4,
    'atyrau': 5,
    'uralsk': 6,
    'kostanay': 3,
    'kokshetau': 3,
    'taraz': 2,
    'kyzylorda': 2,
    'aktau': 7,
}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(max_length=150, verbose_name='Категория', choices=COURSE_CATEGORY)
    image = models.ImageField(upload_to='uploads/courses/', verbose_name='Изображение курса')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_category_display(self):
        return dict(COURSE_CATEGORY)[self.category]

    def get_average_rating(self):
        ratings = CourseRating.objects.filter(course=self)
        if ratings:
            return round(sum([rating.rating for rating in ratings]) / len(ratings), 1)
        return 0

    def get_count_ratings(self):
        return CourseRating.objects.filter(course=self).count()

    def get_first_price(self):
        first_price = 110 * self.price / 100
        return first_price


class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='chapters')
    title = models.CharField(max_length=150, verbose_name='Название главы')
    description = models.TextField(verbose_name='Описание главы')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Глава курса'
        verbose_name_plural = 'Главы курсов'

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def get_count_lessons(self):
        return self.lessons.count()


class CourseLesson(models.Model):
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, verbose_name='Глава', related_name='lessons')
    title = models.CharField(max_length=150, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='reviews')
    text = models.TextField(verbose_name='Отзыв')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг')

    class Meta:
        ordering = ['id']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f"{self.course.title} - {self.rating}"


class CourseCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
    courses = models.ManyToManyField(Course, verbose_name='Курсы', related_name='carts', blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.user.email


class CourseLike(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано', blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Лайк курса'
        verbose_name_plural = 'Лайки курсов'

    def __str__(self):
        return self.course.title


class CourseCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    certificate_number = models.CharField(max_length=150, verbose_name='Номер сертификата')
    certificate_image = models.FileField(upload_to='uploads/certificates/', verbose_name='Изображение сертификата')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_shipping = models.BooleanField(default=False, verbose_name='Доставлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return f"{self.user.email} - {self.course.title} - {self.certificate_number}"


class ShippingCertificate(models.Model):
    certificates = models.ManyToManyField(CourseCertificate, verbose_name='Сертификаты', related_name='shipping_certificates')
    city = models.CharField(max_length=150, verbose_name='Город', choices=SHIPPING_CITIES)
    address = models.TextField(verbose_name='Адрес доставки')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    delivery_time = models.PositiveIntegerField(verbose_name='Время доставки')

    class Meta:
        ordering = ['id']
        verbose_name = 'Доставка сертификата'
        verbose_name_plural = 'Доставки сертификатов'

    def __str__(self):
        return f"{self.city} - {self.cost}"

    def get_city(self):
        return dict(SHIPPING_CITIES)[self.city]

    def get_delivery_time(self):
        current_date = timezone.now()
        date_elapsed = (current_date - self.created_at).days
        remaining_days = max(0, self.delivery_time - date_elapsed)

        return remaining_days


class CoursePurchase(models.Model):
    shipping_certificate = models.ForeignKey(ShippingCertificate, on_delete=models.CASCADE, verbose_name='Сертификат')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано', blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')

    class Meta:
        ordering = ['id']
        verbose_name = 'Покупка курса'
        verbose_name_plural = 'Покупки курсов'

    def __str__(self):
        return f"{self.user.email} - {self.total_cost}"
