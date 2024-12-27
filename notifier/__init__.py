from notifier.ambasada import AmbasadaOffer
from notifier.base import Offer
from notifier.pipa import LodOffer, PipaOffer
from robot.base import BaseRobot


class Notifier(BaseRobot):
    def _main(self) -> None:
        offer_classes = (AmbasadaOffer,) if self._args.ambasada else (AmbasadaOffer, PipaOffer, LodOffer)

        for class_ in offer_classes:
            offer = class_()
            offer.run()

            if offer.new_beers:
                offer.set_tasted()
                offer.send_notification(self._args.notificationless)
