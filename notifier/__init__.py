import utils
from notifier.ambasada import AmbasadaOffer
from notifier.base import Offer
from notifier.pipa import PipaOffer, LodOffer
from robot import BaseRobot


class Notifier(BaseRobot):
    def _main(self) -> None:
        _, tweetless = utils.get_run_args()
        offer_classes: tuple[type[Offer], ...] = (AmbasadaOffer, PipaOffer, LodOffer)

        for class_ in offer_classes:
            offer = class_()
            offer.run()

            if offer.new_beers and not tweetless:
                offer.send_twitter_message()
