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
    path(
        "product-review/<int:pk>/",
        views.ProductReviewDetail.as_view(),
        name="product-review-detail",
    ),
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
    # seller reviews
    path(
        "seller-reviews/<int:pk>/",
        views.SellerReviewList.as_view(),
        name="seller-review-list",
    ),
    path(
        "seller-reviews/",
        views.SellerReviewCreate.as_view(),
        name="seller-review-create",
    ),
    path(
        "seller-review/<int:pk>/",
        views.SellerReviewDetail.as_view(),
        name="seller-review-detail",
    ),
    path(
        "seller-own-reviews/",
        views.SellerOwnReviews.as_view(),
        name="seller-own-reviews",
    ),
]
