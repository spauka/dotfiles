#!/usr/bin/python

import json
import random
import signal
import logging
import argparse
import subprocess
from time import sleep

from colorama import Fore, Style, init

from systemd.journal import JournalHandler
from systemd.daemon import notify
import requests

# Init terminal colors
init(autoreset=True)


# Colored output formatter
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Style.RESET_ALL)
        log_message = super().format(record)
        return f"{log_color}{log_message}{Style.RESET_ALL}"


# Set up a SystemD Logger
handler = JournalHandler()
handler.setLevel(logging.INFO)

# Add a handler
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# The URL to access the metadata service
METADATA_URL = "http://169.254.169.254/metadata/scheduledevents"
# This must be sent otherwise the request will be ignored
HEADER = {"Metadata": "true"}
# Current version of the API
QUERY_PARAMS = {"api-version": "2020-07-01"}

def retry(
    starting_retry_wait=1.0,
    multiplier=1.5,
    max_wait=300.0,
    exception: tuple[type[Exception], ...] | type[Exception] = Exception,
):
    """
    Decorator to add timeout with exponential backoff to function
    on exception
    """

    def retry_func(f):
        def f_with_retry(
            *args, retry_wait=starting_retry_wait, retry_count=0, max_wait=max_wait, **kwargs
        ):
            try:
                return f(*args, **kwargs)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if isinstance(e, exception):
                    wait_time = (retry_wait / 2) + random.uniform(1, retry_wait)
                    next_retry_wait = min(retry_wait * multiplier, max_wait)
                    logger.error(
                        (
                            "Retrying function %s due to exception %s. "
                            "Attempt %d. Waiting %.2f to try again.",
                        ),
                        f.__name__,
                        e.__class__.__name__,
                        retry_count,
                        wait_time,
                    )
                    sleep(wait_time)
                else:
                    raise e
            return f_with_retry(
                *args,
                retry_wait=next_retry_wait,
                retry_count=retry_count + 1,
                **kwargs,
            )

        return f_with_retry

    return retry_func


@retry(exception=(requests.exceptions.ConnectionError, requests.exceptions.Timeout))
def get_scheduled_events():
    resp = requests.get(METADATA_URL, headers=HEADER, params=QUERY_PARAMS, timeout=5.0)
    data = resp.json()
    return data


@retry(exception=(requests.exceptions.ConnectionError, requests.exceptions.Timeout))
def confirm_scheduled_event(event_id):
    # This payload confirms a single event with id event_id
    # You can confirm multiple events in a single request if needed
    payload = json.dumps({"StartRequests": [{"EventId": event_id}]})
    response = requests.post(
        METADATA_URL, headers=HEADER, params=QUERY_PARAMS, data=payload, timeout=5.0
    )
    return response.status_code


def cleanup_and_exit(_signum, _frame):
    """
    Cleanup and exit
    """
    logger.info("Received SIGTERM, cleaning up...")
    notify("STOPPING=1")
    exit(0)


def advanced_sample(last_document_incarnation):
    # Poll every second to see if there are new scheduled events to process
    # Since some events may have necessarily short warning periods, it is
    # recommended to poll frequently
    found_document_incarnation = last_document_incarnation
    while last_document_incarnation == found_document_incarnation:
        sleep(1)
        payload = get_scheduled_events()
        logger.debug(
            "Got DocumentIncarnation=%d. Last was %d.",
            payload["DocumentIncarnation"],
            last_document_incarnation,
        )
        found_document_incarnation = payload["DocumentIncarnation"]

    logger.debug("New payload: %r", payload)

    # We recommend processing all events in a document together,
    # even if you won't be actioning on them right away
    for event in payload["Events"]:

        # Events that have already started, logged for tracking
        if event["EventStatus"] == "Started":
            logger.info("Event started: %r", event)

        # Approve all user initiated events. These are typically created by an
        # administrator and approving them immediately can help to avoid delays
        # in admin actions
        elif event["EventSource"] == "User":
            logger.info("Confirming event %r", event)
            confirm_scheduled_event(event["EventId"])

        # For this application, freeze events less that 9 seconds are considered
        # no impact. This will immediately approve them
        elif (
            event["EventType"] == "Freeze"
            and int(event["DurationInSeconds"]) >= 0
            and int(event["DurationInSeconds"]) < 9
        ):
            confirm_scheduled_event(event["EventId"])

        elif event["EventType"] == "Preempt":
            logger.warning("Spot instance preempted. Shutting down!")
            try:
                subprocess.run(["/bin/sudo", "/bin/systemctl", "poweroff"], check=True)
            except subprocess.CalledProcessError as e:
                logger.error("Failed to shutdown system!", exc_info=e)
            cleanup_and_exit(None, None)

        # Events that may be impactful (for example, reboot or redeploy) may need custom
        # handling for your application
        else:
            logger.warning("Other event %r", event)

    return found_document_incarnation


def main():
    # Install signal handler on exit
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    # Parse arguments
    cmd_args = argparse.ArgumentParser("Azure spot instance shutdown service")
    cmd_args.add_argument("-v", "--verbose", action="store_true")
    args = cmd_args.parse_args()

    if args.verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

        formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    # Notify systemd that the service is ready to run
    notify("READY=1")
    # This will track the last set of events seen
    last_document_incarnation = -1

    logger.debug("Ready. Starting querying")
    try:
        while True:
            last_document_incarnation = advanced_sample(last_document_incarnation)
    except KeyboardInterrupt:
        cleanup_and_exit(None, None)


if __name__ == "__main__":
    main()
