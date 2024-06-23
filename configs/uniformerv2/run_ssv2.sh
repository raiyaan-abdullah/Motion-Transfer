work_path=path_to_output_dir
NUM_SHARDS=1
NUM_GPUS=2 #8
NUM_WORKERS=4
BATCH_SIZE=32 #128
BASE_LR=4e-5
PYTHONPATH=$PYTHONPATH:./slowfast \
python tools/run_net_multi_node.py \
  --init_method tcp://localhost:10125 \
  --cfg exp/ssv2/config_ssv2.yaml \
  --num_shards $NUM_SHARDS \
  DATA.PATH_TO_DATA_DIR ./data_list/path_to_train_val_video_list \
  DATA.PATH_PREFIX path_to_root_directory \
  DATA.LABEL_PATH_TEMPLATE "somesomev2_rgb_{}_split.txt" \
  DATA.IMAGE_TEMPLATE "{:06d}.jpg" \
  TRAIN.EVAL_PERIOD 2 \
  TRAIN.CHECKPOINT_PERIOD 5 \
  TRAIN.BATCH_SIZE $BATCH_SIZE \
  TRAIN.SAVE_LATEST False \
  DATA_LOADER.NUM_WORKERS $NUM_WORKERS \
  NUM_GPUS $NUM_GPUS \
  NUM_SHARDS $NUM_SHARDS \
  SOLVER.MAX_EPOCH 50 \
  SOLVER.BASE_LR $BASE_LR \
  SOLVER.BASE_LR_SCALE_NUM_SHARDS False \
  SOLVER.WARMUP_EPOCHS 5. \
  DATA.TEST_CROP_SIZE 224 \
  TEST.NUM_ENSEMBLE_VIEWS 1 \
  TEST.NUM_SPATIAL_CROPS 3 \
  TEST.TEST_BEST True \
  DATA.MC True \
  RNG_SEED 6666 \
  OUTPUT_DIR $work_path

