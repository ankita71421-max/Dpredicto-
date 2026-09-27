# =========================================================
# 1. DISEASE PENALTIES
# =========================================================

DISEASE_PENALTIES = {

    # -----------------------------------------------------
    # Chicken pox
    # -----------------------------------------------------
    "Chicken pox": {
        "skin_rash": 5,
        "red_spots_over_body": 4,
        "blister": 4,
    },

    # -----------------------------------------------------
    # Tuberculosis
    # -----------------------------------------------------
    "Tuberculosis": {
        "cough": 4,
        "phlegm": 3,
        "weight_loss": 2,
        "blood_in_sputum": 5,
    },

    # -----------------------------------------------------
    # Typhoid
    # -----------------------------------------------------
    "Typhoid": {
        "abdominal_pain": 3,
        "belly_pain": 3,
    },

    # -----------------------------------------------------
    # Malaria
    # -----------------------------------------------------
    "Malaria": {
        "chills": 3,
    },

    # -----------------------------------------------------
    # Dengue
    # -----------------------------------------------------
    "Dengue": {
        "pain_behind_the_eyes": 3,
        "muscle_pain": 2,
        "joint_pain": 2,
    },

    # -----------------------------------------------------
    # Pneumonia
    # -----------------------------------------------------
    "Pneumonia": {
        "cough": 4,
        "breathlessness": 4,
        "chest_pain": 2,
    },

    # -----------------------------------------------------
    # Heart attack
    # -----------------------------------------------------
    "Heart attack": {
        "chest_pain": 5,
        "breathlessness": 4,
    },

    # -----------------------------------------------------
    # UTI
    # -----------------------------------------------------
    "Urinary tract infection": {
        "burning_micturition": 5,
        "bladder_discomfort": 4,
    },

    # -----------------------------------------------------
    # Jaundice
    # -----------------------------------------------------
    "Jaundice": {
        "yellowish_skin": 5,
        "yellowing_of_eyes": 5,
        "dark_urine": 3,
    },

    # -----------------------------------------------------
    # GERD
    # -----------------------------------------------------
    "GERD": {
        "acidity": 4,
        "stomach_pain": 3,
    },

    # -----------------------------------------------------
    # Gastroenteritis
    # -----------------------------------------------------
    "Gastroenteritis": {
        "diarrhoea": 4,
        "dehydration": 3,
        "vomiting": 2,
    },

    # -----------------------------------------------------
    # Acne
    # -----------------------------------------------------
    "Acne": {
        "pus_filled_pimples": 5,
        "blackheads": 5,
        "scurring": 4,
    },

    # -----------------------------------------------------
    # Psoriasis
    # -----------------------------------------------------
    "Psoriasis": {
        "skin_peeling": 4,
        "silver_like_dusting": 5,
        "small_dents_in_nails": 4,
    },

    # -----------------------------------------------------
    # Impetigo
    # -----------------------------------------------------
    "Impetigo": {
        "blister": 4,
        "red_sore_around_nose": 5,
        "yellow_crust_ooze": 5,
    },

    # -----------------------------------------------------
    # AIDS
    # -----------------------------------------------------
    "AIDS": {
        "patches_in_throat": 5,
        "extra_marital_contacts": 5,
        "muscle_wasting": 4,
        "high_fever": 2,
    },

    # -----------------------------------------------------
    # Hypothyroidism
    # -----------------------------------------------------
    "Hypothyroidism": {
        "weight_gain": 3,
        "cold_hands_and_feets": 3,
        "enlarged_thyroid": 4,
    },

    # -----------------------------------------------------
    # Hyperthyroidism
    # -----------------------------------------------------
    "Hyperthyroidism": {
        "weight_loss": 3,
        "sweating": 3,
        "fast_heart_rate": 4,
    },

    # -----------------------------------------------------
    # Varicose veins
    # -----------------------------------------------------
    "Varicose veins": {
        "swollen_blood_vessels": 4,
        "prominent_veins_on_calf": 5,
    },

    # -----------------------------------------------------
    # Osteoarthritis
    # -----------------------------------------------------
    "Osteoarthristis": {
        "knee_pain": 4,
        "hip_joint_pain": 4,
        "painful_walking": 3,
    },

    # -----------------------------------------------------
    # Arthritis
    # -----------------------------------------------------
    "Arthritis": {
        "swelling_joints": 3,
        "movement_stiffness": 4,
        "painful_walking": 3,
    },
}


# =========================================================
# 2. DETAIL QUESTIONS
# =========================================================
#
# These questions are asked AFTER a symptom is confirmed.
#
# Their answers are NOT automatically symptoms.
# They provide additional disease-specific evidence.
#


