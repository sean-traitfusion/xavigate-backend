# backend/onboarding/trait_bundle_loader.py

import json
from pathlib import Path

BUNDLE_PATH = Path(__file__).parent / "trait_bundles.json"

def load_trait_bundles():
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_bundle_by_trait(trait_name: str):
    bundles = load_trait_bundles()
    for bundle in bundles:
        if bundle["trait"].lower() == trait_name.lower():
            return bundle
    return None