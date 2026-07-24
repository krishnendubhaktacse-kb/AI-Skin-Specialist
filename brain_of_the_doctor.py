import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def update_progress(progress, image, video, doctor, image_path, video_path, progress_text):
    if not progress:
        return

    content = ""

    content += f"""
<div style="
font-size:22px;
font-weight:700;
margin-bottom:15px;
color:inherit;
">
{progress_text['title']}
</div>
"""


    if image_path:

        image_text = (
            progress_text["image"]["completed"]
            if image == "✅"
            else progress_text["image"]["processing"]
        )

        content += f"""
<div style="
margin:8px 0;
color:inherit;
">
{image} {image_text}
</div>
"""


    if video_path:

        video_text = (
            progress_text["video"]["completed"]
            if video == "✅"
            else progress_text["video"]["processing"]
        )

        content += f"""
<div style="
margin:8px 0;
color:inherit;
">
{video} {video_text}
</div>
"""


    doctor_text = (
        progress_text["doctor"]["completed"]
        if doctor == "✅"
        else progress_text["doctor"]["processing"]
    )

    content += f"""
<div style="
margin:8px 0;
color:inherit;
">
{doctor} {doctor_text}
</div>
"""


    html = f"""
<div style="
width:500px;
max-width:90%;
margin:20px auto;
padding:20px;
border:1px solid rgba(128,128,128,0.5);
border-radius:12px;
text-align:center;
font-size:16px;
line-height:1.8;
">

{content}

</div>
"""


    progress.markdown(
        html,
        unsafe_allow_html=True
    )

def analyze_skin(
    patient_question,
    image_path,
    video_path,
    language,
    progress=None,
):

    if language == "English 🇺🇸":

        progress_text = {
            "image": {
                "processing": "Analyzing your skin image...",
                "completed": "Skin image analysis completed"
            },
            "video": {
                "processing": "Analyzing your skin video...",
                "completed": "Skin video analysis completed"
            },
            "doctor": {
                "processing": "Preparing your AI diagnosis...",
                "completed": "AI diagnosis completed"
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
            "title": "🩺 एआई त्वचा विश्लेषण"
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

    # =====================================================
    # IMAGE ANALYSIS
    # =====================================================

    
    image_response = None

    if image_path:

        update_progress(
            progress,
            "🔄",
            "⏳",
            "⏳",
            image_path,
            video_path,
            progress_text
        )

        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()


        image_extension = os.path.splitext(image_path)[1].lower()


        if image_extension == ".png":
            image_mime = "image/png"

        elif image_extension in [".jpg", ".jpeg"]:
            image_mime = "image/jpeg"

        else:
            raise ValueError("Unsupported image format")


        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_mime,
        )


        image_prompt = f"""
You are an AI Skin Specialist.

Patient question:
{patient_question}

Analyze this skin image.

Provide:

1. Answer to patient's question
2. Visible skin observations
3. Possible skin concerns
4. Acne/pimples analysis
5. Pigmentation analysis
6. Redness or irritation
7. Skin texture analysis
8. Severity estimation
9. Possible causes
10. Skincare recommendations
11. When to consult a dermatologist

Important:
This is AI visual analysis only, not a confirmed diagnosis.
"""


        for attempt in range(5):

            try:

                print(
                    f"\nGenerating image analysis (Attempt {attempt + 1}/5)..."
                )


                image_response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[
                        image_prompt,
                        image_part,
                    ],
                )


                update_progress(
                    progress,
                    "✅",
                    "🔄",
                    "⏳",
                    image_path,
                    video_path,
                    progress_text
                )
                break


            except ServerError as e:

                print(f"\nServer busy: {e}")


                if attempt == 4:
                    raise


                print("Retrying in 10 seconds...")
                time.sleep(10)



    # =====================================================
    # VIDEO ANALYSIS
    # =====================================================

    video_response = None


    if video_path:

        update_progress(
            progress,
            "✅" if image_path else "",
            "🔄",
            "⏳",
            image_path,
            video_path,
            progress_text
        )


        video = client.files.upload(
            file=video_path
        )


        while video.state.name == "PROCESSING":

            print("Processing video...")

            time.sleep(5)


            video = client.files.get(
                name=video.name
            )


        if video.state.name == "FAILED":
            raise RuntimeError("Video processing failed")


        print("Video ready")


        video_prompt = f"""
You are an AI Skin Specialist.

Patient question:
{patient_question}

Analyze this skin video frame by frame.

Provide:

1. Skin condition observations
2. Changes visible during video
3. Acne/pimples analysis
4. Redness and irritation changes
5. Skin texture analysis
6. Severity estimation
7. Possible causes
8. Skincare recommendations
9. When dermatologist consultation is recommended

Important:
This is AI visual analysis only, not a confirmed diagnosis.
"""


        for attempt in range(5):

            try:

                print(
                    f"\nGenerating video analysis (Attempt {attempt + 1}/5)..."
                )


                video_response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[
                        video_prompt,
                        video,
                    ],
                )


                update_progress(
                    progress,
                    "✅",
                    "✅",
                    "🔄",
                    image_path,
                    video_path,
                    progress_text
                )
                break


            except ServerError as e:

                print(f"\nServer busy: {e}")


                if attempt == 4:
                    raise


                print("Retrying in 10 seconds...")
                time.sleep(10)



    # =====================================================
    # FINAL DOCTOR RESPONSE
    # =====================================================

    update_progress(
        progress,
        "✅",
        "✅",
        "🔄",
        image_path,
        video_path,
        progress_text
    )

    if language == "English 🇺🇸":

        language_instruction = """
Respond entirely in English.
Use clear, simple, professional language.
"""


    elif language == "हिन्दी 🇮🇳":

        language_instruction = """
Respond entirely in Hindi (हिन्दी).
Do not mix English except for unavoidable medical terms.
Use simple Hindi that an ordinary patient can understand.
"""


    else:

        language_instruction = """
Respond entirely in Bengali (বাংলা).
Do not mix English except for unavoidable medical terms.
Use simple Bengali that an ordinary patient can understand.
"""



    image_result = (
        image_response.text
        if image_response
        else "No image was provided. Image analysis was skipped."
    )


    video_result = (
        video_response.text
        if video_response
        else "No video was provided. Video analysis was skipped."
    )



    final_prompt = f"""
You are an experienced dermatologist and skin specialist.

{language_instruction}

The patient asked:

{patient_question}


Image Analysis:

{image_result}


Video Analysis:

{video_result}


Your task:

- Answer the patient's question naturally.
- Combine the available findings.
- Explain the likely skin condition in simple language.
- Mention uncertainty if applicable.
- Recommend basic skincare.
- Explain when the patient should consult a dermatologist.
- Do NOT say "Image Analysis" or "Video Analysis".
- Speak like a real doctor talking to a patient.
- Keep the response under 250 words.
- End by reminding the patient that this is an AI visual assessment and not a confirmed medical diagnosis.
"""


    final_response = None


    for attempt in range(5):

        try:

            print(
                f"\nGenerating final doctor response (Attempt {attempt + 1}/5)..."
            )


            final_response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=final_prompt,
            )


          
            break


        except ServerError as e:

            print(f"\nServer busy: {e}")


            if attempt == 4:
                raise


            print("Retrying in 10 seconds...")
            time.sleep(10)



    return final_response.text