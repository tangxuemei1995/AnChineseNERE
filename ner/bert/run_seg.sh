export BERT_BASE_DIR=./model/1.2
export DATA_DIR=./data/seg
export OUTPUT_DIR=./output/seg_1.2
export EXPORT_DIR=./export/seg_1.2

MAX_EPOCH=15

CUDA_VISIBLE_DEVICES=0,1,2,3 python3 run_tagger_cnn.py \
  --task_name=Seg \
  --do_train=true \
  --do_eval=true \
  --do_predict=false \
  --export_model=false \
  --data_dir=$DATA_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/model.ckpt-1000002 \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --eval_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=0.3 \
  --max_train_epochs=$MAX_EPOCH \
  --output_dir=$OUTPUT_DIR \
  --export_dir=$EXPORT_DIR
#exit 0

for e in $(seq 0.6 0.3 $MAX_EPOCH)
do
    ckpt=`head -n 1 ${OUTPUT_DIR}/checkpoint`
    ckpt=${ckpt:24}
    ckpt=${ckpt%\"*}

    CUDA_VISIBLE_DEVICES=0,1,2,3 python3 run_tagger_cnn.py \
        --task_name=Seg \
        --do_train=true \
        --do_eval=true \
        --do_predict=false \
        --export_model=false \
        --data_dir=$DATA_DIR \
        --vocab_file=$BERT_BASE_DIR/vocab.txt \
        --bert_config_file=$BERT_BASE_DIR/bert_config.json \
        --init_checkpoint=$OUTPUT_DIR/$ckpt \
        --max_seq_length=128 \
        --train_batch_size=32 \
        --eval_batch_size=32 \
        --learning_rate=2e-5 \
        --num_train_epochs=${e} \
        --max_train_epochs=$MAX_EPOCH \
        --output_dir=$OUTPUT_DIR \
        --export_dir=$EXPORT_DIR
done