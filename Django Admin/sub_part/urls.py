from django.urls import path
from . import views

urlpatterns=[

    path('pdf/<pk>/',views.sales_render_pdf_view,name="sales_render_pdf_view"),

    path('',views.landing_page,name="landing_page"),
    path('home',views.home,name='home'),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(), name="activate"),

    path('index',views.index,name="index"),
    path('todo_add',views.todo_add,name='todo_add'),
    path('delete_todo/<int:id>', views.delete_todo),
    path('categories.html',views.categories,name="categories"),
    path('customer_analysis.html',views.customer_analysis,name="customer_analysis"),
    path('customer.html',views.customer,name="customer"),
    path('exp_categories.html',views.exp_categories,name="exp_categories"),
    path('expences.html',views.expences,name="expences"),
    path('products.html',views.products,name="products"),
    path('profile.html',views.profile,name="profile"),
    path('roles.html',views.roles,name="roles"),
    path('sales_list.html',views.sales_list,name="sales_list"),
    path('sales.html',views.sales,name="sales"),
    path('stock_analysis.html',views.stock_analysis,name="stock_analysis"),
    path('tax_report.html',views.tax_report,name="tax_report"),
    path('tax.html',views.tax,name="tax"),
    path('users.html',views.users,name="users"),
    path('vendors.html',views.vendors,name="vendors"),

    path('delete_users/<int:id>', views.delete_users),
    path('delete_roles/<int:id>', views.delete_roles),
    path('delete_customer/<int:id>', views.delete_customer),
    path('delete_vendors/<int:id>', views.delete_vendors),
    path('delete_products/<int:id>', views.delete_products),
    path('delete_categories/<int:id>', views.delete_categories),
    path('delete_tax/<int:id>', views.delete_tax),
    path('delete_sales_list/<int:id>', views.delete_sales_list),
    path('delete_expences/<int:id>', views.delete_expences),
    path('delete_exp_categories/<int:id>', views.delete_exp_categories),

    path('sales_list_view/<int:id>',views.sales_list_view,name='sales_list_view'),

    path('users_edit/<int:id>',views.users_edit,name='users_edit'),
    path('roles_edit/<int:id>',views.roles_edit,name='roles_edit'),
    path('customer_edit/<int:id>',views.customer_edit,name='customer_edit'),
    path('vendors_edit/<int:id>',views.vendors_edit,name='vendors_edit'),
    path('products_edit/<int:id>',views.products_edit,name='products_edit'),
    path('categories_edit/<int:id>',views.categories_edit,name='categories_edit'),
    path('tax_edit/<int:id>',views.tax_edit,name='tax_edit'),
    path('sales_list_edit/<int:id>',views.sales_list_edit,name='sales_list_edit'),
    path('expences_edit/<int:id>',views.expences_edit,name='expences_edit'),
    path('exp_categories_edit/<int:id>',views.exp_categories_edit,name='exp_categories_edit'),

    path('users_update/<int:id>',views.users_update,name='users_update'),
    path('roles_update/<int:id>',views.roles_update,name='roles_update'),
    path('customer_update/<int:id>',views.customer_update,name='customer_update'),
    path('vendors_update/<int:id>',views.vendors_update,name='vendors_update'),
    path('products_update/<int:id>',views.products_update,name='products_update'),
    path('categories_update/<int:id>',views.categories_update,name='categories_update'),
    path('tax_update/<int:id>',views.tax_update,name='tax_update'),
    path('sales_list_update/<int:id>',views.sales_list_update,name='sales_list_update'),
    path('expences_update/<int:id>',views.expences_update,name='expences_update'),
    path('exp_categories_update/<int:id>',views.exp_categories_update,name='exp_categories_update'),

]