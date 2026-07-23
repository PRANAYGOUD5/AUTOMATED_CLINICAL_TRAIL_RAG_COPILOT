"""
Computes real-world volume (in cm^3) of a target structure from a
predicted segmentation mask, correctly accounting for voxel spacing.
"""

import numpy as np


def compute_structure_volume_cm3(
    predicted_mask: np.ndarray,
    original_spacing_mm: tuple,
    original_shape: tuple,
    processed_shape: tuple,
    target_class: int = 1,
) -> float:
    voxel_count = np.sum(predicted_mask == target_class)

    scale_factors = [
        orig / proc for orig, proc in zip(original_shape, processed_shape)
    ]
    effective_spacing_mm = [
        spacing * scale for spacing, scale in zip(original_spacing_mm, scale_factors)
    ]

    voxel_volume_mm3 = np.prod(effective_spacing_mm)
    total_volume_mm3 = voxel_count * voxel_volume_mm3
    total_volume_cm3 = total_volume_mm3 / 1000.0

    return float(total_volume_cm3)


if __name__ == "__main__":
    fake_mask = np.zeros((64, 64, 64), dtype=int)
    fake_mask[20:30, 20:30, 20:30] = 1

    volume = compute_structure_volume_cm3(
        predicted_mask=fake_mask,
        original_spacing_mm=(1.0, 1.0, 1.0),
        original_shape=(128, 128, 128),
        processed_shape=(64, 64, 64),
        target_class=1,
    )

    print(f"Voxel count: {np.sum(fake_mask == 1)}")
    print(f"Computed structure volume: {volume:.2f} cm^3")
