from notifier.ambasada import AmbasadaOffer
from notifier.beerstreet import BeerStreetOffer
from robot.base import BaseRobot


class Notifier(BaseRobot):
    def _main(self) -> None:
        for class_ in (AmbasadaOffer, BeerStreetOffer):
            offer = class_()
            offer.run()

            if offer.new_beers:
                offer.set_tasted()
                offer.send_notification(self._args.notificationless)
