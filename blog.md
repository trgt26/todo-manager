# Django Todo App

Hi! today I will guide you through the process of creating a simple todo app using django.

## Getting the environment ready

Before we start make sure you have python installed in your system.

Now, we will start by creating a virtual environment. It will keep our dependencies isolated. So, open up the command prompt and execute the following command.

```shell
python -m venv venv
```
This will create a virtual environment named `venv`.


Then, by running the following command, we will activate our virtual environment.
```shell
source venv/bin/activate 
```

Now, to install django in `venv` run this command.

```shell
pip install django
```
## Creating project and app

Now, we will create django project, for that, execute the following command.

```
django-admin startproject todo_site
```
This will create some files and directories. Now, go inside the directory named `todo_site`.

Here, we will create an app by executing the following command.

```
python manage.py startapp todo
```
This will create an app named `todo` in the the current directory.

## Writing Models

Before we write model, we include our current app to the `settings.py` file. for that open, `todo_site/settings.py` file and add `todo` to `INSTALLED_APPS` list. The list will look like the following,

```py
INSTALLED_APPS = [
    'todo',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Now, open up `todo/models.py` file and add the following code.

```
class all_todo(models.Model) :
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
```

Then, go to the command prompt and make sure you are on the directory where `manage.py` file exists. Then executive the following commands.
```
python manage.py makemigrations

python mangage.py migrate
```
This will create a table named `todo_all_todo` in our database.
The columns of the table are `title`, `created_at`, `updated_at` and `is_completed`

## Defining URLs

Now, open up `todo/urls.py` file and add the following code.
```
urlpatterns = [
    path('', views.home, name='home'),

    path('<int:todo_id>/todo_delete', views.todo_delete, name='todo_delete'),

    path('<int:todo_id>/todo_update', views.todo_update, name='todo_update'),

    path('todo_create/', views.todo_create, name='todo_create'),
    path('<int:todo_id>/todo_edit/', views.todo_edit, name = 'todo_edit'),
    path('<int:todo_id>/todo_edit_save/', views.todo_edit_save, name='todo_edit_save')
]
```
Here, we have defined some url patterns. Here, we have used `path` function, the first parameter of the path function is a string that defines the URL pattern. Then the second parameter is a function name which is defined in the `views.py` file.
`<int:todo_id>` portion captures an integer parameter named `todo_id` from the url and passes to the function specified in the 2nd parameter.

Finally, the `name` parameter is a unique identifier for the URL pattern. It allows us to reference the pattern in other parts of our Django project.

Then, we need to add these url patterns to our project. For that, we update the `todo_site/urls.py` file with the following code.

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('todo.urls')),
    path('admin/', admin.site.urls),
]
```

Here, we needed to import the `include` function from `django.urls`.

## Writing Views

In Django, when a url is matched, a function from `views.py` is called. So, in the `views.py` file, we define different functions for different url patterns.

```py
from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import all_todo

# Create your views here.

def home(request) :
    todos = all_todo.objects.order_by('-created_at')
  
    data = {'data': todos}
    return render(request, 'home.html', context= data)

def todo_create(request):
    
    title = request.POST['todo-title']
    all_todo.objects.create(title= title)
    return redirect('todo:home')
  
def todo_delete(request, todo_id):
    
    dl = all_todo.objects.get(id = todo_id)
    dl.delete()

    return redirect('todo:home')

def todo_update(request, todo_id):
    
    todo_obj = all_todo.objects.get(id = todo_id)
    if todo_obj.is_completed == False:
        todo_obj.is_completed = True
    else :
        todo_obj.is_completed = False
    
    todo_obj.save()
    
    return redirect('todo:home')

def todo_edit(request, todo_id):
    todo = all_todo.objects.get(id= todo_id)
    print(todo.title)
    data = {
        "title":todo.title,
        "todo_id":todo_id
            }
    return render(request, 'edit.html', context=data)

def todo_edit_save(request, todo_id) :
    todo = all_todo.objects.get(id=todo_id)
    todo.title = request.POST['todo-title']
    todo.save()
    return redirect('todo:home')
```
Here, for the root url, we use `home` function. This function gets all the todos from our database and then passes the todos to `home.html` template.

To create, update and delete the todo, we define, `todo_create`, `todo_delete`, `todo_update` function. All of these functions perform create, delete and update operation respectively in the database. And then redirect to the root url. 

Then, we have `todo_edit` function, it uses `edit.html` template to edit the todos. And finally, `todo_edit_save` function save the modified todo to our database and redirect to the root url. 

## Writing Templates

By default, django searches for the template inside the `templates` directory of the app. So, we create a `templates` directory inside our `todo` app.

Then, we create `todo/templates/base.html` file.

