from porkbun_ddns import PorkbunDDNS
from porkbun_ddns.config import Config, DEFAULT_ENDPOINT

from apscheduler.schedulers.blocking import BlockingScheduler

import os
import json

sched = BlockingScheduler()

DEFAULT_CONFIG = {"key": "YOUR_API_KEY", "secret": "YOUR_API_SECRET", "domains": []}

CONFIG_PATH = "/config/config.json"

if not os.path.isfile(CONFIG_PATH):
    with open(CONFIG_PATH, "w", encoding="UTF-8") as f:
        json.dump(DEFAULT_CONFIG, f)
    print("Configuration created.")
    exit(0)

with open(CONFIG_PATH, "r", encoding="UTF-8") as f:
    config = json.load(f)

pb_objects = []

for domain in config["domains"]:
    parts = domain.rsplit(".", 2)

    pb = PorkbunDDNS(
        Config(DEFAULT_ENDPOINT, config["key"], config["secret"]), ".".join(parts[1:])
    )
    pb.set_subdomain(parts[0])

    pb_objects.append(pb)


@sched.scheduled_job("interval", hours=1)
def update():
    print("Updating...")
    for pb in pb_objects:
        pb.update_records()
    print("Updated.")


update()
sched.start()
