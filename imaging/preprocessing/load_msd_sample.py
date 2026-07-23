"""
Loads one image/label pair from the MSD Hippocampus dataset using
MONAI's dictionary-based transform pipeline.
"""

import json
import os
from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    Orientationd,
    ScaleIntensityd,
)


def load_sample(data_root: str):
    with open(os.path.join(data_root, "dataset.json")) as f:
        dataset_info = json.load(f)

    first_pair = dataset_info["training"][0]
    data_dict = {
        "image": os.path.join(data_root, first_pair["image"].lstrip("./")),
        "label": os.path.join(data_root, first_pair["label"].lstrip("./")),
    }

    transforms = Compose([
        LoadImaged(keys=["image", "label"]),
        EnsureChannelFirstd(keys=["image", "label"]),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        ScaleIntensityd(keys=["image"]),
    ])

    result = transforms(data_dict)

    print(f"Image shape: {result['image'].shape}")
    print(f"Label shape: {result['label'].shape}")
    print(f"Image value range: min={result['image'].min():.3f}, max={result['image'].max():.3f}")
    print(f"Unique label values: {result['label'].unique()}")


if __name__ == "__main__":
    load_sample("data/raw/msd_sample/Task04_Hippocampus")
