from django.urls import path

from feedback import views

urlpatterns = [
    path(
        "product-reviews/<int:pk>/",
        views.ProductReviewList.as_view(),
        name="product-review-list",
    ),
    path("review/<int:pk>/", views.ProductReviewDetail.as_view(), name="review-detail"),
    path("user-reviews/", views.EcomUserProductReviews.as_view(), name="user-reviews"),
    path("comment/", views.ProductCommentList.as_view(), name="comment-list"),
    path("comment/<int:pk>", views.ProductComment.as_view(), name="comment-detail"),
    
    
]
