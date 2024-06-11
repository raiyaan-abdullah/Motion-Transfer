ROOT=path_to_root

B2N_ssv2_file=ssv2_custom/ssv2_distribution3_head_classes
TRAIN_FILE=ssv2_train_set2.csv
VAL_FILE=ssv2_val_set2.csv
TEST_FILE=ssv2_val_set2.csv

cd $ROOT

TORCH_DISTRIBUTED_DEBUG=INFO python -W ignore -u tools/run_net.py \
  --cfg configs/Kinetics/TemporalCLIP_vitb16_8x16_STAdapter_SSV2.yaml \
  --opts DATA.PATH_TO_DATA_DIR $ROOT/zs_label_db/$B2N_ssv2_file \
  TRAIN_FILE $TRAIN_FILE \
  VAL_FILE $VAL_FILE \
  TEST_FILE $TEST_FILE \
  DATA.PATH_PREFIX path_to_dataset \
  DATA.PATH_LABEL_SEPARATOR , \
  DATA.INDEX_LABEL_MAPPING_FILE $ROOT/zs_label_db/ssv2_custom/ssv2_distribution3_head_classes/train_test_head_rephrased.json \
  TRAIN.ENABLE True \
  OUTPUT_DIR $ROOT/outputs/ssv2/head_classes/head_classes_ssv2_froster_tr_set2_val_set2_combined \
  TRAIN.BATCH_SIZE 24 \
  TEST.BATCH_SIZE 48 \
  TEST.NUM_ENSEMBLE_VIEWS 1 \
  TEST.NUM_SPATIAL_CROPS 1 \
  NUM_GPUS 1 \
  SOLVER.MAX_EPOCH 40 \
  SOLVER.WARMUP_EPOCHS 5.0 \
  SOLVER.BASE_LR 3.33e-6 \
  SOLVER.WARMUP_START_LR 3.33e-8 \
  SOLVER.COSINE_END_LR 3.33e-8 \
  TRAIN.MIXED_PRECISION True \
  DATA.DECODING_BACKEND "pyav" \
  MODEL.NUM_CLASSES 26 \
  MIXUP.ENABLE False \
  AUG.ENABLE False \
  AUG.NUM_SAMPLE 1 \
  TRAIN.EVAL_PERIOD 5 \
  TRAIN.CHECKPOINT_PERIOD 5 \
  MODEL.LOSS_FUNC soft_cross_entropy \
  TRAIN.LINEAR_CONNECT_CLIMB False \
  TRAIN.CLIP_ORI_PATH /root/.cache/clip/ViT-B-16.pt \
  TRAIN.LINEAR_CONNECT_LOSS_RATIO 0.0 \
  MODEL.RAW_MODEL_DISTILLATION True \
  MODEL.KEEP_RAW_MODEL True \
  MODEL.DISTILLATION_RATIO 2.0