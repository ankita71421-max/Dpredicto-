from symptom_mapping import SYMPTOM_MAPPING
from disease_info import DISEASE_INFO
from disease_symptom_mapping import DISEASE_SYMPTOMS
from question_mapping import QUESTION_MAPPING

from disease_rules import (
    DISEASE_PENALTIES,
    DETAIL_QUESTIONS,
    DETAIL_CLUES,
    get_detail_question,
    get_detail_clue
)

import pandas as pd
import re


print("Dpredicto chatbot started successfully!")
print("Number of symptom mappings:", len(SYMPTOM_MAPPING))
print("Number of diseases:", len(DISEASE_INFO))
print("ML models connected successfully!")


# =========================================================
# 1. DISEASE-SPECIFIC EXTRA SYMPTOMS
# =========================================================

EXTRA_DISEASE_SYMPTOMS = {

    "Chicken pox": {
        "blister",
        "skin_rash",
        "red_spots_over_body"
    },

    "Impetigo": {
        "blister",
        "red_sore_around_nose",
        "yellow_crust_ooze"
    },

    "Malaria": {
        "chills",
        "sweating"
    },

    "Dengue": {
        "pain_behind_the_eyes",
        "muscle_pain",
        "joint_pain"
    },

    "Tuberculosis": {
        "cough",
        "weight_loss",
        "blood_in_sputum",
        "chest_pain",
        "phlegm"
    }
}


# =========================================================
# SERIOUS SYMPTOMS
# =========================================================

BLOCKED_FOLLOW_UP_SYMPTOMS = {
    "coma",
    "unconsciousness",
    "paralysis",
    "brain_hemorrhage"
}


# =========================================================
# 2. DISEASE PRIORITY SYMPTOMS
# =========================================================

DISEASE_PRIORITY_SYMPTOMS = {

    "Chicken pox": [
        "skin_rash",
        "itching",
        "red_spots_over_body",
        "blister"
    ],

    "Dengue": [
        "skin_rash",
        "headache",
        "pain_behind_the_eyes",
        "joint_pain",
        "muscle_pain",
        "nausea",
        "vomiting",
        "bleeding"
    ],

    "Malaria": [
        "chills",
        "sweating",
        "headache",
        "nausea",
        "vomiting"
    ],

    "Jaundice": [
        "yellowish_skin",
        "yellowing_of_eyes",
        "dark_urine",
        "abdominal_pain",
        "itching"
    ],

    "Hepatitis B": [
        "yellowish_skin",
        "yellowing_of_eyes",
        "dark_urine",
        "abdominal_pain",
        "nausea",
        "vomiting"
    ],

    "Tuberculosis": [
        "cough",
        "weight_loss",
        "night_sweats",
        "chest_pain",
        "blood_in_sputum",
        "phlegm"
    ]
}


# =========================================================
# 3. PATIENT STATE
# =========================================================

patient_state = {

    "present_symptoms": set(),

    "absent_symptoms": set(),

    "asked_symptoms": set(),

    "detail_questions_asked": set(),

    "detail_scores": {},

    "detail_score_keys": set(),

    "conversation_history": [],

    "patient_details": {}
}


# =========================================================
# 4. RESET PATIENT STATE
# =========================================================

def reset_patient_state():

    patient_state["present_symptoms"].clear()

    patient_state["absent_symptoms"].clear()

    patient_state["asked_symptoms"].clear()

    patient_state["detail_questions_asked"].clear()

    patient_state["detail_scores"].clear()

    patient_state["detail_score_keys"].clear()

    patient_state["conversation_history"].clear()

    patient_state["patient_details"].clear()


# =========================================================
# 5. UPDATE PATIENT STATE
# =========================================================

def update_patient_state(present, absent):

    patient_state["present_symptoms"].update(present)

    patient_state["absent_symptoms"].update(absent)

    patient_state["absent_symptoms"].difference_update(
        patient_state["present_symptoms"]
    )


# =========================================================
# 6. SHOW PATIENT STATE
# =========================================================

