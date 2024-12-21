from notifier.ambasada import AmbasadaOffer
from notifier.base import Offer
from notifier.pipa import LodOffer, PipaOffer
from robot.base import BaseRobot


class Notifier(BaseRobot):
    def _main(self) -> None:
        offer_classes: tuple[type[Offer], ...]

        if self._args.ambasada:
            offer_classes = (AmbasadaOffer,)
        else:
            offer_classes = (AmbasadaOffer, PipaOffer, LodOffer)

        for class_ in offer_classes:
            offer = class_()
            offer.run()

            if offer.new_beers:
                offer.set_tasted()
                offer.send_notification(self._args.notificationless)
