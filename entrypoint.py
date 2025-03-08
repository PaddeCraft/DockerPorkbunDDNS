from porkbun_ddns import PorkbunDDNS
from porkbun_ddns.config import Config, DEFAULT_ENDPOINT

from apscheduler.schedulers.blocking import BlockingScheduler

import os
import json

sched = BlockingScheduler()

DEFAULT_CONFIG = {"key": "YOUR_API_KEY", "secret": "YOUR_API_SECRET", "domains": []}
CONFIG_PATH = os.environ.get("CONFIG_PATH", "./config.json")

TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

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


if not TEST_MODE:
    update()
    sched.start()

    # Will never reach this point; for ease of understanding
    exit(0)

# Used primarily for CI/CD testing
if TEST_MODE:
    import random
    import time

    import requests
    import pydig

    resolver = pydig.Resolver(nameservers=["1.1.1.1"])

    rand2 = random.randint(0, 255)
    rand3 = random.randint(0, 255)
    rand4 = random.randint(0, 255)

    # Start with 10 as it is a private IP range
    rand_ip = f"10.{rand2}.{rand3}.{rand4}"

    r = requests.post(
        "https://api.porkbun.com/api/json/v3/ping",
        json={"secretapikey": config["secret"], "apikey": config["key"]},
    )
    j = r.json()
    if j["status"] != "SUCCESS":
        print("API key invalid or other error.")
        print(r.status_code, j)
        exit(1)

    actual_ip = j["yourIp"]

    print(f"Random IP: {rand_ip}")
    print(f"Actual IP (according to Porkbun API): {actual_ip}")

    full_domain = config["domains"][0]

    parts = full_domain.rsplit(".", 2)
    subdomain = parts[0]
    domain = ".".join(parts[1:])
    r2 = requests.post(
        "https://api.porkbun.com/api/json/v3/dns/editByNameType/"
        + domain
        + "/A/"
        + subdomain,
        json={
            "secretapikey": config["secret"],
            "apikey": config["key"],
            "ttl": 600,
            "content": rand_ip,
        },
    )

    if r2.status_code != 200:
        print("Error updating DNS record:", r2.status_code, r2.text)
        exit(1)

    print("DNS record updated.")

    timeout = time.time() + 320
    while True:
        if time.time() > timeout:
            print("Timeout.")
            exit(1)

        time.sleep(10)
        try:
            resolved_ip = resolver.query(full_domain, "A")[0]
            if resolved_ip == rand_ip:
                print("DNS propagated.")
                break
        except Exception as e:
            print("Error resolving:", e)
            exit(1)

        print(
            f"DNS not propagated yet: {full_domain} -> {resolved_ip}, expected {rand_ip}"
        )

    print("Updating DNS record.")
    pb_objects[0].update_records()

    timeout = time.time() + 320
    while True:
        if time.time() > timeout:
            print("Timeout.")
            exit(1)

        time.sleep(10)
        try:
            resolved_ip = resolver.query(full_domain, "A")[0]
            if resolved_ip != rand_ip:
                print("DNS propagated:", resolved_ip)
                break
        except Exception as e:
            print("Error resolving:", e)
            exit(1)

        print(
            f"DNS not propagated yet: {full_domain} -> {resolved_ip}, expected {actual_ip}"
        )

    print("Test complete.")
    exit(0)
