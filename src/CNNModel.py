
def main():
    import numpy as np
    import random
    import tensorflow as tf
    from keras.models import Sequential
    from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
    from keras import optimizers
    from keras.preprocessing.image import ImageDataGenerator
    import matplotlib.pyplot as plt

    basepath = "C:/Users/Trupti/Downloads/Thyroid50%/Thyroid100%"

    # ---------------------------
    # ⚙️ GA PARAMETERS
    # ---------------------------
    POP_SIZE = 5          # number of candidate solutions
    GENERATIONS = 3       # number of evolution cycles
    EPOCHS_PER_MODEL = 10 # small epochs for GA evaluation
    MUTATION_RATE = 0.3

    # ---------------------------
    # 📈 Data Generators
    # ---------------------------
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    training_set = train_datagen.flow_from_directory(
        basepath + '/training_set',
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical')

    test_set = test_datagen.flow_from_directory(
        basepath + '/test_set',
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical')

    steps_per_epoch = int(np.ceil(training_set.samples / 32))
    val_steps = int(np.ceil(test_set.samples / 32))

    # ---------------------------
    # 🧬 GA — Chromosome Structure
    # ---------------------------
    def create_chromosome():
        """Random hyperparameter set"""
        return {
            "lr": random.choice([0.01, 0.005, 0.001]),
            "filters": random.choice([32, 64]),
            "dropout": random.choice([0.3, 0.5]),
            "dense_units": random.choice([128, 256]),
            "optimizer": random.choice(["SGD", "Adam"])
        }

    def mutate(chromo):
        """Random mutation"""
        if random.random() < MUTATION_RATE:
            chromo["lr"] = random.choice([0.01, 0.005, 0.001])
        if random.random() < MUTATION_RATE:
            chromo["filters"] = random.choice([32, 64])
        if random.random() < MUTATION_RATE:
            chromo["dropout"] = random.choice([0.3, 0.5])
        if random.random() < MUTATION_RATE:
            chromo["dense_units"] = random.choice([128, 256])
        if random.random() < MUTATION_RATE:
            chromo["optimizer"] = random.choice(["SGD", "Adam"])
        return chromo

    def crossover(parent1, parent2):
        """Combine two parents"""
        child = {}
        for key in parent1.keys():
            child[key] = random.choice([parent1[key], parent2[key]])
        return mutate(child)

    # ---------------------------
    # 🧠 CNN Model Builder
    # ---------------------------
    def build_model(params):
        classifier = Sequential()
        classifier.add(Convolution2D(params["filters"], 3, 3, input_shape=(100, 100, 3), activation='relu'))
        classifier.add(MaxPooling2D(pool_size=(2, 2)))

        classifier.add(Convolution2D(params["filters"], 3, 3, activation='relu'))
        classifier.add(MaxPooling2D(pool_size=(2, 2)))

        classifier.add(Flatten())
        classifier.add(Dense(params["dense_units"], activation='relu'))
        classifier.add(Dropout(params["dropout"]))
        classifier.add(Dense(2, activation='softmax'))

        if params["optimizer"] == "SGD":
            opt = optimizers.SGD(learning_rate=params["lr"])
        else:
            opt = optimizers.Adam(learning_rate=params["lr"])

        classifier.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        return classifier

    # ---------------------------
    # 🧩 GA Fitness Function
    # ---------------------------
    def evaluate_model(params):
        model = build_model(params)
        history = model.fit(
            training_set,
            steps_per_epoch=steps_per_epoch,
            epochs=EPOCHS_PER_MODEL,
            validation_data=test_set,
            validation_steps=val_steps,
            verbose=0
        )
        val_acc = np.mean(history.history['val_accuracy'][-3:])
        print(f"Tested: {params} -> Val Acc: {val_acc:.4f}")
        return val_acc

    # ---------------------------
    # 🚀 Run Genetic Algorithm
    # ---------------------------
    population = [create_chromosome() for _ in range(POP_SIZE)]

    for generation in range(GENERATIONS):
        print(f"\n=== Generation {generation + 1}/{GENERATIONS} ===")
        fitness_scores = [(chromo, evaluate_model(chromo)) for chromo in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        top = fitness_scores[:2]
        print(f"Top Performers: {top[0][0]} | Accuracy: {top[0][1]:.4f}")

        # Create next generation
        new_pop = [top[0][0], top[1][0]]  # keep best two
        while len(new_pop) < POP_SIZE:
            p1, p2 = random.sample(top, 2)
            new_pop.append(crossover(p1[0], p2[0]))
        population = new_pop

    # ---------------------------
    # 🏆 Train Best Model Fully
    # ---------------------------
    best_params = top[0][0]
    print("\nBest Parameters Found:", best_params)
    final_model = build_model(best_params)

    model = final_model.fit(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=1000,
        validation_data=test_set,
        validation_steps=val_steps
    )

    final_model.save(basepath + '/modelT.h5')

    # ---------------------------
    # 📊 Evaluation and Plotting
    # ---------------------------
    scores = final_model.evaluate(test_set, verbose=1)
    test_acc = f"Testing Accuracy: {scores[1] * 100:.2f}%"
    print(test_acc)
    scores = final_model.evaluate(training_set, verbose=1)
    train_acc = f"Training Accuracy: {scores[1] * 100:.2f}%"
    print(train_acc)

    msg = test_acc + '\n' + train_acc

    plt.plot(model.history['accuracy'])
    plt.plot(model.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.savefig(basepath + "/accuracy_ga.png", bbox_inches='tight')
    plt.show()

    plt.plot(model.history['loss'])
    plt.plot(model.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.savefig(basepath + "/loss_ga.png", bbox_inches='tight')
    plt.show()

    return msg
