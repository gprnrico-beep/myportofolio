from django.urls import path
from main.views import (
    show_main,
    show_experience,
    show_projects,
    create_project,
    update_project,
    get_projects_json,
    delete_project,
    create_experience,
    update_experience,
    delete_experience,
    get_experiences_json,
    register,  
    login_user,
    logout_user,
    toggle_star,
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    
    #Authentication
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    # Projects
    path('projects/', show_projects, name='show_projects'),
    path('projects/add/', create_project, name='create_project'),
    path('projects/<uuid:project_id>/update/',update_project,name='update_project'),
    path('api/projects/', get_projects_json, name='get_projects_json'),
    path('projects/<uuid:project_id>/delete/', delete_project, name='delete_project'),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    
    
    # Experience
    path('experience/', show_experience, name='show_experience'),
    path('experience/add/', create_experience, name='create_experience'),
    path('experience/<uuid:experience_id>/update/', update_experience, name='update_experience'),
    path('experience/<uuid:experience_id>/delete/', delete_experience, name='delete_experience'),
    path('api/experience/', get_experiences_json, name='get_experiences_json'),
]