import tensorflow as tf
from tensorflow.keras import layers, models
import os


# =========================================================
# CONFIGURATION
# =========================================================

DATASET_PATH = r".\dataset\PlantVillage\PlantVillage"

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 15
VALIDATION_SPLIT = 0.20
SEED = 42


# =========================================================
# CHECK DATASET
# =========================================================

print()
print("======================================")
print("       AGROLINK AI CNN TRAINING")
print("======================================")
print()

print("Checking dataset...")

if not os.path.exists(DATASET_PATH):
    print("ERROR: Dataset not found!")
    print("Dataset path:")
    print(os.path.abspath(DATASET_PATH))
    exit()

print("Dataset found:")
print(os.path.abspath(DATASET_PATH))


# =========================================================
# LOAD TRAINING DATA
# =========================================================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,

    validation_split=VALIDATION_SPLIT,

    subset="training",

    seed=SEED,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE
)


# =========================================================
# LOAD VALIDATION DATA
# =========================================================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,

    validation_split=VALIDATION_SPLIT,

    subset="validation",

    seed=SEED,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE
)


# =========================================================
# CLASS NAMES
# =========================================================

class_names = train_dataset.class_names

num_classes = len(class_names)


print()
print("Number of classes:", num_classes)

print()
print("Classes:")

for index, class_name in enumerate(class_names):

    print(index, ":", class_name)


# =========================================================
# PERFORMANCE OPTIMIZATION
# =========================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.cache().shuffle(
    1000
).prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.cache().prefetch(
    buffer_size=AUTOTUNE
)


# =========================================================
# DATA AUGMENTATION
# =========================================================

data_augmentation = tf.keras.Sequential([

    layers.RandomFlip(
        "horizontal"
    ),

    layers.RandomRotation(
        0.1
    ),

    layers.RandomZoom(
        0.1
    )

])


# =========================================================
# CNN MODEL
# =========================================================

model = models.Sequential([

    # Input
    layers.Input(
        shape=(128, 128, 3)
    ),

    # Data augmentation
    data_augmentation,

    # Normalize pixels
    layers.Rescaling(
        1.0 / 255
    ),


    # =====================================
    # CNN BLOCK 1
    # =====================================

    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(
        (2, 2)
    ),


    # =====================================
    # CNN BLOCK 2
    # =====================================

    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(
        (2, 2)
    ),


    # =====================================
    # CNN BLOCK 3
    # =====================================

    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(
        (2, 2)
    ),


    # =====================================
    # CLASSIFICATION
    # =====================================

    layers.Flatten(),

    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(
        0.5
    ),

    layers.Dense(
        num_classes,
        activation="softmax"
    )

])


# =========================================================
# DISPLAY MODEL
# =========================================================

print()

model.summary()


# =========================================================
# COMPILE MODEL
# =========================================================

model.compile(

    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=[
        "accuracy"
    ]

)


# =========================================================
# CALLBACKS
# =========================================================

callbacks = [

    tf.keras.callbacks.EarlyStopping(

        monitor="val_loss",

        patience=3,

        restore_best_weights=True

    ),

    tf.keras.callbacks.ModelCheckpoint(

        "crop_disease_cnn.keras",

        monitor="val_accuracy",

        save_best_only=True

    )

]


# =========================================================
# TRAIN CNN
# =========================================================

print()
print("======================================")
print("       STARTING CNN TRAINING")
print("======================================")
print()


history = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=EPOCHS,

    callbacks=callbacks

)


# =========================================================
# FINAL MESSAGE
# =========================================================

print()
print("======================================")
print("       CNN TRAINING COMPLETED")
print("======================================")
print()

print("Best model saved as:")
print("crop_disease_cnn.keras")

print()

print("Training completed successfully!")