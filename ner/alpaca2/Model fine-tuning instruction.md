If you want to use lore fine-tune alpaca2:

cd  ./scripts/training/
#train model ：
bash run_sft_chapter.sh
#merge models：
bash merge_new_model.sh
#model testing:
bash  run_test.sh
#results evaluation:
python evaluate.py