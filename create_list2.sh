#!/bin/bash 

root_dir=$HOME/img/
sub_dir=ImageSets/Main # 刚才新建的文件夹路径，用以读取刚才 classfiy.py 生成的 txt 文件 
bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 
for dataset in trainval test train val # 刚才四个文件夹的名字，其实主要用的就是 test 和 trainval 
do 
    dst_file=$bash_dir/$dataset.txt 
    if [ -f $dst_file ] 
    then 
       rm -f $dst_file 
    fi 
    for name in person_data # pcdata 是我存放 JPEGImage 和 Annotations 的文件夹名称 
    do 
        if [[ $dataset == "test" && $name == "VOC2012" ]] 
        then 
            continue 
        fi 
        echo "Create list for $name $dataset..." 
        dataset_file=$root_dir/$name/$sub_dir/$dataset.txt 

        img_file=$bash_dir/$dataset"_img.txt" 
        cp $dataset_file $img_file 
        sed -i "s/^/$name\/JPEGImages\//g" $img_file 
        sed -i "s/$/.jpg/g" $img_file 

        label_file=$bash_dir/$dataset"_label.txt" 
        cp $dataset_file $label_file 
        sed -i "s/^/$name\/Annotations\//g" $label_file 
        sed -i "s/$/.xml/g" $label_file 
        paste -d' ' $img_file $label_file >> $dst_file 
        rm -f $label_file 
        rm -f $img_file 
    done 

    # Generate image name and size infomation.
    echo "wxx" 
    if [ $dataset == "test" ] 
    then 
        /home/wxx/develop/caffe-ssd/build/tools/get_image_size $root_dir $dst_file $bash_dir/$dataset"_name_size.txt" 
    fi 
    # Shuffle trainval file. 
     echo "wxx2" 
    if [ $dataset == "trainval" ] 
    then 
        rand_file=$dst_file.random 
        cat $dst_file | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > $rand_file 
        mv $rand_file $dst_file 
    fi 
done

