# Punching Bag vs. Punching Person: Motion Transferability in Videos [ICCV 25]
[![Website](https://img.shields.io/badge/Project-Website-87CEEB)](http://raiyaan-abdullah.github.io/Motion-Transfer-webpage/)
[![Paper coming soon.](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)]()

🎉 (June 25, 2025) Paper got accepted at ICCV 2025

## Benchmark datasets
The detailed videos list and class labels for `Syn-TA`, `Kinectics400 - TA`, and `Something-something-v2 - TA` are provided in `dataset_splits` and `labels`. For `K400-TA` and `SSv2-TA`, please download the subset of videos according to the videos list from their original providers: [Kinetics400](https://github.com/cvdfoundation/kinetics-dataset) and [Something-something-v2](https://www.qualcomm.com/developer/software/something-something-v-2-dataset).

## Syn-TA
The Syn-TA dataset videos are available on Hugging Face: [https://huggingface.co/datasets/raiyaanabdullah/Syn-TA](https://huggingface.co/datasets/raiyaanabdullah/Syn-TA).
If you wish to generate them in Blender, please follow the instructions in [GENERATE_SYNTA.md](https://github.com/raiyaan-abdullah/TrAc-Bench/blob/main/synta_generate_blender/GENERATE_SYNTA.md).

## Training
The training configurations for all the models are available at `configs`. Please see [INSTRUCTIONS.md](https://github.com/raiyaan-abdullah/TrAc-Bench/blob/main/configs/INSTRUCTIONS.md) for more details.

## Absolute drop and harmonic mean of known (CoarseMotion-KC) and unknown (CoarseMotion-UC) accuracies (average of two sets) for *coarse activities*
| **Model**         | **Syn-TA**                     |                  |                  |                  | **K400-TA**                    |                  |                  |                  | **SSv2-TA**                    |                  |                  |                  |
|-------------------|:------------------------------:|:-----------------|:-----------------|:-----------------|:------------------------------:|:-----------------|:-----------------|:-----------------|:------------------------------:|:-----------------|:-----------------|:-----------------|
|                   | **Known ↑** | **Unknown ↑** | **D_abs ↓** | **HM ↑** | **Known ↑** | **Unknown ↑** | **D_abs ↓** | **HM ↑** | **Known ↑** | **Unknown ↑** | **D_abs ↓** | **HM ↑** |
| **Unimodal Models** |                              |                  |                  |                  |                              |                  |                  |                  |                              |                  |                  |                  |
| ResNet50          | 66.66         | 29.93         | 36.73         | 41.30         | 76.49         | 46.21         | 30.28         | 57.59         | 45.07         | 26.08         | 18.99         | 33.01         |
| I3D               | 80.50         | 37.51         | 42.99         | 51.17         | 76.89         | 47.25         | 29.63         | 58.49         | 59.60         | 34.40         | 25.20         | 43.53         |
| X3D               | 93.71         | 58.45         | 35.25         | 71.79         | 81.23         | 49.88         | 31.35         | 61.78         | 72.73         | 41.81         | 30.92         | 53.05         |
| SlowFast          | 89.27         | 46.86         | 42.41         | 61.45         | 81.70         | 50.33         | 31.37         | 62.26         | 57.67         | 35.15         | 22.51         | 43.60         |
| MViTv2            | 63.69         | 43.23         | **20.46***    | 51.50         | 68.88         | 45.06         | 23.81         | 54.47         | 54.31         | 32.37         | 21.93         | 40.49         |
| Rev-MViT          | 65.53         | 38.02         | 27.51         | 47.98         | 59.40         | 40.54         | **18.86***    | 48.16         | 34.64         | 21.72         | **12.92***    | 26.68         |
| AIM               | **99.13***    | **70.16***    | 28.97         | **82.17***    | 95.04         | 63.73         | 31.31         | 76.29         | **79.94***    | **45.82***    | 34.12         | **58.18***    |
| UniformerV2       | 97.96         | 51.20         | 46.76         | 67.25         | 93.56         | 62.29         | 31.27         | 74.77         | 58.16         | 33.20         | 24.96         | 42.25         |
| **Multimodal Models** |                          |                  |                  |                  |                              |                  |                  |                  |                              |                  |                  |                  |
| ActionCLIP        | 96.29         | 55.33         | 40.95         | 70.27         | 93.24         | 62.24         | 31.00         | 74.60         | 64.10         | 36.66         | 27.44         | 46.56         |
| X-CLIP            | 85.04         | 47.83         | 37.21         | 61.22         | 92.69         | 61.47         | 31.22         | 73.90         | 69.49         | 40.10         | 29.39         | 50.74         |
| ViFi-CLIP         | 79.67         | 35.46         | 44.21         | 49.01         | 93.24         | 60.44         | 32.80         | 73.31         | 58.69         | 30.69         | 27.99         | 40.22         |
| EZ-CLIP           | 98.30         | 52.43         | 45.87         | 68.38         | 86.88         | 66.70         | 20.18         | 75.43         | 62.55         | 34.84         | 27.70         | 44.72         |
| FROSTER           | 89.42         | 31.80         | 57.61         | 46.91         | **95.99***    | **69.23***    | 26.76         | **80.42***    | 57.65         | 30.68         | 26.97         | 39.98         |
| **Domain Generalization Methods** |               |                  |                  |                  |                              |                  |                  |                  |                              |                  |                  |                  |
| VideoDG           | 98.07         | 43.43         | 54.64         | 60.17         | 86.11         | 53.95         | 32.15         | 66.27         | 57.25         | 31.54         | 25.71         | 40.63         |
| STDN              | 70.66         | 23.97         | 46.69         | 35.72         | 68.11         | 46.10         | 22.01         | 54.89         | 35.93         | 22.31         | 13.62         | 27.51         |
| CIR               | 60.13         | 9.59          | 50.54         | 16.41         | 68.53         | 12.66         | 55.87         | 21.34         | 48.01         | 31.97         | 16.04         | 38.37         |

## Absolute drop and harmonic mean of known (CoarseMotion-KC) and unknown (CoarseMotion-UC) accuracies (average of two sets) for *fine activities*
| **Model**         | **Syn-TA**                     |                  |                  |                  | **K400-TA**                    |                  |                  |                  | **SSv2-TA**                    |                  |                  |                  |
|-------------------|:------------------------------:|:-----------------|:-----------------|:-----------------|:------------------------------:|:-----------------|:-----------------|:-----------------|:------------------------------:|:-----------------|:-----------------|:-----------------|
|                   | **Known ↑** | **Unknown ↑** | **D_abs ↓** | **HM ↑** | **Known ↑** | **Unknown ↑** | **D_abs ↓** | **HM ↑** | **Known ↑** | **Unknown ↑** | **D_abs ↓** | **HM ↑** |
| ActionCLIP        | 88.01         | **38.81***    | **49.19***    | **53.85***    | 87.75         | 41.52         | 46.23         | 56.20         | 59.72         | 25.84         | 33.88         | 36.03         |
| X-CLIP            | 75.20         | 22.90         | 52.29         | 34.98         | **89.06***    | 48.11         | 40.95         | 62.37         | **65.31***    | 26.53         | 38.78         | 37.69         |
| ViFi-CLIP         | 69.27         | 19.91         | 49.36         | 30.79         | 88.91         | 26.70         | 62.21         | 40.97         | 52.13         | 26.28         | 25.85         | 34.93         |
| EZ-CLIP           | **89.54***    | 24.89         | 64.64         | 38.71         | 83.76         | 73.95         | **9.81***     | 78.47         | 59.83         | **29.73***    | 30.09         | **39.70***    |
| FROSTER           | 85.44         | 20.68         | 64.76         | 33.26         | 88.93         | **74.11***    | 14.82         | **80.81***    | 50.34         | 24.99         | **25.35***    | 33.34         |
