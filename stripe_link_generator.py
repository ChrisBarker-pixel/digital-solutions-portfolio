# =====================================================================
# ZENITH_OS // AUTOMATED MULTI-TENANT STRIPE PRICING LINK INJECTOR
# =====================================================================
import os
import stripe
import firebase_admin
from firebase_admin import credentials, db

# 1. Hardcode live Firebase Realtime Database URL directly into the engine
db_url = "https://zenith-hub-2026-official-default-rtdb.firebaseio.com/"

# 2. Dual-Variable Flexible Vault Scanner (Bypasses all cache traps)
vault_env_path = "/Volumes/X9 Pro/Zenith Rebuild Main/vault/.env"
extracted_key = None

if os.path.exists(vault_env_path):
    with open(vault_env_path, "r") as f:
        for line in f:
            clean_line = line.strip()
            if ("STRIPE_SECRET_KEY" in clean_line or "STRIPE_API_KEY" in clean_line) and "=" in clean_line:
                parts = clean_line.split("=", 1)
                if len(parts) == 2:
                    extracted_key = parts[1].strip().strip('"').strip("'").strip("(").strip(")")
                    break

if extracted_key:
    stripe.api_key = extracted_key
    print(f"SYSTEM: Vault sync complete. Active Token Secured: ({stripe.api_key[:12]}...)")
else:
    print("❌ CRITICAL ERROR: Could not locate a Stripe key inside your vault/.env file.")

if not firebase_admin._apps:
    cred = credentials.Certificate("/Volumes/X9 Pro/Zenith Rebuild Main/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {"databaseURL": db_url})


def automate_marketplace_billing_links():
    ref = db.reference("public_marketplace", url=db_url)
    snapshot = ref.get()

    if not snapshot:
        print("ERROR: Public marketplace data stream empty or unreadable.")
        return

    # 🚨 HARD SECURITY BOUNDARY: Define keys that must NEVER be processed for SaaS links
    EXCLUDED_PRIVATE_KEYS = [
        "STARWASH DETAILING STOREFRONT LINK",
        "SPROUT WING CHUN IDENTITY REGISTRY",
        "LOCAL ENTITY BUSINESS LICENSE VALIDATOR",
        "LOCAL FRANCHISE REVENUE DISTRIBUTER",
        "LOCAL MARKETING OFFICE COORDINATOR",
        "LOCAL SERVICE RANKING RADAR",
        "CUSTOMER REVIEW TEXT SENTIMENT SCANNER",
        "GOOGLE BUSINESS PROFILE SYNC PIPELINE",
        "YELP FOR BUSINESS INGRESS MONITOR",
        "CHARTER SCHOOL ROSTER INTEGRATOR",
        "STUDENT FACING RISK SCREENING LOOP"
    ]

    items_to_process = []
    if isinstance(snapshot, list):
        for index, data in enumerate(snapshot):
            if data:
                items_to_process.append((str(index), data))
    elif isinstance(snapshot, dict):
        for key, data in snapshot.items():
            if data:
                items_to_process.append((str(key), data))

    print(f"SYSTEM: Found {len(items_to_process)} total agent nodes inside database tree.")

    for node_str_key, node_data in items_to_process:
        # Check against string key names or object 'name' values
        node_name_upper = ""
        if isinstance(node_data, dict):
            node_name_upper = node_data.get("name", "").upper()

        # 🚨 FORCED ENFORCEMENT INTERCEPT: Drop out immediately if personal data match is triggered
        if any(private_key in node_str_key.upper() or private_key in node_name_upper for private_key in
               EXCLUDED_PRIVATE_KEYS):
            print(f"🛡️ SECURITY BLOCK: Skipping isolated personal business node -> [{node_str_key}]")
            continue

        if isinstance(node_data, dict) and node_data.get("stripe_link"):
            print(f"SKIPPING: [{node_str_key}] already contains active pricing item.")
            continue

        if isinstance(node_data, dict):
            name = node_data.get("name", f"Zenith Node {node_str_key}")
            price_str = node_data.get("rental_price", "$10.00")
            desc_str = node_data.get("desc", "Autonomous agent computation block.")
        else:
            name = f"Zenith Asset {node_str_key}: {str(node_data)[:25]}"
            price_str = "$10.00"
            desc_str = str(node_data)

        try:
            clean_price = int(float(price_str.replace("$", "").split("/")[0].strip()) * 100)
        except Exception:
            clean_price = 1000

        try:
            print(f"PROVISIONING: Creating Stripe billing assets for [{name}]...")

            product = stripe.Product.create(
                name=f"ZENITH: {name}",
                description=desc_str[:500],
                metadata={"node_key": node_str_key}
            )

            price = stripe.Price.create(
                product=product.id,
                unit_amount=clean_price,
                currency="usd",
                recurring={"interval": "month"} if "mo" in price_str.lower() else None
            )

            checkout_link = stripe.PaymentLink.create(
                line_items=[{"price": price.id, "quantity": 1}],
                metadata={"target_node_key": node_str_key}
            )

            if isinstance(node_data, dict):
                ref.child(node_str_key).update({"stripe_link": checkout_link.url})
            else:
                ref.child(node_str_key).set({"raw_data": node_data, "stripe_link": checkout_link.url})

            print(f"SUCCESS: Mapped secure payment link for [{name}] -> {checkout_link.url}")

        except Exception as e:
            print(f"FAILED TO PROVISION LINK FOR [{name}]: {str(e)}")


if __name__ == "__main__":
    automate_marketplace_billing_links()