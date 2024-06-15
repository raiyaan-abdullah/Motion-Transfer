ANALYSIS_ROOT=/workspace/work_dirs/e33252/analysis/kinetics400
DATA_ROOT=/workspace/work_dirs/e33252/data/kinetics/k400/
ROOT=$ANALYSIS_ROOT/FROSTER
CKPT=$ROOT

DATA_PATH=$DATA_ROOT

# B2N_k400_file=B2N_k400_set$SET
TRAIN_FILE=train_set${1}_head_v2.csv
VAL_FILE=val_set${2}_head_v2.csv
TEST_FILE=test_set${2}_head_v2.csv


cd $ROOT

TORCH_DISTRIBUTED_DEBUG=INFO python -W ignore -u tools/run_net.py \
    --cfg configs/Kinetics/TemporalCLIP_vitb16_8x16_STAdapter_K400.yaml \
    --opts DATA.PATH_TO_DATA_DIR $DATA_PATH \
    TRAIN_FILE $TRAIN_FILE \
    VAL_FILE $VAL_FILE \
    TEST_FILE $TEST_FILE \
    DATA.PATH_PREFIX "" \
    DATA.PATH_LABEL_SEPARATOR " " \
    DATA.INDEX_LABEL_MAPPING_FILE $DATA_PATH/head_classes_rephrased_v2.json \
    TRAIN.ENABLE True \
    OUTPUT_DIR $CKPT/basetraining/v2/B2N_k400_froster_tr_set${1}_val_set${2} \
    TRAIN.BATCH_SIZE 16 \
    TEST.BATCH_SIZE 240 \
    TEST.ENABLE False \
    TEST.NUM_ENSEMBLE_VIEWS 3 \
    TEST.NUM_SPATIAL_CROPS 1 \
    NUM_GPUS 2 \
    SOLVER.MAX_EPOCH 12 \
    SOLVER.WARMUP_EPOCHS 2.0 \
    SOLVER.BASE_LR 3.33e-6 \
    SOLVER.WARMUP_START_LR 3.33e-8 \
    SOLVER.COSINE_END_LR 3.33e-8 \
    TRAIN.MIXED_PRECISION True \
    DATA.DECODING_BACKEND "pyav" \
    MODEL.NUM_CLASSES 41 \
    MIXUP.ENABLE False \
    AUG.ENABLE False \
    AUG.NUM_SAMPLE 1 \
    TRAIN.EVAL_PERIOD 1 \
    TRAIN.CHECKPOINT_PERIOD 1 \
    MODEL.LOSS_FUNC soft_cross_entropy \
    TRAIN.LINEAR_CONNECT_CLIMB False \
    TRAIN.CLIP_ORI_PATH /root/.cache/clip/ViT-B-16.pt \
    TRAIN.LINEAR_CONNECT_LOSS_RATIO 0.0 \
    MODEL.RAW_MODEL_DISTILLATION True \
    MODEL.KEEP_RAW_MODEL True \
    MODEL.DISTILLATION_RATIO 2.0