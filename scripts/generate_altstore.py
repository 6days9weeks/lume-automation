#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import plistlib
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--info-plist", required=True)
p.add_argument("--output", required=True)
p.add_argument("--repository", required=True)
p.add_argument("--tag", required=True)
p.add_argument("--build-number", required=True)
p.add_argument("--ipa-size", type=int, default=0)
a = p.parse_args()

with open(a.info_plist, "rb") as f:
    info = plistlib.load(f)

bundle = info.get("CFBundleIdentifier")
version = info.get("CFBundleShortVersionString")
build = str(info.get("CFBundleVersion", a.build_number))
name = info.get("CFBundleDisplayName") or info.get("CFBundleName") or "Lume"
if not bundle or not version:
    raise SystemExit("Missing CFBundleIdentifier or CFBundleShortVersionString in app Info.plist")

privacy = {
    k: v for k, v in info.items()
    if k.endswith("UsageDescription") and isinstance(v, str)
}
url = f"https://github.com/{a.repository}/releases/download/{a.tag}/Lume.ipa"
data = {
    "name": "6days9weeks Lume",
    "subtitle": "Automated builds of Lume for iPhone",
    "description": "Unsigned Lume builds. Install with AltStore Classic or SideStore using your own Apple ID.",
    "apps": [{
        "name": name,
        "bundleIdentifier": bundle,
        "developerName": "6days9weeks",
        "subtitle": "Lume iOS build",
        "localizedDescription": "Automated iOS build of Lume. Users provide their own lawful playlists and services.",
        "category": "entertainment",
        "versions": [{
            "version": str(version),
            "buildVersion": build,
            "date": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "localizedDescription": f"Automated build {build}.",
            "downloadURL": url,
            "size": a.ipa_size,
            "minOSVersion": str(info.get("MinimumOSVersion", "18.0"))
        }],
        "appPermissions": {
            "entitlements": [],
            "privacy": privacy
        }
    }],
    "news": []
}
Path(a.output).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
