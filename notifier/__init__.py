from notifier.ambasada import AmbasadaOffer
from robot.base import BaseRobot


class Notifier(BaseRobot):
    def _main(self) -> None:
        for class_ in (AmbasadaOffer,):
            offer = class_()
            offer.run()

            if offer.new_beers:
                offer.set_tasted()
                offer.send_notification(self._args.notificationless)