```html
{% load static %}

<!doctype html>
<html lang="en">
    <head>
        <title>Django Todo</title>
        <!-- Required meta tags -->
        <meta charset="utf-8" />
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1, shrink-to-fit=no"
        />

        <!-- Bootstrap CSS v5.2.1 -->
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN"
            crossorigin="anonymous"
        />
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />

        <link rel="stylesheet" href="{% static 'style.css' %}">
    
    </head>

    <body>
        <div class="container-sm !justify !spacing offset-md-3 col-md-6 offset-lg-3 col-lg-5">
            <h1 class="text-center mt-3"> Django Todo</h1>
            
        {% block content%}
        {% endblock %}

        </div>

        <!-- Bootstrap JavaScript Libraries -->
        <script
            src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"
            integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r"
            crossorigin="anonymous"
        ></script>

        <script
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js"
            integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+"
            crossorigin="anonymous"
        ></script>
    </body>
</html>

```
Here, we include the cdn links for `bootstrap` and `font-awesome`. 

We may need to use static files in our template. For that, we have to specify the directory for static files.

For that, we open up the `todo_site/settings.py` file and at the end, we have added this code.
```py
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),
]
```
As a result, we can refer any static files inside `static_files` directory to our templates using relative path. 

Here, `{% load static %}` template tag means, we will use static files. Then, `<link rel="stylesheet" href="{% static 'style.css' %}">` means we include `static_files/style.css` file in our template.

```
{% block content%}
{% endblock %}
```
Then, this template tag is written so that, when we will extend the `base.html` template, we can write our desired code inside this section .

In `create.html`, we have written a html form.

```html
<form method ="post" action="{% url 'todo:todo_create' %}">
    {% csrf_token %}

    <div class="mb-3 mt-3">
        <input
            type="text"
            class="form-control"
            name="todo-title"
            id=""
            value=""
            aria-describedby="helpId"
            placeholder="Write your todo"
        />
      
    </div>
    <div class="text-center mb-3" >
        <button type="submit" class="btn btn-primary">
            Add Todo
        </button>
    </div>
</form>
```

We have used `{% csrf_token %}` template tag to protect against unauthorized cross-site requests.

In the `action` attribute we have used,
`{% url 'todo:todo_create' %}`
Here `url` is a template tag. `todo` is our app name and `todo_create` is the name of our url pattern.

Then, the `list.html` template is used to show all of our all todos.

```html
<div class="">
    
    <ul class="list-group">
        {% for todo in data %}
    
            <li class="list-group-item text-white {% if todo.is_completed == 1 %} bg-dark
            {% else %} bg-secondary
            {% endif %}            
            ">
                <div class="d-inline-flex justify-content-between col-12 {% if todo.is_completed == 1 %} cus-line-through {% endif %}">
                    <div>

                    <!-- UPDATE BUTTON -->
                    
                    {% if todo.is_completed == 0 %}
                    <a href="{% url 'todo:todo_update' todo.id %}" class=" cus-link">
                        <i class="fa-regular fa-square"></i>
                    </a>
                    {% else %}
                    <a href="{% url 'todo:todo_update' todo.id %}" class="cus-link">
                        <i class="fas fa-check-square"></i> 
    
                    </a>
                    {% endif %}    
                
                    <!-- TODO TITLE -->

                    {{ todo.title }}

                    </div>
                    <div class="d-flex justify-content-between col-1">
                        
                        <!-- EDIT BUTTON -->
                        
                        <div class="d-inline">
                            <a href="{% url 'todo:todo_edit' todo.id %}">
                                <p class="fas fa-edit text-white"></p>
                            </a>
                        </div>
                        
                        <!-- DELETE BUTTON -->

                        <div class="d-inline">
                            <a href="{% url 'todo:todo_delete' todo.id %}" class = "">
                                <p class="fa-solid fa-trash  text-danger"></p>
                            </a>
                        </div>
    
                    </div>

                </div>
            </li>
            
        {% endfor %}
    </ul>
</div>
```
Here, we iterate on all the todos using a `for` loop and using `if` condition we apply css classes.

we create `home.html` template with the following code.
```html
{% extends 'base.html' %}
{% block content %}
        {% include "create.html" %}
        {% include "list.html" %}
{% endblock %}
```
Here, we have extended `base.html` template and modified the `content` block of `base.html` template. In the content block, we have included `create.html` and `list.html` template.

For editing the todo, we have created `edit.html` template.

```html
{% extends 'base.html' %}

{% block content %}
<form method ="post" action="{% url 'todo:todo_edit_save' todo_id %}">
    {% csrf_token %}

    <div class="mb-3 mt-3">
        <input
            type="text"
            class="form-control"
            name="todo-title"
            id=""
            value="{{title}}"
            aria-describedby="helpId"
            placeholder="Write your todo"
        />
      
    </div>
    <div class="text-center mb-3" >
        <button type="submit" class="btn btn-primary">
            Save Changes
        </button>
    </div>
</form>
{% endblock %}
```
Here, we have extended the `base.html` template and we have used a html form to update the todo. In the action attribute, we have called the `todo_edit_save` url pattern to save the todo in database.

## Running The app

Now, to run our todo app, open up the command prompt to the directory where `manage.py` file is. And then, run the following command.
```shell
python manage.py runserver
```
Now, open your web browser and navigate to `http://127.0.0.1:8000/`. You should see the todo app, we have built.
