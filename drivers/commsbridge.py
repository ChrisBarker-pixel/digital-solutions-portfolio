
class CommsBridge(OmniBase):
    def __init__(self, engine):
        super().__init__(engine)
        self.name = "CommsBridge_v1"
        self.id = 23
        self.hz = 329.63 # Note E
        self.tag = "COMMS"
        self.announce_ignition()

    def execute(self, **kwargs):
        payload = kwargs.get("payload", {})
        ad_text = payload.get("ad", "")

        # Format for WhatsApp (URL Encoding for 'api.whatsapp.com/send?text=')
        import urllib.parse
        encoded_message = urllib.parse.quote(ad_text)
        wa_link = f"https://api.whatsapp.com/send?text={encoded_message}"

        self.log_to_engine(f"📱 COMMS: WhatsApp Dispatch ready for {payload.get('order_id')}.", "SUCCESS")

        # Mirror the Dispatch State
        self.update_node_state(f"WA_LINK_{payload.get('order_id')}", {"link": wa_link})

        return wa_link