DETAIL_QUESTIONS = {

    # -----------------------------------------------------
    # Tuberculosis
    # -----------------------------------------------------
    "Tuberculosis": {

        "cough": (
            "How long have you had the cough? "
            "Please tell me approximately how many "
            "days or weeks."
        ),

        "weight_loss": (
            "Have you had noticeable or unexplained "
            "weight loss recently?"
        ),
    },


    # -----------------------------------------------------
    # Typhoid
    # -----------------------------------------------------
    "Typhoid": {

        "abdominal_pain": (
            "How long have you had the abdominal pain?"
        ),

        "belly_pain": (
            "How long have you had the belly pain?"
        ),
    },


    # -----------------------------------------------------
    # Dengue
    # -----------------------------------------------------
    "Dengue": {

        "pain_behind_the_eyes": (
            "Have you had pain behind your eyes, "
            "especially when moving them?"
        ),

        "muscle_pain": (
            "Is the muscle pain widespread or severe?"
        ),
    },


    # -----------------------------------------------------
    # Malaria
    # -----------------------------------------------------
    "Malaria": {

        "chills": (
            "Do the chills or shivering occur around "
            "the time your fever rises?"
        ),
    },


    # -----------------------------------------------------
    # AIDS
    # -----------------------------------------------------
    "AIDS": {

        "patches_in_throat": (
            "How long have you noticed white patches "
            "or sores in your throat or mouth?"
        ),

        "extra_marital_contacts": (
            "Have you had recent high-risk exposures "
            "or unprotected sexual contact?"
        ),

        "muscle_wasting": (
            "Have you experienced severe unexplained "
            "muscle loss or drastic weight loss?"
        ),
    },


    # -----------------------------------------------------
    # Chicken pox
    # -----------------------------------------------------
    "Chicken pox": {

        "skin_rash": (
            "When did the skin rash first appear?"
        ),

        "red_spots_over_body": (
            "When did the red spots first appear?"
        ),

        "blister": (
            "Are the blisters filled with fluid?"
        ),
    },
}


# =========================================================
# 3. DETAIL CLUES
# =========================================================
#
# These are the IMPORTANT changes.
#
# A detail answer can now give additional evidence
# FOR or AGAINST a disease.
#
# Format:
#
# disease -> symptom -> answer -> score
#
# Positive score = supports disease
# Negative score = weakens disease
#
# =========================================================

DETAIL_CLUES = {

    # -----------------------------------------------------
    # Chicken pox
    # -----------------------------------------------------
    "Chicken pox": {

        "blister": {

            "yes": 5,
            "no": -5,
        },

        "skin_rash": {

            # A recent rash is more useful than
            # simply knowing that rash exists.
            "recent": 2,
        },

        "red_spots_over_body": {

            "yes": 2,
            "no": -2,
        },
    },


    # -----------------------------------------------------
    # Dengue
    # -----------------------------------------------------
    "Dengue": {

        "pain_behind_the_eyes": {

            "yes": 4,
            "no": -3,
        },

        "muscle_pain": {

            "yes": 4,
            "no": -2,
        },
    },


    # -----------------------------------------------------
    # Malaria
    # -----------------------------------------------------
    "Malaria": {

        "chills": {

            "yes": 4,
            "no": -3,
        },
    },


    # -----------------------------------------------------
    # Tuberculosis
    # -----------------------------------------------------
    "Tuberculosis": {

        "weight_loss": {

            "yes": 3,
            "no": -2,
        },
    },


    # -----------------------------------------------------
    # AIDS
    # -----------------------------------------------------
    "AIDS": {

        "muscle_wasting": {

            "yes": 4,
            "no": -2,
        },

        "extra_marital_contacts": {

            "yes": 5,
            "no": -5,
        },
    },
}


# =========================================================
# 4. GET PENALTY
# =========================================================

def get_penalty(disease, symptom):

    disease_rules = DISEASE_PENALTIES.get(
        disease,
        {}
    )

    return disease_rules.get(
        symptom,
        0
    )


# =========================================================
# 5. GET DETAIL QUESTION
# =========================================================

def get_detail_question(disease, symptom):

    disease_questions = DETAIL_QUESTIONS.get(
        disease,
        {}
    )

    return disease_questions.get(
        symptom
    )


# =========================================================
# 6. GET DETAIL CLUE
# =========================================================

def get_detail_clue(disease, symptom, answer):

    disease_clues = DETAIL_CLUES.get(
        disease,
        {}
    )

    symptom_clues = disease_clues.get(
        symptom,
        {}
    )

    answer = answer.lower().strip()

    # -----------------------------------------------------
    # Direct yes/no answer
    # -----------------------------------------------------

    if answer in symptom_clues:
        return symptom_clues[answer]

    # -----------------------------------------------------
    # Handle common yes answers
    # -----------------------------------------------------

    yes_words = {
        "yes",
        "yeah",
        "yep",
        "yup",
        "sure",
        "i do",
        "i have",
        "correct",
        "true",
        "definitely"
    }

    no_words = {
        "no",
        "nope",
        "nah",
        "never",
        "false",
        "not really",
        "i don't",
        "i do not"
    }

    if answer in yes_words:
        return symptom_clues.get(
            "yes",
            0
        )

    if answer in no_words:
        return symptom_clues.get(
            "no",
            0
        )

    # -----------------------------------------------------
    # Special handling for time/history answers
    # -----------------------------------------------------

    if symptom in {
        "skin_rash",
        "red_spots_over_body"
    }:

        if any(
            word in answer
            for word in [
                "today",
                "yesterday",
                "1 day",
                "2 day",
                "3 day",
                "recent",
                "recently"
            ]
        ):
            return symptom_clues.get(
                "recent",
                0
            )

    return 0