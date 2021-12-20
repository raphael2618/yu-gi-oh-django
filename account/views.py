from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from account.forms import UserSignupForm, ProfileViewForm
from account.models import Profile
from trading_cards.models import Card, Trade


class UserSignUp(CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = UserSignupForm
    success_url = 'home'
    failed_message = "The User couldn't be added"

    def form_valid(self, form):
        user_to_add = form.cleaned_data
        # check the data we get when the form is valid
        print("user_to_add", user_to_add)

        super(UserSignUp, self).form_valid(form)
        # inherit from ModelFormMixin : form_valid(form)
        # Saves the form instance, sets the current object for the view,
        # and redirects to get_success_url().

        print("---------form valid")

        # The form is valid, automatically sign-in the user
        user = authenticate(self.request, username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        if user is None:
            print("---------user none")
            # User not validated for some reason, return standard form_valid() response
            # Inherit from TemplateResponseMixin :
            # render_to_response(context, **response_kwargs)¶
            return self.render_to_response(
                self.get_context_data(form=form,
                                      failed_message=self.failed_message))

        else:
            print("-----------user good")
            # Log the user in
            login(self.request, user)
            # Redirect to success url
            return redirect(reverse(self.get_success_url()))


class ProfileView(UpdateView):
    model = Profile
    template_name = 'profile.html'
    form_class = ProfileViewForm
    success_url = reverse_lazy('home')


def my_deck(request):
    trade = Trade.objects.all()
    return render(request, 'my_deck.html', {'trade': trade})


class MyCard(DetailView):
    model = Card
    # todo: add details view for deck if relevant Maybe if time
