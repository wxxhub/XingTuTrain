#!/bin/sh
if ! test -f example/MobileNetSSD_train.prototxt ;then
	echo "error: example/MobileNetSSD_train.prototxt does not exist."
	echo "please use the gen_model.sh to generate your own model."
        exit 1
fi
mkdir -p snapshot
/home/wxx/develop/caffe-ssd/build/tools/caffe train -solver="solver_train.prototxt" \
-weights="mobilenet_iter.caffemodel" \
-gpu 0
