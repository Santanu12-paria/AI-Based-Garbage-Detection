import streamlit as st
from ultralytics import YOLO
from PIL import Image
from collections import Counter
import tempfile
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Garbage Detection",
    page_icon="🗑️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

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
        color: #666666;
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


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🗑️ AI-Based Garbage Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart Waste Management using YOLO Object Detection'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Project Information")

    st.write("### 🤖 Model")
    st.write("YOLO Object Detection")

    st.write("### 🎯 Detection Confidence")
    st.write("0.15")

    st.write("### ♻️ Waste Classes")

    classes = [
        "LDPE",
        "Bottle",
        "Can",
        "Cardboard",
        "Organic",
        "Paper",
        "Plastic"
    ]

    for item in classes:
        st.write(f"• {item}")

    st.markdown("---")

    st.info(
        "Upload a garbage image to detect and classify "
        "different types of waste."
    )


# =========================================================
# MODEL
# =========================================================

MODEL_PATH = r"runs\detect\garbage_detection-2\weights\best.pt"

if not os.path.exists(MODEL_PATH):

    st.error(
        f"❌ Model not found:\n\n{MODEL_PATH}"
    )

    st.stop()


# Load YOLO model
model = YOLO(MODEL_PATH)


# =========================================================
# IMAGE UPLOAD
# =========================================================

st.subheader("📤 Upload Garbage Image")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
    help="Upload a JPG, JPEG or PNG image."
)


# =========================================================
# IMAGE PROCESSING
# =========================================================

if uploaded_file is not None:

    # Open and convert image to RGB
    image = Image.open(uploaded_file).convert("RGB")

    st.markdown("---")

    # =====================================================
    # TEMPORARY IMAGE
    # =====================================================

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:

        image.save(
            temp_file.name,
            format="JPEG"
        )

        temp_path = temp_file.name

    # =====================================================
    # YOLO DETECTION
    # =====================================================

    with st.spinner("🔍 AI is detecting garbage..."):

        results = model.predict(
            source=temp_path,
            conf=0.15,
            verbose=False
        )

    # Remove temporary file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Get first result
    result = results[0]


    # =====================================================
    # IMAGE COMPARISON
    # =====================================================

    st.subheader("📷 Image Analysis")

    col1, col2 = st.columns(2)

    # Original image
    with col1:

        st.markdown("### 📷 Original Image")

        st.image(
            image,
            use_container_width=True
        )

    # Detection image
    with col2:

        st.markdown("### 🤖 Detection Result")

        annotated_image = result.plot()

        st.image(
            annotated_image,
            use_container_width=True
        )

    st.markdown("---")


    # =====================================================
    # CHECK DETECTIONS
    # =====================================================

    if result.boxes is not None and len(result.boxes) > 0:

        # -------------------------------------------------
        # CLASS IDs
        # -------------------------------------------------

        class_ids = result.boxes.cls.tolist()


        # -------------------------------------------------
        # CLASS NAMES
        # -------------------------------------------------

        detected_names = [
            model.names[int(class_id)]
            for class_id in class_ids
        ]


        # -------------------------------------------------
        # CLASS COUNTS
        # -------------------------------------------------

        counts = Counter(detected_names)


        # -------------------------------------------------
        # CONFIDENCE VALUES
        # -------------------------------------------------

        confidence_values = result.boxes.conf.tolist()


        # -------------------------------------------------
        # AVERAGE CONFIDENCE
        # -------------------------------------------------

        average_confidence = (
            sum(confidence_values)
            / len(confidence_values)
        )


        # -------------------------------------------------
        # TOTAL OBJECTS
        # -------------------------------------------------

        total_objects = len(detected_names)


        # =================================================
        # DETECTION SUMMARY
        # =================================================

        st.subheader("📊 Detection Summary")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "🗑️ Total Objects",
                total_objects
            )

        with metric2:

            st.metric(
                "🏷️ Waste Types",
                len(counts)
            )

        with metric3:

            st.metric(
                "🎯 Avg. Confidence",
                f"{average_confidence * 100:.1f}%"
            )

        st.markdown("---")


        # =================================================
        # CLASS-WISE COUNTS
        # =================================================

        st.subheader("♻️ Waste Classification")

        count_cols = st.columns(len(counts))

        for col, (name, count) in zip(
            count_cols,
            counts.items()
        ):

            with col:

                st.metric(
                    name.upper(),
                    count
                )

        st.markdown("---")


        # =================================================
        # WASTE LEVEL
        # =================================================

        st.subheader("🚮 Waste Level")

        if total_objects <= 3:

            waste_level = "LOW"

            st.success(
                "🟢 LOW WASTE — Small amount of garbage detected."
            )

        elif total_objects <= 7:

            waste_level = "MEDIUM"

            st.warning(
                "🟡 MEDIUM WASTE — Moderate amount of garbage detected."
            )

        else:

            waste_level = "HIGH"

            st.error(
                "🔴 HIGH WASTE — Large amount of garbage detected."
            )

        st.markdown("---")


        # =================================================
        # DETECTION DETAILS
        # =================================================

        st.subheader("🔎 Detection Details")

        for i, (name, confidence) in enumerate(
            zip(
                detected_names,
                confidence_values
            ),
            start=1
        ):

            st.write(
                f"**{i}. {name.upper()}** — "
                f"{confidence * 100:.1f}% confidence"
            )

        st.markdown("---")


        # =================================================
        # DETECTION REPORT TABLE
        # =================================================

        st.subheader("📋 Detection Report")

        detection_data = []

        for name, confidence in zip(
            detected_names,
            confidence_values
        ):

            detection_data.append(
                {
                    "Waste Type": name.upper(),
                    "Confidence": f"{confidence * 100:.1f}%"
                }
            )

        st.table(detection_data)


    # =====================================================
    # NO DETECTION
    # =====================================================

    else:

        st.warning(
            "⚠️ No garbage objects were detected in this image."
        )


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.markdown("---")

st.subheader("📚 About the Project")

st.write(
    """
    **AI-Based Garbage Detection for Smart Waste Management**

    This project uses a YOLO-based deep learning object detection
    model to identify and classify different types of garbage from
    uploaded images. The system can detect multiple waste objects
    and provide their class names, confidence scores and total count.

    The application is developed using **Python, YOLO, Ultralytics
    and Streamlit**.
    """
)


# =========================================================
# PROJECT FEATURES
# =========================================================

st.subheader("✨ Key Features")

feature1, feature2, feature3, feature4 = st.columns(4)

with feature1:

    st.write("📷 **Image Upload**")
    st.caption("Upload JPG, JPEG or PNG images.")


with feature2:

    st.write("🤖 **AI Detection**")
    st.caption("YOLO detects waste objects.")


with feature3:

    st.write("📊 **Analysis**")
    st.caption("View counts and confidence scores.")


with feature4:

    st.write("♻️ **Waste Level**")
    st.caption("LOW, MEDIUM or HIGH waste.")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'AI-Based Garbage Detection | YOLO Object Detection | '
    'Deep Learning | Smart Waste Management'
    '</div>',
    unsafe_allow_html=True
)