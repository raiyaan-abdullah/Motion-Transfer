Please follow the instructions below for each model. For number of classes, refer to this table:
## Number of classes

| Dataset    | Head | Fine-Context Set 1 | Fine-Context Set 2 |
|------------|--------------|--------------------|--------------------|
| SSv2-TA    | 26           | 81                 | 68                 |
| Kinetics400-TA | 41        | 111                | 94                 |
| SynTA      | 20           | 53                 | 47                 |

## Models
1. **ActionCLIP**
   - Follow the setup instructions in [mmaction2](https://github.com/open-mmlab/mmaction2). Place our configuration files in `projects/actionclip/configs`. You may also create a folder for each custom dataset in `tools/data` and follow existing file organization.
2. **AIM (Adapt Image Models)**
   - Follow the setup instructions in [adapt-image-models](https://github.com/taoyang1122/adapt-image-models). Place our configuration files in `configs/recognition/vit`. You may also create a folder for each custom dataset in `tools/data` and follow existing file organization. This project is also based on `mmaction2`.
3. **EZ-CLIP**
   - Follow the setup instructions in [EZ-CLIP](https://github.com/Shahzadnit/EZ-CLIP). Place our configuration files in `configs`. You may also create a folder for each custom dataset in `dataset_splits` and follow existing file organization. We provided the additional GPT description labels in `ezclip/GPT_discription`.
4. **Froster**
   - Follow the setup instructions in [FROSTER](https://github.com/Visual-AI/FROSTER). Place our configuration files in `script/training`. You may also create a folder for each custom dataset in `zs_label_db` and follow existing file organization.
5. **I3D**
   - Follow the setup instructions in [SlowFast](https://github.com/facebookresearch/SlowFast). Place our configuration files in `configs`. You may also create a folder for each custom dataset in `datasets` and follow existing file organization.
6. **MViTv2**
   - Similar to **I3D** using [SlowFast](https://github.com/facebookresearch/SlowFast).
7. **ResNet50**
   - Similar to **I3D** using [SlowFast](https://github.com/facebookresearch/SlowFast).
8. **Rev-MViT**
   - Similar to **I3D** using [SlowFast](https://github.com/facebookresearch/SlowFast).
9. **SlowFast**
   - Similar to **I3D** using [SlowFast](https://github.com/facebookresearch/SlowFast).
10. **UniFormerV2**
    - Follow the setup instructions in [UniFormerV2](https://github.com/OpenGVLab/UniFormerV2). Place our configuration files in `exp`. You may also create a folder for each custom dataset in `data_list` and follow existing file organization.
11. **VIFI-CLIP**
    - Follow the setup instructions in [ViFi-CLIP](https://github.com/muzairkhattak/ViFi-CLIP). Place our configuration files in `configs`. You may also create a folder for each custom dataset in `datasets_splits` and follow existing file organization.
12. **X3D**
    - Similar to **I3D** using [SlowFast](https://github.com/facebookresearch/SlowFast).
13. **XCLIP**
    - Follow the setup instructions in [X-CLIP](https://github.com/microsoft/VideoX/tree/master/X-CLIP). Place our configuration files in `configs`.