def show_patient_state():

    print("\n--------------------------------")

    print(
        "Present symptoms:",
        sorted(
            patient_state["present_symptoms"]
        )
    )

    print(
        "Absent symptoms:",
        sorted(
            patient_state["absent_symptoms"]
        )
    )

    print("--------------------------------")


# =========================================================
# 7. NEGATION DETECTION
# =========================================================

def is_negated(message, start_position):

    before = message[:start_position].strip()

    if not before:
        return False

    negation_patterns = [

        r"\bno\s*$",

        r"\bnot\s*$",

        r"\bdon't\s+have\s*$",

        r"\bdo\s+not\s+have\s*$",

        r"\bdoesn't\s+have\s*$",

        r"\bdoes\s+not\s+have\s*$",

        r"\bhaven't\s+had\s*$",

        r"\bhave\s+not\s+had\s*$",

        r"\bwithout\s*$",

        r"\bnever\s+have\s*$"
    ]

    for pattern in negation_patterns:

        if re.search(
            pattern,
            before,
            re.IGNORECASE
        ):
            return True

    return False


# =========================================================
# 8. SYMPTOM EXTRACTION
# =========================================================

def extract_symptoms(message):

    message = message.lower()

    present = []

    absent = []

    for symptom, phrases in SYMPTOM_MAPPING.items():

        # Fever handled separately.
        if symptom in {
            "fever",
            "high_fever",
            "mild_fever",
            "low_fever"
        }:
            continue

        for phrase in phrases:

            phrase = phrase.lower().strip()

            if not phrase:
                continue

            pattern = (
                r"\b"
                +
                re.escape(phrase)
                +
                r"\b"
            )

            match = re.search(
                pattern,
                message
            )

            if not match:
                continue

            if is_negated(
                message,
                match.start()
            ):

                if symptom not in absent:
                    absent.append(symptom)

            else:

                if symptom not in present:
                    present.append(symptom)

            break

    return present, absent


# =========================================================
# 9. GET DISEASE SYMPTOMS
# =========================================================

def get_disease_symptoms(disease):

    disease_symptoms = set(
        DISEASE_SYMPTOMS.get(
            disease,
            []
        )
    )

    disease_symptoms.update(
        EXTRA_DISEASE_SYMPTOMS.get(
            disease,
            set()
        )
    )

    return disease_symptoms


# =========================================================
# 10. TOTAL DETAIL SCORE
# =========================================================

def get_total_detail_score(disease):

    return patient_state[
        "detail_scores"
    ].get(
        disease,
        0
    )


# =========================================================
# 11. DISEASE SCORING
# =========================================================

def get_possible_diseases():

    present = patient_state[
        "present_symptoms"
    ]

    absent = patient_state[
        "absent_symptoms"
    ]

    results = []

    for disease in DISEASE_SYMPTOMS.keys():

        disease_symptoms = get_disease_symptoms(
            disease
        )

        # Positive matches
        present_matches = len(
            present.intersection(
                disease_symptoms
            )
        )

        # Absent matches
        absent_matches = len(
            absent.intersection(
                disease_symptoms
            )
        )

        # Disease penalties
        total_penalty = 0

        disease_rules = DISEASE_PENALTIES.get(
            disease,
            {}
        )

        for symptom, penalty in disease_rules.items():

            if symptom in absent:

                total_penalty += penalty

        # Detail score
        detail_score = get_total_detail_score(
            disease
        )

        # Conversational score
        score = (
            present_matches
            -
            total_penalty
            +
            detail_score
        )

        # Keep diseases supported
        # by at least one symptom.
        if present_matches > 0:

            results.append({

                "disease": disease,

                "score": score,

                "matches": present_matches,

                "absent_matches": absent_matches,

                "penalty": total_penalty,

                "detail_score": detail_score
            })

    results.sort(
        key=lambda x: (
            x["score"],
            x["detail_score"],
            x["matches"],
            -x["penalty"],
            -x["absent_matches"]
        ),
        reverse=True
    )

    return results


# =========================================================
# 12. SHOW POSSIBLE CONDITIONS
# =========================================================

