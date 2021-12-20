from django.urls import path, include

from . import views
from .views import OfferView, DeleteOffer, UpdateOffer, TradeView

urlpatterns = [
    path('', views.index, name='home'),
    path('create_trade/<int:card_id>', views.make_trade, name='make_trade'),
    path('trades/', TradeView.as_view(), name='trades'),
    path('trades-history/', views.indexHistory.as_view(), name='trades-history'),
    path('make_offer/<int:trade_id>', views.MakeOfferView.as_view(), name='make_offer'),
    path('my_offer/', OfferView.as_view(), name='my_offer'),
    path('delete_offer/<int:pk>', DeleteOffer.as_view(), name='offer-delete'),
    path('edit_offer/<int:pk>', UpdateOffer.as_view(), name='offer-edit'),
    path('finalize-offer/<int:offer_id>/<int:accepted>', views.accept_offer, name='finalize-offer')
]