from voice_of_the_patient import get_patient_voice
from brain_of_the_doctor import analyze_skin
from voice_of_the_doctor import speak_doctor_response


def main():

    print("\n" + "=" * 70)
    print("AI SKIN SPECIALIST")
    print("=" * 70)

    print("\nListening to the patient...\n")

    patient_question = get_patient_voice()

    print("\nPatient Question:")
    print(patient_question)

    print("\nDoctor is analyzing your skin...\n")

    doctor_response = analyze_skin(
        patient_question=patient_question
    )

    print("\n" + "=" * 70)
    print("DOCTOR RESPONSE")
    print("=" * 70)

    print(doctor_response)

    print("\nDoctor is speaking...\n")

    speak_doctor_response(
        doctor_response
    )

if __name__ == "__main__":
    main()