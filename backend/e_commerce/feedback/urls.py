from django.urls import path

from feedback import views

urlpatterns = [
    # product review
    path(
        "product-reviews/<int:pk>/",
        views.ProductReviewList.as_view(),
        name="product-review-list",
    ),
    path(
        "product-reviews/",
        views.ProductReviewCreate.as_view(),
        name="product-review-create",
    ),
    path("review/<int:pk>/", views.ProductReviewDetail.as_view(), name="review-detail"),
    path("user-reviews/", views.CustomerProductReviews.as_view(), name="user-reviews"),
    # product comments
    path(
        "product-comments/<int:pk>/",
        views.ProductCommentList.as_view(),
        name="product-comment-list",
    ),
    path(
        "product-comments/",
        views.ProductCommentCreate.as_view(),
        name="product-comments-create",
    ),
    path(
        "comment/<int:pk>", views.ProductCommentDetail.as_view(), name="comment-detail"
    ),
    path(
        "user-comments/", views.CustomerProductComments.as_view(), name="user-comments"
    ),
]