def show_possible_diseases():

    diseases = get_possible_diseases()

    if not diseases:
        return

    print("\nPossible conditions:")

    for item in diseases[:4]:

        detail_text = ""

        if item["detail_score"] != 0:

            sign = (
                "+"
                if item["detail_score"] > 0
                else ""
            )

            detail_text = (
                f", detail evidence "
                f"{sign}{item['detail_score']}"
            )

        print(
            f"- {item['disease']} "
            f"({item['matches']} matching symptoms"
            f"{detail_text})"
        )


# =========================================================
# 13. QUESTION VALUE
# =========================================================

def question_value(
    symptom,
    candidates
):

    total_candidates = len(
        candidates
    )

    if total_candidates <= 1:
        return 0

    present_in = 0

    for candidate in candidates:

        disease = candidate["disease"]

        disease_symptoms = get_disease_symptoms(
            disease
        )

        if symptom in disease_symptoms:

            present_in += 1

    absent_in = (
        total_candidates
        -
        present_in
    )

    if present_in == 0 or absent_in == 0:
        return 0

    difference = abs(
        present_in - absent_in
    )

    return (
        total_candidates
        -
        difference
    )


# =========================================================
# 14. GET NEXT USEFUL QUESTION
# =========================================================

def get_next_question():

    candidates = get_possible_diseases()

    if len(candidates) <= 1:
        return None

    candidates = candidates[:4]

    answered = (
        patient_state["present_symptoms"]
        |
        patient_state["absent_symptoms"]
        |
        patient_state["asked_symptoms"]
    )

    fever_known = (

        "high_fever" in answered

        or

        "mild_fever" in answered

        or

        "low_fever" in answered
    )

    # -----------------------------------------------------
    # FIRST PRIORITY:
    # Disease-specific priority symptoms
    # -----------------------------------------------------

    priority_questions = []

    for candidate in candidates:

        disease = candidate["disease"]

        priority_symptoms = (
            DISEASE_PRIORITY_SYMPTOMS.get(
                disease,
                []
            )
        )

        for symptom in priority_symptoms:

            if symptom in BLOCKED_FOLLOW_UP_SYMPTOMS:
                continue

            if symptom in answered:
                continue

            if (
                fever_known
                and
                symptom in {
                    "high_fever",
                    "mild_fever",
                    "low_fever"
                }
            ):
                continue

            relevant = False

            for current_candidate in candidates:

                current_disease = (
                    current_candidate["disease"]
                )

                disease_symptoms = (
                    get_disease_symptoms(
                        current_disease
                    )
                )

                if symptom in disease_symptoms:

                    relevant = True

                    break

            if not relevant:
                continue

            priority_questions.append(
                (
                    symptom,
                    candidate["score"]
                )
            )

    if priority_questions:

        priority_questions.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return priority_questions[0][0]

    # -----------------------------------------------------
    # SECOND PRIORITY:
    # Information-value questions
    # -----------------------------------------------------

    possible_questions = set()

    for candidate in candidates:

        disease = candidate["disease"]

        disease_symptoms = get_disease_symptoms(
            disease
        )

        for symptom in disease_symptoms:

            if symptom in answered:
                continue

            if symptom in BLOCKED_FOLLOW_UP_SYMPTOMS:
                continue

            if (
                fever_known
                and
                symptom in {
                    "high_fever",
                    "mild_fever",
                    "low_fever"
                }
            ):
                continue

            possible_questions.add(
                symptom
            )

    scored = []

    for symptom in possible_questions:

        value = question_value(
            symptom,
            candidates
        )

        if value > 0:

            scored.append(
                (
                    symptom,
                    value
                )
            )

    if not scored:
        return None

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored[0][0]


# =========================================================
# 15. NATURAL QUESTION
# =========================================================

def make_question(symptom):

    if symptom in QUESTION_MAPPING:

        return QUESTION_MAPPING[
            symptom
        ]

    return None


# =========================================================
# 16. YES / NO UNDERSTANDING
# =========================================================

