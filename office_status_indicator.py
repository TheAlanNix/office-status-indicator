import json
import os
import time

import pytz

from datetime import datetime, timedelta, timezone

from calendar_setup import get_calendar_service
from unicornhatmini import UnicornHATMini

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)

# Global variables
OFFICE_STATUS_HOUR_START = int(os.getenv("OFFICE_STATUS_HOUR_START", 8))
OFFICE_STATUS_HOUR_END = int(os.getenv("OFFICE_STATUS_HOUR_END", 18))
OFFICE_STATUS_TZ = os.getenv("OFFICE_STATUS_TZ", "America/New_York")
OFFICE_STATUS_WARNING_MINUTES = int(os.getenv("OFFICE_STATUS_WARNING_MINUTES", 10))
OFFICE_STATUS_WEEK_START = int(os.getenv("OFFICE_STATUS_WEEK_START", 0))
OFFICE_STATUS_WEEK_END = int(os.getenv("OFFICE_STATUS_WEEK_END", 4))

def get_events():

    # Get the calendar service
    service = get_calendar_service()

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'

    print('Getting list of calendar events...')

    events_result = service.events().list(calendarId='primary',
                                          timeMin=now,
                                          maxResults=10,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def set_red():
    set_color(255, 0, 0)


def set_orange():
    set_color(255, 144, 0)


def set_green():
    set_color(0, 255, 0)


def set_off():
    set_color(0, 0, 0)


def set_color(r, g, b):
    unicornhatmini.set_all(r, g, b)
    unicornhatmini.show()


def read_datetime(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")


def main():

    current_time = datetime.now(timezone.utc)

    # Convert to the desired timezone
    pytz_timezone = pytz.timezone(OFFICE_STATUS_TZ)
    current_tz_time = current_time.astimezone(pytz_timezone)

    print(f"Current Time: {current_tz_time}")

    try:
        # Refresh calendar events
        events = get_events()
    except Exception:
        print("Failed to fetch calendar events from Google.")
        return

    # For each event
    for event in events:

        if event.get("transparency", "") == "transparent":
            continue

        # Get the datetime for the start/end of the event
        start_time = read_datetime(event["start"]["dateTime"])
        end_time = read_datetime(event["end"]["dateTime"])

        print(f"Next Calendar Event: {start_time}")

        if start_time < current_time < end_time:
            # In a Meeting
            set_red()
            return
        elif start_time < current_time + timedelta(minutes=OFFICE_STATUS_WARNING_MINUTES):
            # Meeting Soon
            set_orange()
            return
        else:
            break

    # If it's a weekday
    if OFFICE_STATUS_WEEK_START <= current_tz_time.weekday() <= OFFICE_STATUS_WEEK_END:

        # If we're during working hours
        if OFFICE_STATUS_HOUR_START <= current_tz_time.hour < OFFICE_STATUS_HOUR_END:

            # No current/upcoming meetings
            set_green()
            return

    print(f"Not working hours...")
    set_off()
    return


if __name__ == '__main__':

    while True:
        main()
        time.sleep(60)
