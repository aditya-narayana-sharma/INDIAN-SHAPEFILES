import fiona
from fiona.transform import transform_geom
import os

# Define input and output directories
input_dir = "."  # Current folder or change as needed
output_dir = "./cleaned_geojson"
os.makedirs(output_dir, exist_ok=True)

# Iterate over all .geojson files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".geojson"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".geojson", "_clean.geojson"))

        print(f"\nProcessing file: {filename}")
        total = 0
        written = 0

        with fiona.open(input_path) as src:
            meta = src.meta
            with fiona.open(output_path, 'w', **meta) as dst:
                for feature in src:
                    total += 1
                    try:
                        feature["geometry"] = transform_geom(src.crs, src.crs, feature["geometry"])
                        dst.write(feature)
                        written += 1
                    except Exception as e:
                        print(f"  Skipped feature due to error: {e}")

        print(f"  Total features: {total}, Successfully written: {written}, Skipped: {total - written}")

print("\nCleaning complete. Cleaned files saved in:", output_dir)