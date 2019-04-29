batch_size=256

data_root=/mnt/SSD/rongyu/data/3D/
#data_root=/mnt/SSD2/rongyu/data/

human36m_anno_dir=$data_root'human36m/pkl/test/'
coco_anno_dir=$data_root'coco/annotations/crop_anno_val2014_all/' 
up3d_anno_file=$data_root'up_3d_new/infos_refine_IUV_remove_and_add/test.pkl' 

DPW_sample_method='edge_plus_uniform'


if [ -d test_result ]; then
    rm -rf test_result
fi
mkdir test_result

if [ -d demo_log ]; then
    rm -rf demo_log
fi
mkdir demo_log


start_gpu=0

for i in $(seq 0 1 1)
do
    for j in $(seq 0 1 1)
    do
        process_id=$(expr $i \* 2 + $j)
        gpu_id=$(expr $i + $start_gpu)
        dpw_anno_file=$data_root'3DPW/infos_demo_full/'$process_id'.pkl'

        CUDA_VISIBLE_DEVICES=$gpu_id python2 demo.py  --gpu_ids=0 \
            --single_branch --main_encoder resnet50  --aux_as_main \
            --name dp2smpl  --model dp2smpl \
            --coco_anno_dir $coco_anno_dir \
            --human36m_anno_dir $human36m_anno_dir \
            --up3d_anno_file $up3d_anno_file \
            --dpw_anno_dir $dpw_anno_file \
            --batchSize $batch_size --phase test \
            --dp_max_anno 400 --refine_IUV --five_weight \
            --result_id $process_id \
            --test_dataset  dpw | tee 'demo_log/'$process_id'.txt' &
    done
done
