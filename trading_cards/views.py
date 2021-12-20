from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from trading_cards.forms import MakeOfferForm
from trading_cards.models import Card, Trade, Offer

class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.profile.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)

def index(request):
    trades = Trade.objects.filter(status='P').order_by('-timestamp')
    return render(request, 'trading_cards/index.html', {'trades': trades})


# def index_history(request):
#     # trades = Trade.objects.filter(status='F').order_by('-timestamp')
#     offers = Offer.objects.filter(status='A')
#     return render(request, 'trading_cards/indexHistory.html', {'offers':offers})

class indexHistory(LoginRequiredMixin, ListView):
    model = Offer
    template_name = "trading_cards/indexHistory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['offers'] = Offer.objects.filter(status="A").filter(Q(profile=profile)|Q(trade__profile=profile))
        return context
#     this required another query against the database !! check the one for OfferView and TradeView with QS...
# Q saved the project

def make_trade(request, card_id):
    card = Card.objects.get(pk=card_id)

    # if request.user.profile.trade_set.filter(card=card).exists():
    #     return redirect('home')

    if card not in request.user.profile.deck.all():
        # todo: add flash message - card does not belong for trade
        return redirect('home')

    trade = Trade.objects.get_or_create(
        card=card,
        profile=request.user.profile
    )
    # todo: message - trade successful (class Success, Danger) Toast materialize
    return redirect('home')

class MakeOfferView(LoginRequiredMixin, CreateView):
    model = Offer
    form_class = MakeOfferForm

    def form_valid(self, form):
        trade = Trade.objects.get(id=self.kwargs['trade_id'])
        offer = form.save(commit=False)
        offer.profile = self.request.user.profile
        offer.trade = trade
        offer.save()
        return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(MakeOfferView, self).get_context_data(**kwargs)
        form = MakeOfferForm()
        form.fields['card'].queryset = self.request.user.profile.deck.all()
        context['form'] = form
        trade = Trade.objects.get(id=self.kwargs['trade_id'])
        context['trade'] = trade
        context['edit'] = False
        return context

@login_required
def accept_offer(request, offer_id, accepted):
    offer = Offer.objects.get(pk=offer_id)
    trade = offer.trade
    if request.user != trade.profile.user:
        messages.warning(request, "You cannot do that man :(")
        return redirect('home')

    if accepted:
        offer.status = "A"
        trade.status = "F"
        offer.profile.deck.remove(offer.card)
        offer.profile.deck.add(trade.card)
        trade.profile.deck.remove(trade.card)
        trade.profile.deck.add(offer.card)
        trade.save()
        for ofer in trade.offers.filter(status="W"):
            ofer.status = 'D'
            ofer.save()

    else:
        offer.status = "D"

    offer.save()
    return redirect("home")


# OFFERS
class OfferView(LoginRequiredMixin, ListView):
    model = Offer
    context_object_name = 'offers'

    def get_queryset(self):
        qs = super(OfferView, self).get_queryset()
        qs = qs.filter(status='W')
        return qs


class UpdateOffer(LoginRequiredMixin, OwnerProtectMixin, UpdateView):
    model = Offer
    fields = ['card']
    context_object_name = 'offers'
    success_url = reverse_lazy('my_offer')

    def get_context_data(self, **kwargs):
        context = super(UpdateOffer, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class DeleteOffer(LoginRequiredMixin, OwnerProtectMixin, DeleteView):
    model = Offer
    context_object_name = 'offers'
    success_url = reverse_lazy('home')


# TRANSACTIONS
class TradeView(LoginRequiredMixin, ListView):
    model = Trade
    context_object_name = 'trades'
    # template_name = 'trading_cards/trade_list.html'

    def get_queryset(self):
        qs = super(TradeView, self).get_queryset()
        qs = qs.filter(status='P')
        return qs