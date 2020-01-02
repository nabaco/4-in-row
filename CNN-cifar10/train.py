import os
from matplotlib import pyplot
from keras.datasets import cifar10
from keras.utils import to_categorical
from keras.models import Model, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, BatchNormalization
from keras.layers import Input, Flatten, Dense
from keras.optimizers import SGD
from keras.regularizers import l2


def load_dataset():
    """
    Load cifar-10 dataset.
    Return:
        trainX, trainY, testX, testY (tuple): Dataset.
    """
    (trainX, trainY), (testX, testY) = cifar10.load_data()
    trainY = to_categorical(trainY)
    testY = to_categorical(testY)
    return trainX, trainY, testX, testY


def dataset_norm(train, test):
    """
    Dataset normalization.
    Arguments:
        train (ndarray): Train data.
        test (ndarray): Test data.
    Return:
        train_norm, test_norm (tuple): Normelized images.
    """
    train_norm = train.astype('float32')
    test_norm = test.astype('float32')
    train_norm = train_norm / 255
    test_norm = test_norm / 255
    return train_norm, test_norm


def define_model():
    """
    Define CNN model based on VGG16 architecture:
    * 3 VGG blocks:
        Conv2D -> BachNormalization ->
        Conv2D -> BachNormalization ->
        MaxPooling -> Dropuot.
    * Flatten.
    * Dense 128 -> Dense 10.

    Return:
        model (model): Model.
    """
    # Input
    img = Input(shape=(32, 32, 3))

    # VGG Block A
    conv_A1 = Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform',
                     padding='same', kernel_regularizer=l2(0.001))(img)
    BN_A1 = BatchNormalization()(conv_A1)
    conv_A2 = Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform',
                     padding='same', kernel_regularizer=l2(0.001))(BN_A1)
    BN_A2 = BatchNormalization()(conv_A2)
    pooling_A = MaxPooling2D((2, 2))(BN_A2)
    dropout_A = Dropout(0.2)(pooling_A)

    # VGG Block B
    conv_B1 = Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform',
                     padding='same', kernel_regularizer=l2(0.001))(dropout_A)
    BN_B1 = BatchNormalization()(conv_B1)
    conv_B2 = Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform',
                     padding='same', kernel_regularizer=l2(0.001))(BN_B1)
    BN_B2 = BatchNormalization()(conv_B2)
    pooling_B = MaxPooling2D((2, 2))(BN_B2)
    dropout_B = Dropout(0.3)(pooling_B)

    # VGG Block C
    conv_C1 = Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform',
                     padding='same', kernel_regularizer=l2(0.001))(dropout_B)
    BN_C1 = BatchNormalization()(conv_C1)
    conv_C2 = Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform',
                     padding='same', kernel_regularizer=l2(0.001))(BN_C1)
    BN_C2 = BatchNormalization()(conv_C2)
    pooling_C = MaxPooling2D((2, 2))(BN_C2)
    dropout_C = Dropout(0.4)(pooling_C)

    # Flatten
    flatten = Flatten()(dropout_C)

    # Full-connection
    dense128 = Dense(128, activation='relu', kernel_initializer='he_uniform',
                     kernel_regularizer=l2(0.001))(flatten)
    BN128 = BatchNormalization()(dense128)
    dropout128 = Dropout(0.5)(BN128)
    prediction = Dense(10, activation='softmax')(dropout128)

    # Model and optimizer Definition
    model = Model(inputs=img, outputs=prediction)
    opt = SGD(lr=0.001, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def model_diagnostics(history):
    """
    Create plots of Cross Entropy Loss and Classification Accuracy.
    Arguments:
        history (History): Hystory of data fiting.
    """
    # Plot loss
    pyplot.subplot(211)
    pyplot.title('Cross Entropy Loss')
    pyplot.plot(history.history['loss'], color='blue', label='train')
    pyplot.plot(history.history['val_loss'], color='orange', label='test')

    # Plot accuracy
    pyplot.subplot(212)
    pyplot.title('Classification Accuracy')
    pyplot.plot(history.history['acc'], color='blue', label='train')
    pyplot.plot(history.history['val_acc'], color='orange', label='test')

    # Save plot to file
    pyplot.savefig('history_plot.png')
    pyplot.close()


def train(filename):
    """
    Train the model and save it in *.h5 file.
    Arguments:
        filename (str): File name to load from and save to the trained model.
    """
    # Load and normelize dataset
    trainX, trainY, testX, testY = load_dataset()
    trainX, testX = dataset_norm(trainX, testX)

    # Define model
    model = load_model(filename) if os.path.isfile(
        filename) else define_model()
    model.summary()

    # Model fitting, Saving and model diagnostics
    history = model.fit(trainX, trainY, epochs=100, batch_size=64,
                        validation_data=(testX, testY), verbose=1)
    model.save(filename)
    model_diagnostics(history)
