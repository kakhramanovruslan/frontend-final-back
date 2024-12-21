from rest_framework import serializers
from courses.models import *


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()


class CourseAddReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ('course', 'user', 'text')
        extra_kwargs = {
            'user': {'read_only': True}
        }


class CourseReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = CourseReview
        fields = ('id', 'user', 'text', 'created_at')


class CourseChapterSerializer(serializers.ModelSerializer):
    count_lessons = serializers.IntegerField(source='get_count_lessons', read_only=True)

    class Meta:
        model = CourseChapter
        fields = ('id', 'title', 'description', 'count_lessons')


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name', read_only=True)
    category = serializers.CharField(source='get_category_display', read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_ratings = serializers.IntegerField(source='get_count_ratings', read_only=True)
    first_price = serializers.DecimalField(source='get_first_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'price', 'category', 'author', 'image')
        extra_kwargs = {
            'author': {'read_only': True}
        }


class CreateCourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ('course', 'title', 'description')


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'price', 'category', 'image')


class CourseDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name', read_only=True)
    category = serializers.CharField(source='get_category_display', read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_ratings = serializers.IntegerField(source='get_count_ratings', read_only=True)
    first_price = serializers.DecimalField(source='get_first_price', max_digits=10, decimal_places=2, read_only=True)
    reviews = serializers.SerializerMethodField()
    chapters = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return CourseReviewSerializer(reviews, many=True).data

    def get_chapters(self, obj):
        chapters = obj.chapters.all()
        return CourseChapterSerializer(chapters, many=True).data


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ('id', 'title', 'description', 'video_url')


class CoureChapterSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = CourseChapter
        fields = ('id', 'lessons')

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return CourseLessonSerializer(lessons, many=True).data


class CourseAddReviewAndRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = CourseReview
        fields = ('course', 'user', 'text', 'rating')
        extra_kwargs = {
            'user': {'read_only': True}
        }


class AddToCartSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()


class RemoveFromCartSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()


class CourseCartSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'price', 'image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


class CartSerializer(serializers.ModelSerializer):
    courses = CourseCartSerializer(many=True)

    class Meta:
        model = CourseCart
        fields = ('courses', )


class FavoriteSerializer(serializers.ModelSerializer):
    courses = CourseCartSerializer(many=True)

    class Meta:
        model = CourseLike
        fields = ('courses', )


class CreateShippingCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCertificate
        fields = '__all__'


class CourseCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificate
        fields = ('id', 'certificate_number', 'certificate_image', 'is_shipping')


class ShippingCertificateSerializer(serializers.ModelSerializer):
    certificates = CourseCertificateSerializer(many=True, read_only=True)

    class Meta:
        model = ShippingCertificate
        fields = ('id', 'certificates', 'city', 'address', 'cost', 'delivery_time')


class ShippingOrderCertificateSerializer(serializers.ModelSerializer):
    certificates = CourseCertificateSerializer(many=True, read_only=True)
    city = serializers.CharField(source="get_city", read_only=True)
    delivery_time = serializers.IntegerField(source="get_delivery_time", read_only=True)

    class Meta:
        model = ShippingCertificate
        fields = ('id', 'certificates', 'city', 'address', 'cost', 'delivery_time')


class ShippingCitySerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    cost = serializers.IntegerField()
    delivery_time = serializers.IntegerField()


class TotalCostSerializer(serializers.Serializer):
    city = serializers.ChoiceField(choices=SHIPPING_CITIES)


class CartCheckoutSerializer(serializers.Serializer):
    city = serializers.ChoiceField(choices=SHIPPING_CITIES)
    address = serializers.CharField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class CoursePurchaseSerializer(serializers.ModelSerializer):
    shipping = ShippingOrderCertificateSerializer(source='shipping_certificate', read_only=True)
    courses = serializers.SerializerMethodField()

    class Meta:
        model = CoursePurchase
        fields = ('id', 'total_cost', 'created_at', 'shipping', 'courses')

    def get_courses(self, obj):
        certificates = obj.shipping_certificate.certificates.all()
        courses = [certificate.course for certificate in certificates]
        return CourseCartSerializer(courses, many=True, context=self.context).data
