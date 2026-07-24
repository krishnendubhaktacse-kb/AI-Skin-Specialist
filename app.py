import streamlit as st
import os
import threading
import time
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
from brain_of_the_doctor import analyze_skin, update_progress
from voice_of_the_patient import record_patient_voice
from voice_of_the_doctor import generate_doctor_voice


def generate_voice(doctor_response, language, result):
    result["audio_file"] = generate_doctor_voice(
        doctor_response,
        language=language
    )


st.set_page_config(
    page_title="AI Skin Specialist",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>

/* Make the main content wider */
.block-container{
    padding-top:3rem;
    padding-bottom:0;
    max-width:95%;
    min-height:100vh;
    display:flex;
    flex-direction:column;
}


/* Title */
.main-title{
    text-align:left;
    font-size:42px;
    font-weight:700;
    margin:0;
}


/* Mobile */
@media (max-width:768px){

    .block-container{
        max-width:100%;
    }

    .main-title{
        text-align:center;
        font-size:32px;
    }

    div[data-testid="stTextArea"] {
        margin-top:-15px;
    }

}


.footer {
    margin-top:auto;
    padding:8px 0;
    text-align:center;
    border-top:1px solid #e5e7eb;
    color:#666;
    font-size:14px;
    width:100%;
}


.footer p {
    margin:2px;
}

</style>
""", unsafe_allow_html=True)



header_left, header_right = st.columns([8, 2])


with header_right:
    language = st.selectbox(
        "",
        [
            "English 🇺🇸",
            "हिन्दी 🇮🇳",
            "বাংলা 🇮🇳"
        ]
    )


translations = {
    "English 🇺🇸": {
        "developer": "❤️ Designed & Developed with care and dedication by Krishnendu Bhakta",
        "footer": "AI-powered skin analysis assistant",
        "intro": "Upload your skin image or video and describe your problem for AI-powered skin analysis.",
        "uploaded_image": "Uploaded Skin Image",
        "uploaded_video": "Uploaded Skin Video",
        "upload_warning": "Please upload an image or video.",
        "question_warning": "Please enter or record your question.",
        "title": "🩺 AI Skin Specialist",
        "subtitle": "AI-powered dermatologist for skin analysis",
        "upload_image": "📷 Skin Image",
        "upload_video": "🎥 Skin Video",
        "question": "💬 Tell me your skin related issue",
        "placeholder": "Describe your skin problem here...",
        "voice": "🎤 Ask by Voice",
        "analyze": "🔍 Analyze Skin",
        "loading": "🩺 Doctor is analyzing your skin. Please wait a few seconds...",
        "response": "👨‍⚕️ Doctor Response",
    },

    "বাংলা 🇮🇳": {
        "developer": "❤️ যত্ন ও নিষ্ঠার সাথে কৃষ্ণেন্দু ভক্তের দ্বারা ডিজাইন ও তৈরি করা হয়েছে",
        "footer": "AI-চালিত ত্বক বিশ্লেষণ সহায়ক",
        "intro": "AI-চালিত ত্বক বিশ্লেষণের জন্য আপনার ত্বকের ছবি বা ভিডিও আপলোড করুন এবং আপনার সমস্যা জানান।",
        "uploaded_image": "আপলোড করা ত্বকের ছবি",
        "uploaded_video": "আপলোড করা ত্বকের ভিডিও",
        "upload_warning": "অনুগ্রহ করে একটি ছবি বা ভিডিও আপলোড করুন।",
        "question_warning": "অনুগ্রহ করে আপনার প্রশ্ন লিখুন অথবা কণ্ঠে বলুন।",
        "title": "🩺 AI ত্বক বিশেষজ্ঞ",
        "subtitle": "AI-চালিত ত্বক বিশ্লেষণ",
        "upload_image": "📷 ত্বকের ছবি",
        "upload_video": "🎥 ত্বকের ভিডিও",
        "question": "💬 আপনার ত্বকের সমস্যাটি লিখুন",
        "placeholder": "এখানে আপনার ত্বকের সমস্যাটি লিখুন...",
        "voice": "🎤 কণ্ঠে বলুন",
        "analyze": "🔍 ত্বক বিশ্লেষণ করুন",
        "loading": "🩺 ডাক্তার আপনার ত্বক বিশ্লেষণ করছেন। অনুগ্রহ করে কয়েক সেকেন্ড অপেক্ষা করুন...",
        "response": "👨‍⚕️ ডাক্তারের মতামত",
    },

    "हिन्दी 🇮🇳": {
        "developer": "❤️ देखभाल और समर्पण के साथ कृष्णेंदु भक्त द्वारा डिज़ाइन एवं विकसित किया गया",
        "footer": "AI-संचालित त्वचा विश्लेषण सहायक",
        "intro": "AI-संचालित त्वचा विश्लेषण के लिए अपनी त्वचा की तस्वीर या वीडियो अपलोड करें और अपनी समस्या बताएं।",
        "uploaded_image": "अपलोड की गई त्वचा की तस्वीर",
        "uploaded_video": "अपलोड किया गया त्वचा का वीडियो",
        "upload_warning": "कृपया एक तस्वीर या वीडियो अपलोड करें।",
        "question_warning": "कृपया अपना प्रश्न लिखें या आवाज़ से पूछें।",
        "title": "🩺 AI त्वचा विशेषज्ञ",
        "subtitle": "AI-द्वारा त्वचा विश्लेषण",
        "upload_image": "📷 त्वचा की तस्वीर",
        "upload_video": "🎥 त्वचा का वीडियो",
        "question": "💬 अपनी त्वचा की समस्या बताइए",
        "placeholder": "अपनी त्वचा की समस्या यहाँ लिखें...",
        "voice": "🎤 आवाज़ से पूछें",
        "analyze": "🔍 त्वचा का विश्लेषण करें",
        "loading": "🩺 डॉक्टर आपकी त्वचा का विश्लेषण कर रहे हैं। कृपया कुछ सेकंड प्रतीक्षा करें...",
        "response": "👨‍⚕️ डॉक्टर की सलाह",
    }
}

ui = translations[language]

with header_left:
    st.markdown(
        f"""
        <h1 style="
            margin-bottom:0px;
            font-size:42px;
            font-weight:700;
        ">
            {ui["title"]}
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.caption(ui["subtitle"])

if "patient_question" not in st.session_state:
    st.session_state.patient_question = ""

st.write(
    ui["intro"]
)


# Create upload folder

os.makedirs(
    "uploads",
    exist_ok=True
)


# Image Upload

upload_col1, upload_col2 = st.columns(
    [1, 1],
    gap="large"
)


with upload_col1:

    st.subheader(ui["upload_image"])

    image_file = st.file_uploader(
        "Upload Skin Image",
        type=["png", "jpg", "jpeg"],
        key="image_upload"
    )


with upload_col2:

    st.subheader(ui["upload_video"])

    video_file = st.file_uploader(
        "Upload Skin Video",
        type=["mp4", "mov", "avi", "mkv"],
        key="video_upload"
    )

image_path = None
video_path = None


# Save Image

if image_file:

    image_path = os.path.join(
        "uploads",
        image_file.name
    )

    with open(image_path, "wb") as f:
        f.write(
            image_file.getbuffer()
        )

    with upload_col1:

        st.image(
            image_file,
            width="stretch"
        )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:12px;
                color:gray;
                margin-top:5px;
            ">
                {ui["uploaded_image"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# Save Video

if video_file:

    video_path = os.path.join(
        "uploads",
        video_file.name
    )

    with open(video_path, "wb") as f:
        f.write(
            video_file.getbuffer()
        )

    with upload_col2:

        st.video(
            video_file,
            width="stretch"
        )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:12px;
                color:gray;
                margin-top:5px;
            ">
                {ui["uploaded_video"]}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    f"""
    <h2 style="
        text-align:center;
        font-size:28px;
        font-weight:700;
        margin-top:5px;
        margin-bottom:-15px;
    ">
        {ui["question"]}
    </h2>
    """,
    unsafe_allow_html=True
)

center_col = st.columns([2, 4, 2])

with center_col[1]:

    patient_question = st.text_area(
        "",
        value=st.session_state.patient_question,
        placeholder=ui["placeholder"],
        height=180
    )


button_col1, button_col2 = st.columns(2)


with center_col[1]:

    button_col1, button_col2 = st.columns(2)

    with button_col1:

        voice_button = st.button(
            ui["voice"],
            use_container_width=True
        )


    with button_col2:

        analyze_button = st.button(
            ui["analyze"],
            use_container_width=True
        )

if voice_button:

    with st.spinner("Listening..."):

        voice_text = record_patient_voice(language)

    if st.session_state.patient_question.strip():
        st.session_state.patient_question += " " + voice_text
    else:
        st.session_state.patient_question = voice_text

    st.rerun()

# Analyze Button
# Analyze Button
if analyze_button:

    final_question = patient_question.strip()

    progress_col = st.columns([2, 3, 2])

    with progress_col[1]:
        progress = st.empty()

    if language == "English 🇺🇸":

        progress_text = {
            "image": {
                "processing": "Analyzing Your Skin Image...",
                "completed": "Skin Image Analysis Completed"
            },
            "video": {
                "processing": "Analyzing Your Skin Video...",
                "completed": "Skin Video Analysis Completed"
            },
            "doctor": {
                "processing": "Preparing your AI Diagnosis...",
                "completed": "AI Diagnosis Completed"
            },
            "title": "🩺 AI Skin Analysis"
        }

    elif language == "हिन्दी 🇮🇳":

        progress_text = {
            "image": {
                "processing": "आपकी त्वचा की तस्वीर का विश्लेषण किया जा रहा है...",
                "completed": "त्वचा की तस्वीर का विश्लेषण पूरा हुआ"
            },
            "video": {
                "processing": "आपकी त्वचा के वीडियो का विश्लेषण किया जा रहा है...",
                "completed": "त्वचा के वीडियो का विश्लेषण पूरा हुआ"
            },
            "doctor": {
                "processing": "आपका AI निदान तैयार किया जा रहा है...",
                "completed": "AI निदान पूरा हुआ"
            },
            "title": "🩺 AI त्वचा विश्लेषण"
        }

    else:

        progress_text = {
            "image": {
                "processing": "আপনার ত্বকের ছবি বিশ্লেষণ করা হচ্ছে...",
                "completed": "ত্বকের ছবি বিশ্লেষণ সম্পন্ন হয়েছে"
            },
            "video": {
                "processing": "আপনার ত্বকের ভিডিও বিশ্লেষণ করা হচ্ছে...",
                "completed": "ত্বকের ভিডিও বিশ্লেষণ সম্পন্ন হয়েছে"
            },
            "doctor": {
                "processing": "আপনার AI নির্ণয় প্রস্তুত করা হচ্ছে...",
                "completed": "AI নির্ণয় সম্পন্ন হয়েছে"
            },
            "title": "🩺 AI ত্বক বিশ্লেষণ"
        }

    update_progress(
        progress,
        "⏳",
        "⏳",
        "⏳",
        image_path,
        video_path,
        progress_text,
    )

    if not final_question:
        final_question = st.session_state.patient_question.strip()

    if (image_path or video_path) and final_question:

        doctor_response = analyze_skin(
            patient_question=final_question,
            image_path=image_path,
            video_path=video_path,
            language=language,
            progress=progress
        )

        voice_result = {}

        voice_thread = threading.Thread(
            target=generate_voice,
            args=(
                doctor_response,
                language,
                voice_result
            )
        )

        voice_thread.start()

        while voice_thread.is_alive():
            time.sleep(1)

        voice_thread.join()

        update_progress(
            progress,
            "✅" if image_path else "",
            "✅" if video_path else "",
            "✅",
            image_path,
            video_path,
            progress_text,
        )

        st.markdown(
            f"""
            <h2 style="
                text-align:center;
                font-size:28px;
                font-weight:700;
                margin-top:30px;
                margin-bottom:15px;
            ">
                {ui["response"]}
            </h2>
            """,
            unsafe_allow_html=True
        )

        response_col = st.columns([1, 4, 1])

        with response_col[1]:

            st.markdown(
                f"""
                <div style="
                    padding:25px;
                    border-radius:15px;
                    border:1px solid #ddd;
                    background-color:#fafafa;
                    color:#111111;
                    font-size:16px;
                    line-height:1.6;
                ">
                    {doctor_response}
                </div>
                """,
                unsafe_allow_html=True
            )

        audio_file = voice_result["audio_file"]

        with open(audio_file, "rb") as audio:
            audio_bytes = audio.read()

        st.audio(
            audio_bytes,
            format="audio/wav",
            autoplay=True
        )

    elif not image_path and not video_path:

        st.warning(ui["upload_warning"])

    elif not final_question:

        st.warning(ui["question_warning"])

st.markdown(
    f"""
    <div class="footer">
        <p>{ui['footer']}</p>
        <p>{ui['developer']}</p>
    </div>
    """,
    unsafe_allow_html=True
)