def understand_answer(message):

    message = message.lower().strip()

    yes_words = {

        "yes",
        "yeah",
        "yep",
        "yup",
        "sure",
        "yes i do",
        "yes i have",
        "i do",
        "i have",
        "correct",
        "true",
        "definitely",
        "sometimes"
    }

    no_words = {

        "no",
        "nope",
        "nah",
        "no i don't",
        "no i do not",
        "i don't",
        "i do not",
        "not really",
        "false",
        "never"
    }

    if message in yes_words:
        return "yes"

    if message in no_words:
        return "no"

    return "unknown"


# =========================================================
# 17. PROCESS FOLLOW-UP ANSWER
# =========================================================

def process_follow_up_answer(
    symptom,
    answer
):

    result = understand_answer(
        answer
    )

    if result == "yes":

        patient_state[
            "asked_symptoms"
        ].add(
            symptom
        )

        patient_state[
            "present_symptoms"
        ].add(
            symptom
        )

        patient_state[
            "absent_symptoms"
        ].discard(
            symptom
        )

        return True

    if result == "no":

        patient_state[
            "asked_symptoms"
        ].add(
            symptom
        )

        patient_state[
            "absent_symptoms"
        ].add(
            symptom
        )

        patient_state[
            "present_symptoms"
        ].discard(
            symptom
        )

        return True

    return False


# =========================================================
# 18. APPLY DETAIL CLUE
# =========================================================

def apply_detail_clue(
    disease,
    symptom,
    answer
):

    clue_score = get_detail_clue(
        disease,
        symptom,
        answer
    )

    if clue_score == 0:
        return 0

    detail_key = (
        disease,
        symptom
    )

    if detail_key in patient_state[
        "detail_score_keys"
    ]:
        return 0

    patient_state[
        "detail_score_keys"
    ].add(
        detail_key
    )

    current_score = (
        patient_state[
            "detail_scores"
        ].get(
            disease,
            0
        )
    )

    patient_state[
        "detail_scores"
    ][disease] = (
        current_score
        +
        clue_score
    )

    sign = (
        "+"
        if clue_score > 0
        else ""
    )

    print(
        f"\nDetail evidence detected for "
        f"{disease}: {sign}{clue_score}"
    )

    return clue_score


# =========================================================
# 19. DISEASE-SPECIFIC DETAIL QUESTION
# =========================================================

def ask_detail_question(
    disease,
    symptom
):

    detail_question = get_detail_question(
        disease,
        symptom
    )

    if not detail_question:
        return False

    detail_key = (
        disease,
        symptom
    )

    if detail_key in patient_state[
        "detail_questions_asked"
    ]:
        return False

    patient_state[
        "detail_questions_asked"
    ].add(
        detail_key
    )

    print(
        "\nBot:",
        detail_question
    )

    answer = input(
        "\nPatient: "
    ).strip()

    if not answer:
        return False

    patient_state[
        "patient_details"
    ][
        f"{disease}:{symptom}"
    ] = answer

    apply_detail_clue(
        disease,
        symptom,
        answer
    )

    patient_state[
        "conversation_history"
    ].append({

        "type": "detail",

        "disease": disease,

        "symptom": symptom,

        "question": detail_question,

        "answer": answer
    })

    print(
        "\nInformation recorded."
    )

    return True


# =========================================================
# 20. ASK RELEVANT DETAIL QUESTIONS
# =========================================================

def ask_relevant_detail_questions():

    candidates = get_possible_diseases()

    if not candidates:
        return False

    for candidate in candidates[:3]:

        disease = candidate["disease"]

        disease_questions = (
            DETAIL_QUESTIONS.get(
                disease,
                {}
            )
        )

        if not disease_questions:
            continue

        for symptom in disease_questions:

            if symptom not in patient_state[
                "present_symptoms"
            ]:
                continue

            detail_key = (
                disease,
                symptom
            )

            if detail_key in patient_state[
                "detail_questions_asked"
            ]:
                continue

            asked = ask_detail_question(
                disease,
                symptom
            )

            if asked:
                return True

    return False


# =========================================================
# 21. CREATE PATIENT DATAFRAME
# =========================================================

