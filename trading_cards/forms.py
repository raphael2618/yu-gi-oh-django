from django import forms

from trading_cards.models import Offer, Trade


class MakeOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "card"
        ]