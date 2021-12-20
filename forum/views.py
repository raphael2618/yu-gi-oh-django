from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages

from .forms import CommentForm
from .models import Forum, Comment


class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumView(ListView):
    model = Forum
    context_object_name = "forums"
    queryset = Forum.objects.order_by('-created_at')


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumCreate(SuccessMessageMixin, CreateView):
    model = Forum
    fields = ['title', 'desc']
    # widget = {'desc': forms.RadioSelect()}
    success_message = 'Forum was successfully created'
    success_url = reverse_lazy('forum')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumUpdateView(OwnerProtectMixin, UpdateView):
    model = Forum
    fields = ['title', 'desc']
    context_object_name = 'forums'
    template_name = 'forum/forum_update_form.html'

    # success_url = reverse_lazy('forum')

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.slug})


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumDetailView(DetailView):
    model = Forum
    context_object_name = 'forums'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comment'] = CommentForm()
        # context['additional'] = 'this is the value of the additional variable'
        return context


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumUserListView(ListView):
    context_object_name = "forums"  # has to be context of everything :)

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        print(self.user)
        print(Forum.objects.filter(user=self.user))
        return Forum.objects.filter(user=self.user)


@method_decorator(login_required, name='dispatch')
class ForumDeleteView(OwnerProtectMixin, DeleteView):
    model = Forum
    success_url = reverse_lazy('forum')
    context_object_name = 'forums'

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'The forum was Deleted !')
        return super(ForumDeleteView, self).delete(*args, **kwargs)

# todo: messages

# COMMENT
class CommentCreateView(CreateView):
    model = Comment
    fields = ['desc']

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})

    def form_valid(self, form):
        _forum = get_object_or_404(Forum, id=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.forum = _forum
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(OwnerProtectMixin, UpdateView):
    model = Comment
    fields = ['desc']
    template_name = 'forum/forum_update_comment.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(OwnerProtectMixin, DeleteView):
    model = Comment

    # success_url = reverse_lazy('forum')

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})

# todo: Maybe Paginate (YES OR NO?)
