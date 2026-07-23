"""
Core preprocessing pipeline: intensity clipping, normalization, and resizing.
"""

import numpy as np
from scipy.ndimage import zoom


def clip_intensity(volume: np.ndarray, min_val: float = -1000, max_val: float = 400) -> np.ndarray:
    """
    Clips extreme intensity values before normalizing.
    Defaults tuned for CT (Hounsfield Units): -1000 = air, 400 = dense bone.
    """
    return np.clip(volume, min_val, max_val)


def normalize_intensity(volume: np.ndarray) -> np.ndarray:
    """Rescales values to the [0, 1] range using min-max normalization."""
    v_min, v_max = volume.min(), volume.max()
    if v_max - v_min == 0:
        return np.zeros_like(volume)
    return (volume - v_min) / (v_max - v_min)


def resize_volume(volume: np.ndarray, target_shape: tuple, is_label: bool = False) -> np.ndarray:
    """
    Resizes a 3D volume to a fixed target shape.
    is_label=True uses nearest-neighbor interpolation (order=0) to keep
    segmentation mask values as valid discrete classes.
    is_label=False uses cubic interpolation (order=3) for smooth intensity data.
    """
    zoom_factors = [t / s for t, s in zip(target_shape, volume.shape)]
    interpolation_order = 0 if is_label else 3
    return zoom(volume, zoom_factors, order=interpolation_order)


def preprocess_volume(volume: np.ndarray, target_shape: tuple = (128, 128, 128)) -> np.ndarray:
    """Full pipeline: clip -> normalize -> resize, in that order."""
    volume = clip_intensity(volume)
    volume = normalize_intensity(volume)
    volume = resize_volume(volume, target_shape, is_label=False)
    volume = np.clip(volume, 0, 1)  # guard against cubic interpolation overshoot
    return volume


if __name__ == "__main__":
    import nibabel as nib

    img = nib.load("data/raw/sample_mri/sample_t1.nii.gz")
    data = img.get_fdata()

    if data.ndim == 4:
        data = data[:, :, :, 0]

    print(f"Original shape: {data.shape}")
    processed = preprocess_volume(data)
    print(f"Processed shape: {processed.shape}")
    print(f"Processed value range: min={processed.min():.3f}, max={processed.max():.3f}")
