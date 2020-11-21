# Office Status Indicator

## Summary

This is a project to create a Google Calendar integrated status indicator for home office use.

![Office Status Indicator](img/office_status_indicator.jpg)

This project utilizes the following hardware:
- [Raspberry Pi Zero W](https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header)
- [Unicorn HAT Mini](https://shop.pimoroni.com/products/unicorn-hat-mini)

## Requirements

- Docker installed on your Raspberry Pi
- A Google Project with the Calendar API enabled

## Setup

First, you'll need to create a Google Calendar API project.  There's a good tutorial [here](https://developers.google.com/calendar/quickstart/python).  Download the `credentials.json` file for the project - you'll need it to allow the project to access your Google calendar - and then either copy the file to your container and place it in the `/app` directory, or mount the file to the container from the host.

On the Raspberry Pi Zero W with the Unicorn HAT Mini, run the following command to download and run the container:
```
docker run -it \
           --name office-status \
           --privileged \
           --restart=always \
           --volume $(pwd)/credentials.json:/app/credentials.json:ro \
           alannix/office-status:latest
```

This will prompt you to visit a URL to authorize the script to have access to your Google Calendar.  Once you have gone through the authorization process, you'll receive an authorization code that you'll need to provide back to the application.  The authorization code is stored within the container, so you can safely exit (Control + c) and the container will restart and continue to run.

Once the application is authorized, it will check your Google Calendar for events every minute, determine if you're in a meeting, then update the state of the status light accordingly. 

## Configuration

You can tweak the operation of the script by providing any of the following environment variables:

| Name | Description | Type | Default |
|------|-------------|------|:---------:|
| OFFICE_STATUS_HOUR_START | The hour of the day that the status light should activate. | Integer | 8 |
| OFFICE_STATUS_HOUR_END | The hour of the day that the status light should de-activate. | Integer | 18 |
| OFFICE_STATUS_TZ | The timezone that should be used to determine working hours. | String | "America/New_York" |
| OFFICE_STATUS_WARNING_MINUTES | The number of minutes prior to the next meeting that the light should change to 'warning' status. | Integer | 10 |
| OFFICE_STATUS_WEEK_START | The integer representation of the day of the week to start the work week (Monday is 0 and Sunday is 6) | Integer | 0 |
| OFFICE_STATUS_WEEK_END | The integer representation of the day of the week to end the work week (Monday is 0 and Sunday is 6) | Integer | 4 |
