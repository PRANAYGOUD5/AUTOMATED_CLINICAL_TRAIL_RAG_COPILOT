"""
Builds a MONAI U-Net and runs a single forward pass (inference) on
one sample volume. Weights are randomly initialized (not trained yet) -
this module confirms the full data -> model -> prediction pipeline works.
"""

import json
import os
import torch
from monai.networks.nets import UNet
from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    Orientationd,
    ScaleIntensityd,
    Resized,
)


def build_unet() -> UNet:
    """
    Constructs a 3D U-Net.
    in_channels=1: single-channel (grayscale) MRI/CT input
    out_channels=3: 3 classes for this dataset (background, anterior, posterior)
    channels: number of feature channels at each encoder/decoder level -
              this list length determines how many "levels deep" the U is
    strides: downsampling factor between each level (2 = halve spatial size)
    """
    model = UNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=3,
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
        num_res_units=2,
    )
    return model


def load_and_preprocess_sample(data_root: str) -> torch.Tensor:
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
        # Resize to a fixed shape divisible by 8 (2^3, since we have 3
        # downsampling steps) - U-Net requires this or the skip
        # connections won't line up in size during upsampling.
        Resized(keys=["image", "label"], spatial_size=(64, 64, 64), mode=("trilinear", "nearest")),
    ])

    result = transforms(data_dict)
    return result["image"]


if __name__ == "__main__":
    model = build_unet()
    model.eval()  # inference mode - disables dropout/batchnorm training behavior

    image = load_and_preprocess_sample("data/raw/msd_sample/Task04_Hippocampus")

    # Add a batch dimension: model expects [batch, channel, H, W, D]
    input_tensor = image.unsqueeze(0)
    print(f"Input tensor shape: {input_tensor.shape}")

    with torch.no_grad():  # no gradient tracking needed for inference - saves memory
        output = model(input_tensor)

    print(f"Raw model output shape: {output.shape}")

    # Output has 3 channels (one score per class) at every voxel.
    # argmax picks the class with the highest score at each voxel,
    # collapsing 3 channels into a single predicted class map.
    predicted_mask = torch.argmax(output, dim=1)
    print(f"Predicted mask shape: {predicted_mask.shape}")
    print(f"Unique predicted classes: {torch.unique(predicted_mask)}")
