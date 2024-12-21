from django.urls import path

from .views import *

urlpatterns = [
    path('get-category-list/', CategoryListView.as_view(), name='get-category-list'),

    path('get-course-list/', CourseListView.as_view(), name='get-course-list'),
    path('get-course-detail/<int:pk>/', CourseDetailView.as_view(), name='get-course-detail'),
    path('get-chapter-lessons/<int:pk>/', ChapterLessonsView.as_view(), name='get-chapter-lessons'),

    path('add-course/', CourseCreateView.as_view(), name='add-course'),
    path('add-course-chapter/', CourseChapterCreateView.as_view(), name='add-course-chapter'),
    path('edit-course/<int:pk>', CourseUpdateView.as_view(), name='edit-course'),
    path('delete-course/<int:pk>', CourseDeleteView.as_view(), name='delete-course'),

    path('add-review-and-rating/', AddReviewAndRatingView.as_view(), name='add-review-and-rating'),

    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('add-to-favorite/', AddToFavoriteView.as_view(), name='add-to-favorite'),

    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('remove-from-favorite/', RemoveFromFavoriteView.as_view(), name='remove-from-favorite'),

    path('get-cart/', CartView.as_view(), name='get-cart'),
    path('get-favorite/', FavoriteView.as_view(), name='get-favorite'),

    path('get-cities/', CityListView.as_view(), name='get-cities'),
    path('get-total-cost/<str:name_city>', TotalCostView.as_view(), name='get-total-cost'),
    path('checkout/', CartCheckoutView.as_view(), name='checkout'),

    path('get-orders/', OrderListView.as_view(), name='get-orders'),
]