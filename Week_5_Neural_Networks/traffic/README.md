# Initial tests (Just 10 categories at a time)
## Attempt 1
I started with a single hidden layer with the same neurons as the number of categories. Just to provide a starting point. Also I've added a 0.5 Dropout rate to fight overfitting.

This gave me an accuracy of around 0.1534 @ Epoch 10 and 0.149 at the evaluation.

## Attempt 2
For this attempt I increased the Neurons in the hidden layer to 1024 (randomly selected)

The results are slightly better, but still at around .15 in both training and evaluation. So the problem here is not the amount of neurons (at least yet).

## Attempt 3
For this attempt I reduced the neurons in the hidden layer to 256 and added a layer with a Convolution in 2D with a matrix (3, 3) and 32 filters. After this, I have added a Pooling layer with pool size (2, 2).

Here I got a 10 percent increase in accuracy in both testing and evaluation sets. So, Adding these two layers did improve the detection.

## Attempt 4
Just to see what the bottleneck in accuracy is, I increased back the number of neurons to 1024.

This change affected quite signficantly the performance of the neural network, increasing the training time by a factor of 3, but even though the training had a final accuracy of 70%, the evaluation had barely changed at all.

## Attempt 5
I turned down the ammount of neurons back to 256, and then added another convolution and Pooling layer after the last Pooling, with the same configuration as before.

This changed nothing in accuracy, but did improve performance, cutting in half training time.

# The Bug
After all of this work, I realize I had a bug in my code! Apparently I was using np.resize instead of cv2.resize, which basically cut in half the image, which is not good.
After changing that, accuracy skyrocketed to 87%! without changing anything in the neural network

# Final Attempt
So, after knowing what the problem was, I changed the training to all 43 categories and got 94% accuracy in the evaluation test.

My final neural network described by tensorflow model.summary:
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (Conv2D)             (None, 28, 28, 32)        896

 max_pooling2d (MaxPooling2  (None, 14, 14, 32)        0
 D)

 conv2d_1 (Conv2D)           (None, 12, 12, 32)        9248

 max_pooling2d_1 (MaxPoolin  (None, 6, 6, 32)          0
 g2D)

 flatten (Flatten)           (None, 1152)              0

 dense (Dense)               (None, 256)               295168

 dropout (Dropout)           (None, 256)               0

 dense_1 (Dense)             (None, 43)                11051

=================================================================
Total params: 316363 (1.21 MB)
Trainable params: 316363 (1.21 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________