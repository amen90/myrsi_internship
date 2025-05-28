import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Load MobileNetV2 pre-trained model without the top layers
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze base model layers
base_model.trainable = False

# Add custom layers on top
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)  # Fully connected layer with 1024 units
predictions = Dense(2, activation='softmax')(x)  # Assuming binary classification: healthy vs. unhealthy

# Final model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model with additional metrics (precision, recall)
model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

# Image data generator for training with advanced augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    zoom_range=0.2,
    rotation_range=30,
    brightness_range=[0.8, 1.2]
)

# Training data generator
train_generator = train_datagen.flow_from_directory(
    'dataset/train',  # Path to training dataset
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Validation data generator
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
    'dataset/validation',  # Path to validation dataset
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Early stopping and model checkpoint
early_stopping = EarlyStopping(monitor='val_loss', patience=3)
model_checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True, monitor='val_loss')

# Train the model with dynamic steps per epoch and validation steps
steps_per_epoch = len(train_generator)
validation_steps = len(val_generator)

model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps,
    callbacks=[early_stopping, model_checkpoint]
)

# Fine-tuning the base model after initial training
base_model.trainable = True

# Fine-tune from layer 100 onwards
for layer in base_model.layers[:100]:
    layer.trainable = False

# Re-compile the model with a lower learning rate for fine-tuning
model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), 
              loss='categorical_crossentropy', 
              metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

# Train the model again with fine-tuning
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps,
    callbacks=[early_stopping, model_checkpoint]
)
