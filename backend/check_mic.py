import sounddevice as sd

print("🔍 Available audio devices:")
devices = sd.query_devices()
for i, device in enumerate(devices):
    print(f"{i}: {device['name']} — {device['max_input_channels']} input channels")

# Optional: try setting a default input manually
# Replace `0` with the correct index from the list above
try:
    sd.default.device = (0, None)  # (input_device_index, output_device_index)
    print("✅ Default input device set successfully.")
except Exception as e:
    print(f"❌ Failed to set default device: {e}")