def make_patient_dataframe():

    try:

        from model import X_train

        columns = X_train.columns

    except ImportError:

        columns = list(
            SYMPTOM_MAPPING.keys()
        )

    patient = pd.DataFrame(
        0,
        index=[0],
        columns=columns
    )

    for symptom in patient_state[
        "present_symptoms"
    ]:

        if symptom in patient.columns:

            patient.loc[
                0,
                symptom
            ] = 1

    return patient


# =========================================================
# 22. FINAL ML PREDICTION
# =========================================================

def final_prediction():

    patient = make_patient_dataframe()

    try:

        from model import (
            rf_model,
            lr_model
        )

        # =================================================
        # LOGISTIC REGRESSION
        # =================================================

        lr_probabilities = (
            lr_model.predict_proba(
                patient
            )[0]
        )

        lr_classes = (
            lr_model.classes_
        )

        # =================================================
        # RANDOM FOREST
        # =================================================

        rf_probabilities = (
            rf_model.predict_proba(
                patient
            )[0]
        )

        rf_classes = (
            rf_model.classes_
        )

        # =================================================
        # LR + RF ENSEMBLE
        #
        # LR = 80%
        # RF = 20%
        #
        # DO NOT CHANGE THESE WEIGHTS
        # =================================================

        ml_scores = {}

        # -------------------------------------------------
        # LOGISTIC REGRESSION = 80%
        # -------------------------------------------------

        for disease, probability in zip(
            lr_classes,
            lr_probabilities
        ):

            ml_scores[disease] = (

                ml_scores.get(
                    disease,
                    0
                )

                +

                probability * 0.80
            )

        # -------------------------------------------------
        # RANDOM FOREST = 20%
        # -------------------------------------------------

        for disease, probability in zip(
            rf_classes,
            rf_probabilities
        ):

            ml_scores[disease] = (

                ml_scores.get(
                    disease,
                    0
                )

                +

                probability * 0.20
            )

        # =================================================
        # RULE-BASED CANDIDATES
        # =================================================

        rule_candidates = (
            get_possible_diseases()
        )

        rule_lookup = {}

        for candidate in rule_candidates:

            rule_lookup[
                candidate["disease"]
            ] = candidate

        # =================================================
        # COMBINE ML + CONVERSATIONAL EVIDENCE
        # =================================================

        ranked_candidates = []

        for disease, ml_probability in ml_scores.items():

            rule_score = 0

            matches = 0

            penalty = 0

            detail_score = 0

            # ---------------------------------------------
            # Conversational evidence
            # ---------------------------------------------

            if disease in rule_lookup:

                candidate = rule_lookup[
                    disease
                ]

                rule_score = candidate.get(
                    "score",
                    0
                )

                matches = candidate.get(
                    "matches",
                    0
                )

                penalty = candidate.get(
                    "penalty",
                    0
                )

                detail_score = candidate.get(
                    "detail_score",
                    0
                )

            # ---------------------------------------------
            # FINAL COMBINED SCORE
            #
            # ML remains the main prediction source.
            # LR/RF probabilities are NOT replaced.
            # ---------------------------------------------

            final_score = (

                ml_probability * 5

                +

                rule_score * 2

                +

                matches * 0.5

                -

                penalty * 0.5

                +

                detail_score * 0.5
            )

            ranked_candidates.append({

                "disease": disease,

                "ml_probability":
                    ml_probability,

                "rule_score":
                    rule_score,

                "matches":
                    matches,

                "penalty":
                    penalty,

                "detail_score":
                    detail_score,

                "final_score":
                    final_score
            })

        # =================================================
        # SORT ALL ML DISEASES
        #
        # IMPORTANT:
        # We DO NOT remove diseases which have no
        # rule-based evidence.
        #
        # Therefore alternatives can always come
        # from the complete LR + RF prediction.
        # =================================================

        ranked_candidates.sort(

            key=lambda x: (

                x["final_score"],

                x["ml_probability"],

                x["detail_score"],

                x["matches"],

                -x["penalty"]
            ),

            reverse=True
        )

        # =================================================
        # FINAL RANKING
        # =================================================

        ranked = [

            (

                item["disease"],

                item["final_score"],

                item["ml_probability"]

            )

            for item in ranked_candidates
        ]

        # =================================================
        # FINAL RESULT
        # =================================================

        print("\n")

        print(
            "========== PREDICTION =========="
        )

        if ranked:

            # =============================================
            # MOST LIKELY CONDITION
            # =============================================

            best_disease = ranked[0][0]

            print(
                "\nMost likely condition:",
                best_disease
            )

            # =============================================
            # OTHER POSSIBLE CONDITIONS
            #
            # ALWAYS TAKE THEM FROM THE COMPLETE
            # LR + RF RANKING.
            #
            # ranked[0] = most likely
            # ranked[1] = alternative 1
            # ranked[2] = alternative 2
            # =============================================

            print(
                "\nOther possible conditions:"
            )

            alternatives = ranked[1:3]

            if alternatives:

                for disease, score, probability in alternatives:

                    print(
                        f"- {disease}"
                    )

            else:

                print(
                    "- No additional likely conditions identified."
                )

        else:

            print(
                "\nUnable to determine "
                "a likely condition."
            )

        print(
            "================================"
        )

        # =================================================
        # DEBUG INFORMATION
        #
        # Shows the LR + RF ranking internally.
        # Useful during project testing.
        # =================================================

        print(
            "\nML ensemble ranking:"
        )

        for position, item in enumerate(
            ranked_candidates[:5],
            start=1
        ):

            print(

                f"{position}. "
                f"{item['disease']} "
                f"(ML probability: "
                f"{item['ml_probability']:.4f})"
            )

        # =================================================
        # RETURN COMPLETE RANKING
        # =================================================

        return ranked

    except Exception as error:

        print(
            "\nML Prediction error:",
            error
        )

        return []


