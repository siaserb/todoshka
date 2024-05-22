from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from todo_app.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    template_name = "todo_app/task_list.html"
    context_object_name = "task_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search"] = search
        return context

    def get_queryset(self):
        queryset = Task.objects.prefetch_related(
            "tags"
        ).order_by("done", "-datetime")
        search = self.request.GET.get("search", "")
        if search:
            return queryset.filter(content__icontains=search)
        return queryset


def toggle_do(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    return HttpResponseRedirect(reverse_lazy("todo-app:task-list"))


class TaskCreateView(generic.edit.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("todo-app:task-list")


class TaskUpdateView(generic.edit.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("todo-app:task-list")


class TaskDeleteView(generic.edit.DeleteView):
    model = Task
    success_url = reverse_lazy("todo-app:task-list")


class TagListView(generic.ListView):
    model = Tag
    template_name = "todo_app/tag_list.html"
    context_object_name = "tag_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search"] = search
        return context

    def get_queryset(self):
        queryset = Tag.objects.all()
        search = self.request.GET.get("search", "")
        if search:
            return queryset.filter(name__icontains=search)
        return queryset


class TagCreateView(generic.edit.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("todo-app:tag-list")


class TagUpdateView(generic.edit.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("todo-app:tag-list")


class TagDeleteView(generic.edit.DeleteView):
    model = Tag
    success_url = reverse_lazy("todo-app:tag-list")
