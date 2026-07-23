"""
Reads a single DICOM file and prints key metadata tags.
"""

import pydicom
from pydicom.data import get_testdata_file


def inspect_dicom(filepath: str) -> None:
    ds = pydicom.dcmread(filepath)

    print(f"File: {filepath}")
    print(f"Patient ID: {ds.get('PatientID', 'N/A')}")
    print(f"Modality: {ds.get('Modality', 'N/A')}")
    print(f"Rows x Columns: {ds.Rows} x {ds.Columns}")
    print(f"Pixel Spacing (mm): {ds.get('PixelSpacing', 'N/A')}")
    print(f"Instance Number (slice order): {ds.get('InstanceNumber', 'N/A')}")

    pixel_array = ds.pixel_array
    print(f"Pixel array shape: {pixel_array.shape}")
    print(f"Pixel value range: min={pixel_array.min()}, max={pixel_array.max()}")


if __name__ == "__main__":
    sample_path = get_testdata_file("CT_small.dcm")
    inspect_dicom(sample_path)