# =========================================================
# 23. DISEASE INFORMATION
# =========================================================

def show_disease_information(disease):

    requested = (
        disease.strip().lower()
    )

    info = None

    matched_name = disease

    for name, details in DISEASE_INFO.items():

        if name.strip().lower() == requested:

            info = details

            matched_name = name

            break

    if info is None:

        print(
            "\nNo additional information "
            "available for this condition."
        )

        return

    print("\n")

    print(
        "========== DISEASE INFORMATION =========="
    )

    print("\nDisease:")

    print(
        matched_name
    )

    if isinstance(info, dict):

        if "overview" in info:

            print("\nOverview:")

            print(
                info["overview"]
            )

        if "tests" in info:

            print("\nTests:")

            print(
                info["tests"]
            )

        if "treatment" in info:

            print("\nTreatment:")

            print(
                info["treatment"]
            )

        if "when_to_seek" in info:

            print("\nWhen To Seek:")

            print(
                info["when_to_seek"]
            )

    print(
        "=========================================="
    )


# =========================================================
# 24. GENERIC FEVER HANDLING
# =========================================================

def handle_generic_fever(
    message,
    present,
    absent
):

    message_lower = message.lower()

    generic_fever = re.search(
        r"\bfever\b",
        message_lower
    )

    if not generic_fever:
        return True

    fever_levels = {
        "high_fever",
        "mild_fever",
        "low_fever"
    }

    if any(
        fever in present
        for fever in fever_levels
    ):
        return True

    if any(
        fever in absent
        for fever in fever_levels
    ):
        return True

    print(
        "\nBot: Is your fever high, mild, or low?"
    )

    fever_answer = input(
        "\nPatient: "
    ).strip().lower()

    # -----------------------------------------------------
    # HIGH FEVER
    # -----------------------------------------------------

    if re.search(
        r"\b(high|very high)\b",
        fever_answer
    ):

        present.append(
            "high_fever"
        )

        return True

    # -----------------------------------------------------
    # MILD FEVER
    # -----------------------------------------------------

    if re.search(
        r"\b(mild|slight|slightly)\b",
        fever_answer
    ):

        present.append(
            "mild_fever"
        )

        return True

    # -----------------------------------------------------
    # LOW FEVER
    # -----------------------------------------------------

    if re.search(
        r"\blow\b",
        fever_answer
    ):

        present.append(
            "low_fever"
        )

        return True

    print(
        "\nBot: Please tell me if your fever "
        "is high, mild, or low."
    )

    return False


