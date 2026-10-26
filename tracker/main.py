import logging

from .cli import Menu

logger = logging.getLogger(__name__)


def main():
    try:
        logging.basicConfig(
            filename="tracker.log",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
    except OSError:
        print("Cannot open tracker.log. Run from a folder you can write to.")
        return
    logger.info("Application started")
    menu = Menu()
    while True:
        try:
            menu.run()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception:
            logger.exception("Unexpected application error")
            print("Something went wrong. Details were saved to tracker.log. Returning to the menu.")
        else:
            break
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
