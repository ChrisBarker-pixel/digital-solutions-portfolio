import os
import time
import io
import google.genai as genai


def fire(app, prompt, filename):
    """🚀 IMAGEN_4_ULTRA: The Precision Strike for Zenith OS."""
    app.log_system("NEURAL_GATEWAY: Firing Imagen 4.0 Fast Strike...")

    # 🎯 TARGET CONFIGURATION
    project_id = "zenith-hub-2026-official"
    location = "us-central1"
    model_id = "imagen-4.0-fast-generate-001"
    service_key_path = "/Volumes/X9 Pro/Zenith Rebuild Main/serviceAccountKey.json"

    try:
        # 🛡️ AUTHENTICATION LATCH
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_key_path

        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )

        # 🎯 EXECUTE THE STRIKE
        response = client.models.generate_images(
            model=model_id,
            prompt=f"Sprout Wing Chun aesthetic, high-fidelity martial arts design: {prompt}",
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="BLOCK_ONLY_HIGH",
                output_mime_type="image/jpeg"
            )
        )

        if response.generated_images:
            img_obj = response.generated_images[0]
            img_bytes = None

            # 🧬 THE NESTED LATCH (Based on ATTR_MISMATCH report)
            # The 'image' attribute detected in your HUD contains the bytes.
            try:
                if hasattr(img_obj, 'image'):
                    # Check if it's the SDK 'Image' object with .image_bytes
                    if hasattr(img_obj.image, 'image_bytes'):
                        img_bytes = img_obj.image.image_bytes
                    # Check if 'image' itself is the bytes
                    elif isinstance(img_obj.image, bytes):
                        img_bytes = img_obj.image

                # Fallback for Pydantic 'model_dump' structure also detected in HUD
                if not img_bytes and hasattr(img_obj, 'model_dump'):
                    dump = img_obj.model_dump()
                    img_bytes = dump.get('image', {}).get('image_bytes')
            except Exception as e:
                app.log_system(f"⚠️ EXTRACTION_FAIL: {str(e)[:50]}")

            if img_bytes:
                # 🛠️ PATH LAW (X9 PRO)
                save_dir = "/Volumes/X9 Pro/Zenith Rebuild Main/sprout_official/generated/"
                save_path = os.path.join(save_dir, f"{filename}.jpg")
                os.makedirs(save_dir, exist_ok=True)

                with open(save_path, "wb") as f:
                    f.write(img_bytes)

                # 🔗 MANIFEST TO THE LATTICE GRID
                # This triggers your VisualLatch.manifest_image through zenith_visual_latch.py
                logic = "import zenith_visual_latch\nzenith_visual_latch.strike(app, self.node_id)"
                app.after(0, lambda: app.manifest_node(title="IMGEN_4", logic=logic))

                # LATCH FILEPATH TO THE NEWEST NODE
                time.sleep(0.5)
                new_id = app.manifest_count
                if new_id in app.active_lattice:
                    app.active_lattice[new_id]['path'] = save_path
                    app.log_system(f"✅ STRIKE_SUCCESS: Imagen 4.0 manifested Node_{new_id}.")
            else:
                app.log_system("⚠️ DATA_ERR: Bytes missing inside the 'image' object.")
        else:
            app.log_system("⚠️ DATA_ERR: Vertex returned zero images.")

    except Exception as e:
        app.log_system(f"🛑 FATAL_ERR: {str(e)[:100]}")