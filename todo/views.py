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

