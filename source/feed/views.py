from typing import Any
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from feed.forms import CommentForm, PostForm
from feed.models import PostModel, CommentModel
from datetime import datetime
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

class SearchResultsView(ListView):
    model = PostModel
    template_name = "search_results.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['this_objects'] = self.get_queryset()
        print(context['this_objects'])
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        this_objects = PostModel.objects.filter(
            Q(title__icontains=query) | 
            Q(text__icontains=query)
        )
        return this_objects
    

class FeedView(ListView):
    template_name = 'feed.html'
    context_object_name = 'post_obj'
    model = PostModel

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['post_obj'] = PostModel.objects.all().order_by('date_add')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:log_in'
    template_name = 'content/new_post.html'
    form_class = PostForm
    model = PostModel

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(kwargs)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        print(form.data)
        print(form.errors)
        print(self.request.POST.dict())
        return redirect('feed')
    
    def form_valid(self, form):
        print(self.request.user)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect('feed')
 

class PostDetailedView(FormMixin, DetailView):
    login_url = 'accounts:log_in'
    template_name = 'detailed_post.html'
    model = PostModel
    form_class = CommentForm
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'

    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('feed')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post_model = self.get_object()
        self.object.save()
        return super().form_valid(form)
    

class ModerateView(ListView):
    template_name='moderate.html'
    context_object_name = 'post_obj'
    model = PostModel

    def post(self, request, *args, **kwargs):
        mod = request.POST.get('mod')
        post = PostModel.objects.get(id=request.POST.get('postid'))
        answer = {}
        if mod == 'yes':
            post.moderate = 'M'
            post.date_moderate = datetime.now()
            answer['answer'] = 'Опубликовано'

        elif mod == 'no':
            post.moderate = 'U'
            answer['answer'] = 'Отклонено'

        post.save()
        return JsonResponse(answer)


class PostEditView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:log_in'
    model = PostModel
    form_class = PostForm
    template_name = 'content/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post_obj'

    def get_success_url(self, **kwargs):
        return reverse('feed')
    
    def get_context_data(self, **kwargs):
        kwargs['post_obj'] = self.get_object()
        kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)


class PostDeleteView(View):
    def post(self, request, *args, **kwargs):
        post = PostModel.objects.get(id=request.POST.get('postid'))
        answer = {}
        post.moderate = 'D'
        post.date_moderate = datetime.now()
        answer['answer'] = 'На удаление'
        post.save()
        return JsonResponse(answer)
    
class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        comment = CommentModel.objects.get(id=request.POST.get('commentid'))
        comment.delete()
        answer = {}
        answer['answer'] = 'Комментарий удален'
        return JsonResponse(answer)






    