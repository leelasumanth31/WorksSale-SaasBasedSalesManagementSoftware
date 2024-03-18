from django.urls import path
from . import views

urlpatterns=[
    path('pdf/<pk>/',views.orders_render_pdf_view,name="orders_render_pdf_view"),
    path('',views.landing_page,name="landing_page"),
    path('home',views.home,name='home'),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('index',views.index,name='index'),
    path('todo_add',views.todo_add,name='todo_add'),
    path('delete_todo/<int:id>', views.delete_todo),
    path('coupons',views.coupons,name='coupons'),
    path('orders',views.orders,name='orders'),
    path('owners',views.owners,name='owners'),
    path('plans',views.plans,name='plans'),
    path('plans_delete/<int:id>',views.plans_delete,name='plans_delete'),
    path('delete_coupons/<int:id>', views.delete_coupons), 
    path('coupons_edit/<int:id>',views.coupons_edit,name='coupons_edit'),
    path('owners_edit/<int:id>',views.owners_edit,name='owners_edit'),
    path('coupons_update/<int:id>',views.coupons_update,name='coupons_update'),
    path('owners_update/<int:id>',views.owners_update,name='owners_update'),
    path('delete_owners/<int:id>', views.delete_owners),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(), name="activate"),
]