# =========================================================
# 25. MAIN CHATBOT
# =========================================================

def run_chatbot():

    reset_patient_state()

    print(
        "\n================================"
    )

    print(
        "       DPREDICTO CHATBOT"
    )

    print(
        "================================"
    )

    print(
        "\nTell me what you are experiencing."
    )

    print(
        "You can describe multiple symptoms "
        "in one message."
    )

    # =====================================================
    # FIRST PATIENT MESSAGE
    # =====================================================

    while True:

        message = input(
            "\nPatient: "
        ).strip()

        if not message:
            continue

        # -------------------------------------------------
        # Extract symptoms
        # -------------------------------------------------

        present, absent = (
            extract_symptoms(
                message
            )
        )

        # -------------------------------------------------
        # Generic fever
        # -------------------------------------------------

        fever_ok = handle_generic_fever(
            message,
            present,
            absent
        )

        if not fever_ok:
            continue

        # -------------------------------------------------
        # Check symptoms
        # -------------------------------------------------

        if not present and not absent:

            print(
                "\nBot: I could not identify "
                "any symptoms from that message."
            )

            print(
                "Please describe what you are feeling."
            )

            continue

        # -------------------------------------------------
        # Update patient state
        # -------------------------------------------------

        update_patient_state(
            present,
            absent
        )

        # -------------------------------------------------
        # Save conversation
        # -------------------------------------------------

        patient_state[
            "conversation_history"
        ].append({

            "type": "patient",

            "patient": message,

            "present": present,

            "absent": absent
        })

        show_patient_state()

        break

    # =====================================================
    # ADAPTIVE FOLLOW-UP
    # =====================================================

    max_questions = 10

    questions_asked = 0

    while questions_asked < max_questions:

        candidates = (
            get_possible_diseases()
        )

        if not candidates:
            break

        # -------------------------------------------------
        # Show current possible conditions
        # -------------------------------------------------

        show_possible_diseases()

        # -------------------------------------------------
        # Disease-specific detail question
        # -------------------------------------------------

        detail_asked = (
            ask_relevant_detail_questions()
        )

        if detail_asked:

            print(
                "\nUpdated possible conditions:"
            )

            show_possible_diseases()

            continue

        # -------------------------------------------------
        # Get next useful symptom question
        # -------------------------------------------------

        next_symptom = (
            get_next_question()
        )

        if next_symptom is None:
            break

        # -------------------------------------------------
        # Convert symptom into natural question
        # -------------------------------------------------

        question = make_question(
            next_symptom
        )

        if question is None:

            patient_state[
                "asked_symptoms"
            ].add(
                next_symptom
            )

            continue

        # -------------------------------------------------
        # Ask question
        # -------------------------------------------------

        print(
            "\nBot:",
            question
        )

        answer = input(
            "\nPatient: "
        ).strip()

        # -------------------------------------------------
        # Process answer
        # -------------------------------------------------

        understood = (
            process_follow_up_answer(
                next_symptom,
                answer
            )
        )

        if not understood:

            print(
                "Bot: Please answer yes or no."
            )

            continue

        questions_asked += 1

        # -------------------------------------------------
        # Save conversation
        # -------------------------------------------------

        patient_state[
            "conversation_history"
        ].append({

            "type": "follow_up",

            "question": question,

            "answer": answer,

            "symptom": next_symptom
        })

        show_patient_state()

    # =====================================================
    # FINAL RESULT
    # =====================================================

    print(
        "\nI have collected enough information "
        "for an initial prediction."
    )

    possible = final_prediction()

    # =====================================================
    # DISEASE INFORMATION
    # =====================================================

    if possible:

        best_disease = possible[0][0]

        show_disease_information(
            best_disease
        )


# =========================================================
# START CHATBOT
# =========================================================

if __name__ == "__main__":

    run_chatbot()