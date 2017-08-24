# Pi Frame

> Confirmed working on a Raspberry Pi Zero W.
> Other models should work similarly.

## Requirements

- Python 3
- pip (install `python3-pip`)
- `fbi`
- `systemd` (recommended)

## Installation

Scripts and services assume installation at `/opt/pi-frame/`.

1. Copy (via SCP/`rsync`) the `pi-frame-web` folder to `/opt/pi-frame` on the target.
1. Install the `pi-frame.service` file in `/etc/systemd/system/pi-frame.service`
1. Run `sudo systemctl daemon-reload` to load the service file
1. Run `sudo systemctl start pi-frame` to start the Pi Frame service.

Now, browse to `http://<your-ip-address>` in a browser. Use the "Albums" screen to add your photo directories, and the "Start" screen to launch a slideshow.

> There is an sample `landing-screen.service` file in `system/` that can be used as a landing/splash screen for your Pi. Requires `wget` and uses Unsplash Source.