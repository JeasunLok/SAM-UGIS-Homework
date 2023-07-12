import torch
from samgeo import SamGeo

def sam_segmentation(image_path, segmentation_path, str_device):
    checkpoint = r'asset\sam_vit_b_01ec64.pth'

    if str_device == "GPU":
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = 'cpu'
    
    sam = SamGeo(
        checkpoint=checkpoint,
        model_type='vit_b',
        device=device,
        sam_kwargs=None,
    )

    sam.generate(image_path, segmentation_path)
