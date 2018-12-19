EXAMPLE=examples/my_simple_image
DATA=examples/my_simple_image
TOOLS=build/tools

$TOOLS/compute_image_mean $EXAMPLE/ilsvrc12_train_lmdb $DATA/imagenet_mean.binaryproto

echo "Done."
