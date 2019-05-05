from abc import ABC, abstractmethod
import numpy as np

import functional

class NN:

    def __init__(self, layers=[], loss_function, lr):
        self.layers = layers
        self.loss_function = loss_function
        self.lr = lr

    def fit(self, x_train, y_train, epochs=5):
        for _ in range(epochs):

            for x, y in zip(x_train, y_train):
                self.feed(x)

                error = np.sum(self.loss_function(self.layers[-1].a, y))
                self.backprop(y)

            print('Epoch: {}. Error: {}'.format(_ + 1, error))

    def feed(self, x):
        for L in self.layers:
            x = L.feed(x)

    def backprop(self, y):

        prev_delta = None

        for l in reversed(range(len(self.layers))):

            # If it's the final layer
            if l + 1 == len(self.layers):
                a_grad = self.loss_function(self.layers[l].a, y, deriv=True)
                delta = a_grad * self.layers[l].activation(self.layers[l].z, deriv=True)
            else:
                p1 = np.dot(self.layers[l + 1].W.T, prev_delta)
                p2 = self.layers[l].activation(self.layers[l].z, deriv=True)
                delta = p1 * p2
            prev_delta = delta

            # If it's the first hidden layer
            if l == 0:
                self.layers[l].W_grad = np.dot(delta, self.layers[l].x.T)
            else:
                self.layers[l].W_grad = np.dot(delta, self.layers[l - 1].a.T)
            self.layers[l].b_grad = delta

        # Apply computed gradients to weights and biases
        for l in range(len(self.layers)):
            self.layers[l].W -= (self.layers[l].W_grad * self.lr)
            self.layers[l].b -= (self.layers[l].b_grad * self.lr)

    def test(self, x_test, y_test):
        total = 0
        success = 0
        for x, y in zip(x_test, y_test):
            total += 1
            self.feed(x)

            success += (np.argmax(self.layers[-1].a) == np.argmax(y))

        print('Accuracy: {}'.format(success/total))