import utils
from notifier.ambasada import AmbasadaOffer
from notifier.base import Offer
from notifier.pipa import PipaOffer, LodOffer
from robot.base import BaseRobot


class Notifier(BaseRobot):
    def _main(self) -> None:
        offer_classes: tuple[type[Offer], ...] = (AmbasadaOffer, PipaOffer, LodOffer)

        for class_ in offer_classes:
            offer = class_()
            offer.run()

            if offer.new_beers and not self._args.tweetless:
                offer.send_twitter_message()
