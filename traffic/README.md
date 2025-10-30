Started with simple single Convolution layer, No pooling and got the accuracy 93.20% in about 333/333 - 1s - 2ms/step with a loss of 3.96%
Added a Pooling layer and got - 333/333 - 1s - 2ms/step - accuracy: 0.9441 - loss: 0.0328
Added a convolution layer and a pooling layer and got - 333/333 - 1s - 4ms/step - accuracy: 0.9812 - loss: 0.0089
Added a convolution layer and a pooling layer with size 3 X 3 and got - 333/333 - 1s - 4ms/step - accuracy: 0.9808 - loss: 0.0065
Added a hidden layer - 333/333 - 1s - 4ms/step - accuracy: 0.9860 - loss: 0.0035
Added another hidden layer - 333/333 - 2s - 5ms/step - accuracy: 0.9839 - loss: 0.0033
Added dropout - 333/333 - 2s - 5ms/step - accuracy: 0.9865 - loss: 0.0027