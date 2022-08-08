from django.apps import AppConfig
from django.core.signals import request_finished
import signal, sys
from ad.driver import driver, redis_cursor


def signal_handler(signal_num, frame):
    print(f"Remove Selenium Session from Redis: {redis_cursor.get('session')}")
    redis_cursor.set("session", "")
    driver.quit()


class AdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ad'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
        # Explicitly connect a signal handler.
        request_finished.connect(signals.my_handler)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


