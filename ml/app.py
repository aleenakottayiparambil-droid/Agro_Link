from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import numpy as np

from PIL import Image
import io


# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

CORS(app)


# =====================================================
# MODEL CONFIGURATION
# =====================================================

MODEL_PATH = "crop_disease_cnn.keras"

IMAGE_SIZE = (128, 128)


# =====================================================
# CLASS NAMES
# =====================================================

CLASS_NAMES = [

    "Pepper__bell___Bacterial_spot",

    "Pepper__bell___healthy",

    "Potato___Early_blight",

    "Potato___Late_blight",

    "Potato___healthy",

    "Tomato_Bacterial_spot",

    "Tomato_Early_blight",

    "Tomato_Late_blight",

    "Tomato_Leaf_Mold",

    "Tomato_Septoria_leaf_spot",

    "Tomato_Spider_mites_Two_spotted_spider_mite",

    "Tomato__Target_Spot",

    "Tomato__Tomato_YellowLeaf__Curl_Virus",

    "Tomato__Tomato_mosaic_virus",

    "Tomato_healthy"

]


# =====================================================
# RECOMMENDATIONS
# =====================================================

RECOMMENDATIONS = {

    "Pepper__bell___Bacterial_spot":
        "Remove infected leaves and avoid overhead irrigation. Use appropriate bacterial disease management practices.",

    "Pepper__bell___healthy":
        "The pepper plant appears healthy. Continue proper watering, nutrition and regular monitoring.",

    "Potato___Early_blight":
        "Remove infected leaves and improve air circulation. Avoid overhead watering and consider appropriate fungicide management.",

    "Potato___Late_blight":
        "Remove severely infected plant material and avoid excessive moisture. Consult an agricultural expert for suitable fungicide treatment.",

    "Potato___healthy":
        "The potato plant appears healthy. Continue regular monitoring and maintain proper irrigation and nutrition.",

    "Tomato_Bacterial_spot":
        "Remove infected leaves and avoid wetting the foliage. Maintain good air circulation and use suitable disease management practices.",

    "Tomato_Early_blight":
        "Remove affected leaves, improve air circulation and avoid overhead irrigation. Consider appropriate fungicide treatment.",

    "Tomato_Late_blight":
        "Remove infected plant material immediately and avoid excess moisture. Consult an agricultural expert for suitable treatment.",

    "Tomato_Leaf_Mold":
        "Improve ventilation and reduce humidity around the plants. Remove infected leaves and monitor the crop closely.",

    "Tomato_Septoria_leaf_spot":
        "Remove infected leaves and avoid overhead watering. Keep adequate spacing between plants to improve air circulation.",

    "Tomato_Spider_mites_Two_spotted_spider_mite":
        "Inspect the underside of leaves and remove heavily affected leaves. Maintain adequate plant moisture and consider appropriate pest management.",

    "Tomato__Target_Spot":
        "Remove affected leaves and improve air circulation. Avoid overhead irrigation and monitor the plant regularly.",

    "Tomato__Tomato_YellowLeaf__Curl_Virus":
        "Remove severely infected plants and control whitefly populations, which can spread the virus.",

    "Tomato__Tomato_mosaic_virus":
        "Remove infected plants and sanitize tools. Avoid handling healthy plants after touching infected plants.",

    "Tomato_healthy":
        "The tomato plant appears healthy. Continue regular monitoring, watering and proper crop nutrition."

}


# =====================================================
# LOAD CNN MODEL
# =====================================================

print()
print("======================================")
print("       AGROLINK AI CNN API")
print("======================================")
print()

print("Loading CNN model...")

try:

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("CNN model loaded successfully!")

except Exception as error:

    print("ERROR: Could not load CNN model.")

    print(error)

    model = None


# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "success": True,

        "message":
            "AgroLink AI Crop Disease CNN API is running",

        "model":
            MODEL_PATH,

        "classes":
            len(CLASS_NAMES)

    })


# =====================================================
# PREDICTION ROUTE
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    # -------------------------------------------------
    # CHECK MODEL
    # -------------------------------------------------

    if model is None:

        return jsonify({

            "success": False,

            "message":
                "CNN model is not loaded."

        }), 500


    # -------------------------------------------------
    # CHECK IMAGE
    # -------------------------------------------------

    if "image" not in request.files:

        return jsonify({

            "success": False,

            "message":
                "No image uploaded."

        }), 400


    file = request.files["image"]


    if file.filename == "":

        return jsonify({

            "success": False,

            "message":
                "No image selected."

        }), 400


    try:

        # -------------------------------------------------
        # READ IMAGE
        # -------------------------------------------------

        image_bytes = file.read()

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        # Convert to RGB

        image = image.convert("RGB")


        # -------------------------------------------------
        # RESIZE
        # -------------------------------------------------

        image = image.resize(
            IMAGE_SIZE
        )


        # -------------------------------------------------
        # CONVERT TO NUMPY
        # -------------------------------------------------

        image_array = np.array(
            image
        )


        # -------------------------------------------------
        # ADD BATCH DIMENSION
        # -------------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # -------------------------------------------------
        # CNN PREDICTION
        # -------------------------------------------------

        predictions = model.predict(
            image_array,
            verbose=0
        )


        # -------------------------------------------------
        # FIND BEST CLASS
        # -------------------------------------------------

        predicted_index = np.argmax(
            predictions[0]
        )


        confidence = (
            float(predictions[0][predicted_index])
            * 100
        )


        disease = CLASS_NAMES[
            predicted_index
        ]


        # -------------------------------------------------
        # RECOMMENDATION
        # -------------------------------------------------

        recommendation = RECOMMENDATIONS.get(

            disease,

            "Please consult an agricultural expert for further treatment advice."

        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "prediction":
                disease,

            "disease":
                disease,

            "confidence":
                round(confidence, 2),

            "recommendation":
                recommendation

        })


    except Exception as error:

        print("Prediction error:")
        print(error)

        return jsonify({

            "success": False,

            "message":
                "Error processing image.",

            "error":
                str(error)

        }), 500


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       AGROLINK AI CNN API")
    print("======================================")
    print("Server: http://localhost:8000")
    print()

    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False

    )