# Regression model by Leroy Tee Yang Andy
import math
import tensorflow as tf
import numpy as np
import pylab as plt
from tqdm import tqdm

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

NUM_FEATURES = 45

learning_rate = 0.001
epochs = 1000
batch_size = 128
num_neuron = 20
seed = 10
reg_weight = 0.001
num_sample_data = 100
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
        H = tf.nn.sigmoid(Z)

    with tf.name_scope('linear'):

        # Output Layer
        V = init_weights(num_neuron, 1)
        c = init_bias(1)
        y = tf.matmul(H, V) + c # linear

    return y, V, W, c, b

def main():
    #read and divide data into test and train sets 
    admit_data = np.genfromtxt('cleanRegressionData.csv', delimiter= ',')
    X_data, Y_data = admit_data[1:,1:46], admit_data[1:,-1]
    Y_data = Y_data.reshape(Y_data.shape[0], 1)

    idx = np.arange(X_data.shape[0])
    np.random.shuffle(idx)
    X_data, Y_data = X_data[idx], Y_data[idx]

    #X_data = X_data[:2000]
    #Y_data = Y_data[:2000]

    # Only normalise columns 1:3 and 43:end
    X_data[:,1:3] = (X_data[:,1:3]- np.mean(X_data[:,1:3], axis=0))/ np.std(X_data[:,1:3], axis=0)
    X_data[:,43:] = (X_data[:,43:]- np.mean(X_data[:,43:], axis=0))/ np.std(X_data[:,43:], axis=0)
    #X_data = (X_data- np.mean(X_data, axis=0))/ np.std(X_data, axis=0)
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

    y, V, W, c, b = ffn(x)

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

        lowestLoss = None

        # LEARN WEIGHTS
        for i in tqdm(range(epochs)):
            
            # Shuffle at every epoch
            np.random.shuffle(idx)
            trainX, trainY = trainX[idx], trainY[idx]


            for start, end in zip(range(0, len(trainX), batch_size), range(batch_size, len(trainX), batch_size)):
                sess.run([train_op], feed_dict={x: trainX[start:end], d: trainY[start:end]})

            tr_err = sess.run([loss], feed_dict={x: trainX, d: trainY})
            train_err.append(tr_err[0])

            te_err = sess.run([loss], feed_dict={x: testX, d: testY})
            test_err.append(te_err[0])

            if lowestLoss == None or te_err < lowestLoss:
                lowestLoss = te_err
                V_, c_, W_, b_ = sess.run([V, c, W, b]) #store weights at best epoch
                bestEpoch = i

            #if i % 10 == 0:
            #    print('iter %d: train error %g test error %g'%(i, train_err[i], test_err[i]))
        
        print("Best current epoch = ", bestEpoch)
        # load weights from selected epoch
        V.load(V_, sess)
        W.load(W_, sess)
        b.load(b_, sess)
        c.load(c_, sess)

        # Shuffle test samples and sample 100 of them
        idxtest = np.arange(testX.shape[0])
        np.random.shuffle(idxtest)
        testX, testY = testX[idxtest], testY[idxtest]
        sub_testX = testX[:num_sample_data]
        sub_testY = testY[:num_sample_data]

        # Sort the samples for visual aesthetic sake
        idxsort = np.argsort([i[0] for i in sub_testY])
        sub_testX, sub_testY = sub_testX[idxsort], sub_testY[idxsort]
        y_ = sess.run([y], feed_dict={x: sub_testX})
        sub_testY = unnormalise(sub_testY, mean, std)
        y_ = unnormalise(np.array(y_), mean, std)

    # plot learning curves
    f1 = plt.figure(1)
    #print(train_err)
    #print(test_err)
    plt.plot(range(epochs), train_err, label = 'train error')
    plt.plot(range(epochs), test_err, label = 'test error')
    plt.xlabel(str(epochs) + ' iterations')
    plt.ylabel('Mean Square Error')
    plt.title('Mean square errors against Epochs')
    plt.ylim(0,0.8)
    plt.legend()

    f2 = plt.figure(2)

    y1 = [i[0] for i in y_[0]]
    d1 = [i[0] for i in sub_testY]

    #print(y1)
    #print(d1)

    plt.scatter(range(num_sample_data), y1, label = "Predicted Values")
    plt.scatter(range(num_sample_data), d1, label = "Actual values")
    plt.title('Scatterplot of Predicted vs Target values')
    plt.xlabel('50 random data samples, sorted')
    plt.ylabel('Housing Prices')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()