# Regression model by Leroy Tee Yang Andy
import math
import tensorflow as tf
import numpy as np
import pylab as plt

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

NUM_FEATURES = 45

learning_rate = 0.001
epochs = 10
batch_size = 64
num_neuron = 20
seed = 10
reg_weight = 0.001
np.random.seed(seed)

# initialization routines for bias and weights
def init_bias(n = 1):
    return(tf.Variable(np.zeros(n), dtype=tf.float32))

def init_weights(n_in=1, n_out=1):
    W_values = tf.random.truncated_normal((n_in, n_out), stddev=1.0/math.sqrt(n_in))
    return(tf.Variable(W_values, dtype=tf.float32))

def unnormalise(data, mean, std):
    return data * std + mean


def ffn(x):
    with tf.name_scope('hidden'):

        # Hidden Layer
        W = init_weights(NUM_FEATURES, num_neuron)
        b = init_bias(num_neuron)
        Z = tf.matmul(x, W) + b
        H = tf.nn.relu(Z)

    with tf.name_scope('linear'):

        # Output Layer
        V = init_weights(num_neuron, 1)
        c = init_bias(1)
        y = tf.matmul(H, V) + c # linear

    return y, V, c, W, b, H, Z

def main():
    #read and divide data into test and train sets 
    admit_data = np.genfromtxt('cleanRegressionData.csv', delimiter= ',')
    X_data, Y_data = admit_data[1:,1:46], admit_data[1:,-1]
    Y_data = Y_data.reshape(Y_data.shape[0], 1)

    idx = np.arange(X_data.shape[0])
    np.random.shuffle(idx)
    X_data, Y_data = X_data[idx], Y_data[idx]

    X_data = X_data[:2000]
    Y_data = Y_data[:2000]

    X_data = (X_data- np.mean(X_data, axis=0))/ np.std(X_data, axis=0)
    mean = np.mean(Y_data)
    std = np.std(Y_data)
    Y_data = (Y_data - mean)/ std

    #split into train and test
    cutoff = math.floor(0.7 * len(X_data))

    trainX = np.copy(X_data[:cutoff])
    trainY = np.copy(Y_data[:cutoff])

    testX = np.copy(X_data[cutoff:])
    testY = np.copy(Y_data[cutoff:])

    # Create the model
    x = tf.placeholder(tf.float32, [None, NUM_FEATURES])
    d = tf.placeholder(tf.float32, [None, 1])

    y, V, c, W, b, H, Z = ffn(x)

    #Create the gradient descent optimizer with the given learning rate.
    mse = tf.reduce_mean(tf.square(d - y))

    regularisation = tf.nn.l2_loss(V) + tf.nn.l2_loss(W)
    loss = mse + reg_weight * regularisation

    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_op = optimizer.minimize(loss)
        
    with tf.Session() as sess:
        tf.set_random_seed(seed+5)
        tf.global_variables_initializer().run()
        train_err = []
        test_err = []
        idx = np.arange(trainX.shape[0])

        # LEARN WEIGHTS
        for i in range(epochs):
            
            # Shuffle at every epoch
            np.random.shuffle(idx)
            trainX, trainY = trainX[idx], trainY[idx]


            for start, end in zip(range(0, len(trainX), batch_size), range(batch_size, len(trainX), batch_size)):
                t, W_, b_, Z_ = sess.run([train_op, W, b, Z], feed_dict={x: trainX[start:end], d: trainY[start:end]})
                if i == 5 and start < 1:
                    print("W", W_)
                    print("b", b_)
                    print("Z", Z_)

            tr_err = sess.run([loss], feed_dict={x: trainX, d: trainY})
            train_err.append(tr_err[0])

            te_err = sess.run([loss], feed_dict={x: testX, d: testY})
            test_err.append(te_err[0])

            if i % 100 == 0:
                print('iter %d: train error %g test error %g'%(i, train_err[i], test_err[i]))

    # plot learning curves
    f1 = plt.figure(1)
    print(train_err)
    print(test_err)
    plt.plot(range(epochs), train_err, label = 'train error')
    plt.plot(range(epochs), test_err, label = 'test error')
    plt.xlabel(str(epochs) + ' iterations')
    plt.ylabel('Mean Square Error')
    plt.title('Training errors against Epochs - RFE')
    #plt.ylim(0,0.015)
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()