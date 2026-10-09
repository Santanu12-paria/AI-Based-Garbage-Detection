
import streamlit as st
from ultralytics import YOLO
from PIL import Image
from collections import Counter
from pathlib import Path


# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="AI Based Waste Detection",
    page_icon="🗑️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CUSTOM STYLING ----------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777777;
        margin-bottom: 25px;
    }

    .footer {
        text-align: center;
        color: #777777;
        font-size: 14px;
        margin-top: 35px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- APPLICATION HEADER ----------------
st.markdown(
    '<div class="main-title">🗑️ AI Based Waste Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart Waste Management using YOLOv8 Object Detection'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ---------------- MODEL CONFIGURATION ----------------
MODEL_PATH = Path(
    "runs/detect/garbage_detection-2/weights/best.pt"
)


@st.cache_resource
def load_model(model_path):
    return YOLO(str(model_path))


if not MODEL_PATH.is_file():
    st.error(f"Trained YOLOv8 model not found: {MODEL_PATH}")
    st.info(
        "Check that app.py is running from your project folder "
        "and that the best.pt file exists at the specified path."
    )
    st.stop()


try:
    model = load_model(MODEL_PATH.resolve())
except Exception as error:
    st.error(f"Unable to load the trained model: {error}")
    st.stop()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Project Information")

    st.subheader("🤖 AI Model")
    st.write("YOLOv8 Nano (YOLOv8n)")
    st.write("Custom-trained object detection model")

    st.subheader("🎯 Detection Confidence")

    conf_threshold = st.slider(
        "Confidence threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.40,
        step=0.05,
        help=(
            "Lower values may detect more objects but can also "
            "produce false detections."
        )
    )

    st.subheader("♻️ Waste Classes")

    for name in model.names.values():
        st.write(f"• {name}")

    st.markdown("---")

    st.info(
        "Upload an image to identify and classify garbage "
        "using the trained YOLOv8 model."
    )


# ---------------- IMAGE UPLOAD ----------------
st.subheader("📤 Upload Garbage Image")

uploaded_file = st.file_uploader(
    "Choose a garbage image",
    type=["jpg", "jpeg", "png"],
    help="Upload a JPG, JPEG, or PNG image."
)


if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file).convert("RGB")
    except Exception:
        st.error("Unable to read this image. Please upload a valid image.")
        st.stop()

    st.markdown("---")

    # ---------------- OBJECT DETECTION ----------------
    with st.spinner("🔍 YOLOv8 is detecting garbage..."):

        try:
            results = model.predict(
                source=image,
                conf=conf_threshold,
                imgsz=640,
                verbose=False
            )

            result = results[0]

        except Exception as error:
            st.error(f"Detection failed: {error}")
            st.stop()

    # ---------------- IMAGE COMPARISON ----------------
    st.subheader("📷 Image Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📷 Original Image")
        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    with col2:
        st.markdown("### 🤖 Detection Result")

        # Ultralytics returns the plotted image in BGR order.
        # Convert it to RGB for Streamlit.
        annotated_image = result.plot()[..., ::-1]

        st.image(
            annotated_image,
            caption="YOLOv8 Detection Output",
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- DETECTION SUMMARY ----------------
    if result.boxes is not None and len(result.boxes) > 0:

        class_ids = [
            int(class_id)
            for class_id in result.boxes.cls.tolist()
        ]

        detected_names = [
            model.names[class_id]
            for class_id in class_ids
        ]

        confidences = result.boxes.conf.tolist()

        counts = Counter(detected_names)

        total_objects = len(detected_names)
        total_types = len(counts)
        average_confidence = (
            sum(confidences) / len(confidences)
        )

        st.subheader("📊 Detection Summary")

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "🗑️ Total Objects",
            total_objects
        )

        metric2.metric(
            "🏷️ Waste Types",
            total_types
        )

        metric3.metric(
            "🎯 Average Confidence",
            f"{average_confidence * 100:.1f}%"
        )

        st.markdown("---")

        # ---------------- WASTE CLASSIFICATION ----------------
        st.subheader("♻️ Waste Classification")

        classification_data = [
            {
                "Waste Type": name,
                "Count": count
            }
            for name, count in counts.items()
        ]

        st.table(classification_data)

        st.markdown("---")

        # ---------------- WASTE LEVEL ----------------
        st.subheader("🚮 Waste Level")

        if total_objects <= 3:
            st.success(
                "🟢 LOW WASTE — A small number of objects detected."
            )

        elif total_objects <= 7:
            st.warning(
                "🟡 MEDIUM WASTE — A moderate number of objects detected."
            )

        else:
            st.error(
                "🔴 HIGH WASTE — A large number of objects detected."
            )

        st.caption(
            "Waste level is estimated from the number of detected "
            "objects in this image. It is not a measurement of "
            "actual waste volume or weight."
        )

        st.markdown("---")

        # ---------------- DETECTION DETAILS ----------------
        st.subheader("🔎 Detection Details")

        for index, (name, confidence) in enumerate(
            zip(detected_names, confidences),
            start=1
        ):
            st.write(
                f"**{index}. {name}** — "
                f"{confidence * 100:.1f}% confidence"
            )

        st.markdown("---")

        # ---------------- DETECTION REPORT ----------------
        st.subheader("📋 Detection Report")

        report_data = [
            {
                "Object No.": index,
                "Waste Type": name,
                "Confidence": f"{confidence * 100:.1f}%"
            }
            for index, (name, confidence) in enumerate(
                zip(detected_names, confidences),
                start=1
            )
        ]

        st.dataframe(
            report_data,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning(
            "⚠️ No garbage objects were detected. "
            "Try lowering the confidence threshold or uploading "
            "a clearer image."
        )


# ---------------- ABOUT THE PROJECT ----------------
st.markdown("---")

st.subheader("📚 About the Project")

st.write(
    """
    **AI-Based Garbage Detection for Smart Waste Management**

    This project uses a custom-trained YOLOv8 Nano deep learning
    object detection model to identify and classify garbage in
    uploaded images.

    The application displays annotated images, detected waste
    categories, object counts, confidence scores, and a simple
    waste-level estimate.

    **Technologies:** Python, YOLOv8, Ultralytics, Streamlit and Pillow.
    """
)


# ---------------- KEY FEATURES ----------------
st.subheader("✨ Key Features")

feature1, feature2, feature3, feature4 = st.columns(4)

with feature1:
    st.write("📷 **Image Upload**")
    st.caption("Upload JPG, JPEG, or PNG images.")

with feature2:
    st.write("🤖 **AI Detection**")
    st.caption("Detect garbage using your trained YOLOv8 model.")

with feature3:
    st.write("📊 **Analysis**")
    st.caption("View detected objects and confidence scores.")

with feature4:
    st.write("♻️ **Waste Classification**")
    st.caption("Review waste categories and estimated waste level.")


# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">'
    'AI-Based Garbage Detection | YOLOv8 Nano | '
    'Deep Learning | Smart Waste Management'
    '</div>',
    unsafe_allow_html=True
)

