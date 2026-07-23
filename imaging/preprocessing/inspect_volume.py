"""
Loads a NIfTI volume and prints its core properties.
"""

import nibabel as nib
import numpy as np

def inspect_nifti(filepath: str) -> None:
    img = nib.load(filepath)
    data = img.get_fdata()

    print(f"File: {filepath}")
    print(f"Shape (voxel dimensions): {data.shape}")
    print(f"Data type: {data.dtype}")
    print(f"Value range: min={data.min():.2f}, max={data.max():.2f}")

    print(f"\nAffine matrix (voxel -> world coordinates):\n{img.affine}")

    voxel_sizes = img.header.get_zooms()
    print(f"\nVoxel spacing (mm): {voxel_sizes}")


if __name__ == "__main__":
    inspect_nifti("data/raw/sample_mri/sample_t1.nii.gz")
