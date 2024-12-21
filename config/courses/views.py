from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config import settings
from courses.models import Course, CourseChapter, CourseReview, CourseRating, COURSE_CATEGORY, CourseCart, CourseLike, \
    CourseCertificate, SHIPPING_COST, SHIPPING_DELIVERY_TIME, ShippingCertificate, CoursePurchase, SHIPPING_CITIES
from courses.serializers import CourseSerializer, CourseDetailSerializer, CoureChapterSerializer, \
    CourseReviewSerializer, CourseAddReviewSerializer, CourseAddReviewAndRatingSerializer, CourseCreateSerializer, \
    CreateCourseChapterSerializer, CategorySerializer, AddToCartSerializer, RemoveFromCartSerializer, CartSerializer, \
    FavoriteSerializer, CourseCartSerializer, CreateShippingCertificateSerializer, CartCheckoutSerializer, \
    ShippingCitySerializer, TotalCostSerializer, CoursePurchaseSerializer, CourseUpdateSerializer


class CategoryListView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        return dict(COURSE_CATEGORY)

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return Response(self.get_object())


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = None

    @swagger_auto_schema(
        tags=["courses"],
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.all()
        category = self.request.query_params.get('category')
        title = self.request.query_params.get('title')

        if category:
            queryset = queryset.filter(category=category)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset


class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response({'message': 'Курс успешно создан'}, status=201)


class CourseChapterCreateView(generics.CreateAPIView):
    serializer_class = CreateCourseChapterSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Глава успешно создана'}, status=201)


class CourseUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CourseUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['patch']

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(tags=["courses"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CourseDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(tags=["courses"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChapterLessonsView(generics.RetrieveAPIView):
    serializer_class = CoureChapterSerializer

    def get_object(self):
        return get_object_or_404(CourseChapter, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AddReviewAndRatingView(generics.CreateAPIView):
    serializer_class = CourseAddReviewAndRatingSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        data = request.data

        course = get_object_or_404(Course, pk=data.get('course'))
        user = request.user
        text = data.get('text')
        rating = data.get('rating')

        review = CourseReview.objects.create(course=course, user=user, text=text)
        CourseRating.objects.create(course=course, user=user, rating=rating)

        return Response({'message': 'Отзыв успешно добавлен'})


class AddToCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not CourseCart.objects.filter(user=user).exists():
            CourseCart.objects.create(user=user)

        if course_id in user.cart.courses.values_list('id', flat=True):
            return Response({'message': 'Курс уже добавлен в корзину'}, status=400)

        course = get_object_or_404(Course, pk=course_id)
        user.cart.courses.add(course)

        return Response({'message': 'Курс успешно добавлен в корзину'})


class AddToFavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if course_id in user.likes.values_list('id', flat=True):
            return Response({'message': 'Курс уже добавлен в избранное'}, status=400)

        course = get_object_or_404(Course, pk=course_id)
        CourseLike.objects.create(user=user, course=course)

        return Response({'message': 'Курс успешно добавлен в избранное'})


class RemoveFromCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveFromCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course = get_object_or_404(Course, pk=course_id)
        user.cart.courses.remove(course)

        return Response({'message': 'Курс успешно удален из корзины'})


class RemoveFromFavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveFromCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course = get_object_or_404(Course, pk=course_id)
        CourseLike.objects.filter(user=user, course=course).delete()

        return Response({'message': 'Курс успешно удален из избранного'})


class CartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        try:
            cart = request.user.cart
        except:
            cart = CourseCart.objects.create(user=request.user)

        serializer = self.serializer_class(cart, context={'request': request})
        return Response(serializer.data)


class FavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        likes = request.user.likes.all()
        courses = [like.course for like in likes]
        serializer = self.serializer_class(courses, many=True, context={'request': request})
        return Response(serializer.data)


class ShippingCertificatesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateShippingCertificateSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Сертификат успешно создан'})


class CityListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingCitySerializer

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        # Формируем список городов
        city_data = []
        for key, name in SHIPPING_CITIES:
            city_data.append({
                'key': key,
                'name': name,
                'cost': SHIPPING_COST.get(key, 0),
                'delivery_time': SHIPPING_DELIVERY_TIME.get(key, 0),
            })

        # Сериализуем данные
        serializer = self.serializer_class(city_data, many=True)
        return Response(serializer.data)


class TotalCostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TotalCostSerializer

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        user = request.user
        cart_courses = user.cart.courses.all()
        if not cart_courses:
            return Response({'message': 'Корзина пуста'}, status=400)

        city = kwargs.get('name_city')
        shipping_city = dict(SHIPPING_CITIES).get(city)

        if not shipping_city:
            return Response({'message': 'Город не найден'}, status=400)

        delivery_cost = SHIPPING_COST.get(city, 0)
        total_courses_cost = sum(course.price for course in cart_courses)
        total_cost = total_courses_cost + delivery_cost

        return Response({'total_cost': total_cost})


class CartCheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartCheckoutSerializer

    @transaction.atomic
    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user

        cart_courses = user.cart.courses.all()
        if not cart_courses:
            return Response({'message': 'Корзина пуста'}, status=400)

        certificates = []
        for course in cart_courses:
            certificate = CourseCertificate.objects.create(
                user=user,
                course=course,
                certificate_number=f"CERT-{user.id}-{course.id}"
            )
            certificates.append(certificate)

        city = request.data.get('city')
        address = request.data.get('address')

        if not city or not address:
            return Response({'message': 'Город и адрес доставки обязательны'}, status=400)

        delivery_cost = SHIPPING_COST.get(city, 0)
        delivery_time = SHIPPING_DELIVERY_TIME.get(city, 0)

        shipping = ShippingCertificate.objects.create(
            city=city,
            address=address,
            cost=delivery_cost,
            delivery_time=delivery_time
        )
        shipping.certificates.set(certificates)

        total_courses_cost = sum(course.price for course in cart_courses)
        total_cost = total_courses_cost + delivery_cost

        purchase = CoursePurchase.objects.create(
            shipping_certificate=shipping,
            user=user,
            total_cost=total_cost
        )

        # send email notification to user
        subject = 'Purchase confirmation'
        message = f"""
Your purchase has been confirmed.

Total cost: {total_cost} KZT.
Shipping address: {address}, {dict(SHIPPING_CITIES).get(city)}.
Delivery time: {delivery_time} days.

Courses:
{''.join([f"{idx}. {course.title} - {course.price} KZT. " for idx, course in enumerate(cart_courses, 1)])}


Thank you for your purchase!
Please, check your email for further details.

Best regards,
Courses team!
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        user.cart.courses.clear()

        return Response({'message': 'Покупка успешно оформлена'})


class OrderListView(generics.ListAPIView):
    serializer_class = CoursePurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CoursePurchase.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True, context={'request': request})

        return Response(serializer.data)