# notice this script should be run under DeepSpeedExamples/applications/DeepSpeed-Chat/training/step1_supervised_finetuning
# start running script: nohup bash training_scripts/llama2/run_llama2_7b.sh > /data-ai/checkpoints/shaojun/nohup.log  2>&1 &
# using env: gpu
OUTPUT=$1
ZERO_STAGE=$2
if [ "$OUTPUT" == "" ]; then
    OUTPUT=/data-ai/checkpoints/shaojun
fi
if [ "$ZERO_STAGE" == "" ]; then
    ZERO_STAGE=3
fi
mkdir -p $OUTPUT

# Set CUDA_VISIBLE_DEVICES to restrict GPU usage
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7


deepspeed --include localhost:1,2,3 --master_port 29601 main.py \
   --data_split 2,4,4 \
   --dtype "bf16" \
   --model_name_or_path /data-ai/model/llama2/llama2_hf/Llama-2-7b-hf \
   --per_device_train_batch_size 4 \
   --per_device_eval_batch_size 4 \
   --max_seq_len 512 \
   --learning_rate 9.65e-6 \
   --weight_decay 0. \
   --num_train_epochs 100000  \
   --gradient_accumulation_steps 1 \
   --lr_scheduler_type cosine \
   --num_warmup_steps 0 \
   --seed 1234 \
   --gradient_checkpointing \
   --zero_stage $ZERO_STAGE \
   --deepspeed \
   --output_dir $OUTPUT \
   &> $OUTPUT/training.log
