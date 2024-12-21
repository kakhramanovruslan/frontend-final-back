from django.contrib import admin

from .models import *


admin.site.register(Course)
admin.site.register(CourseChapter)
admin.site.register(CourseLesson)
admin.site.register(CourseReview)
admin.site.register(CourseRating)
admin.site.register(CourseCart)
admin.site.register(CourseLike)
admin.site.register(CourseCertificate)
admin.site.register(ShippingCertificate)
admin.site.register(CoursePurchase)
