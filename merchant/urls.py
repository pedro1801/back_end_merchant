from django.urls import path

import merchant.views as views


urlpatterns = [
    path(
        "merchants/create/",
        views.MerchantCreateView.as_view(),
        name="merchant-create"
    ),
    path(
        "merchants/",
        views.MerchantListView.as_view(),
        name="merchant-list"
    ),
    path(
        "merchants/<int:merchant_id>/",
        views.MerchantIdView.as_view(),
        name="merchant-id"
    ),
    path(
        "merchants/status/<int:status_id>/",
        views.MerchantStatusView.as_view(),
        name="merchant-status"
    ),
    path(
        "merchants/<int:merchant_id>/update/",
        views.MerchantUpdateView.as_view(),
        name="merchant-update"
    ),
    path(
        "merchants/<int:merchant_id>/update/status/",
        views.MerchantUpdataStatusView.as_view(),
        name="merchant-update-status"
    ),
    path(
        "merchants/<int:merchant_id>/timeline/",
        views.MerchantTimeLineListView.as_view(),
        name="merchant-timeline"
    ),
    path("login/", views.LoginView.as_view(), name="login"),
]