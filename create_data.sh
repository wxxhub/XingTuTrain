cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
root_dir="$HOME/develop/caffe-ssd"

cd $root_dir

redo=1
data_root_dir="$HOME/img/"
dataset_name="person_data"
mapfile="$HOME/develop/demo3/labelmap_voc.prototxt"
anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0

extra_cmd="--encode-type=jpg --encoded"
if [ $redo ]
then
  extra_cmd="$extra_cmd --redo"
fi
for subset in test trainval
do
  python3 $root_dir/scripts/create_annoset.py --anno-type=$anno_type --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim --resize-width=$width --resize-height=$height --check-label $extra_cmd $data_root_dir $HOME/develop/demo3/$subset.txt $HOME/develop/demo3/$db/$dataset_name"_"$subset"_"$db examples/$dataset_name
done
