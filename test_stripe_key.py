# =====================================================================
# ZENITH_OS // DUAL-VARIABLE STRIPE DIAGNOSTIC
# =====================================================================
import os
import stripe

vault_env_path = "/Volumes/X9 Pro/Zenith Rebuild Main/vault/.env"
extracted_key = None

print("SYSTEM: Scanning vault file for any valid Stripe key identifiers...")
if os.path.exists(vault_env_path):
    with open(vault_env_path, "r") as f:
        for line in f:
            clean_line = line.strip()

            # Smart-match: Accept EITHER variable name seamlessly
            if ("STRIPE_SECRET_KEY" in clean_line or "STRIPE_API_KEY" in clean_line) and "=" in clean_line:
                parts = clean_line.split("=", 1)
                if len(parts) == 2:
                    extracted_key = parts[1].strip().strip('"').strip("'").strip("(").strip(")")
                    print(f"🎯 SYSTEM CHECK: Found matching line variable name: {parts[0].strip()}")
                    break

if extracted_key:
    stripe.api_key = extracted_key
    print(f"SUCCESS: Read raw token from file -> ({stripe.api_key[:12]}...)")

    try:
        print("SYSTEM: Pinging Stripe servers for verification...")
        account_details = stripe.Account.retrieve()
        print(f"\n🔒 AUTHENTICATION PASSED!")
        print(f" └── Connected to Account ID: {account_details.id}")
    except Exception as e:
        print(f"\n❌ STRIPE API REJECTION: {str(e)}")
else:
    print("\n❌ CRITICAL ERROR: Neither 'STRIPE_SECRET_KEY' nor 'STRIPE_API_KEY' was found inside vault/.env")