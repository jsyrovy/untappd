from notifier.ambasada import AmbasadaOffer
from notifier.base import Offer


def run() -> None:
    offer_classes: tuple[type[Offer]] = (AmbasadaOffer,)

    for class_ in offer_classes:
        offer = class_()
        offer.run()

        if offer.new_beers:
            offer.send_twitter_message()
