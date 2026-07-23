"""
Visualizes a single 2D slice from the middle of a 3D volume.
"""

import nibabel as nib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def visualize_middle_slice(filepath: str, output_path: str) -> None:
    img = nib.load(filepath)
    data = img.get_fdata()

    if data.ndim == 4:
        data = data[:, :, :, 0]

    mid_slice_index = data.shape[2] // 2
    mid_slice = data[:, :, mid_slice_index]

    plt.figure(figsize=(6, 6))
    plt.imshow(mid_slice.T, cmap="gray", origin="lower")
    plt.title(f"Middle slice (index {mid_slice_index})")
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Saved visualization to {output_path}")


if __name__ == "__main__":
    visualize_middle_slice(
        "data/raw/sample_mri/sample_t1.nii.gz",
        "data/processed/middle_slice.png",
    )
