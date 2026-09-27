import sys
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


import chatbot


class ChatbotBridge:

    # Maximum questions shown in one batch
    MAX_QUESTIONS = 10

    def __init__(self):
        self.started = False
        self.finished = False

        # Questions currently displayed on website
        self.current_questions = []


    # =========================================================
    # START NEW CONVERSATION
    # =========================================================

    def start(self):

        chatbot.reset_patient_state()

        self.started = True
        self.finished = False
        self.current_questions = []

        return {
            "success": True,

            "message":
                "Chatbot conversation started.",

            "reply": (
                "Tell me what you are experiencing. "
                "You can describe multiple symptoms in one message."
            ),

            "finished": False
        }


    # =========================================================
    # SAVE PATIENT MESSAGE
    # =========================================================

    def _save_patient_message(
        self,
        message,
        present,
        absent
    ):

        chatbot.patient_state[
            "conversation_history"
        ].append({

            "type": "patient",

            "patient": message,

            "present": present,

            "absent": absent
        })


    # =========================================================
    # CURRENT POSSIBLE CONDITIONS
    # =========================================================

    def _get_current_candidates(self):

        candidates = chatbot.get_possible_diseases()

        return [

            {
                "disease": item["disease"],
                "score": item["score"],
                "matches": item["matches"],
                "detail_score": item["detail_score"]
            }

            for item in candidates[:4]
        ]


    # =========================================================
    # CREATE QUESTION OBJECT
    # =========================================================

    def _make_question_object(
        self,
        question_id,
        question,
        question_type,
        input_type,
        options=None,
        symptom=None,
        disease=None
    ):

        item = {

            "id": question_id,

            "question": question,

            "question_type": question_type,

            "input_type": input_type
        }

        if options is not None:
            item["options"] = options

        if symptom is not None:
            item["symptom"] = symptom

        if disease is not None:
            item["disease"] = disease

        return item


    # =========================================================
    # BUILD GIANT QUESTION BATCH
    # =========================================================

    def _build_question_batch(self):

        questions = []

        used_symptoms = set()

        used_detail_questions = set()


        # =====================================================
        # CHECK FEVER
        # =====================================================

        answered_symptoms = (

            chatbot.patient_state[
                "present_symptoms"
            ]

            |

            chatbot.patient_state[
                "absent_symptoms"
            ]
        )

        fever_known = (

            "high_fever" in answered_symptoms

            or

            "mild_fever" in answered_symptoms

            or

            "low_fever" in answered_symptoms
        )


        # =====================================================
        # FEVER QUESTION
        # =====================================================

        if (

            "fever"
            in
            chatbot.patient_state[
                "conversation_history"
            ][-1].get(
                "patient",
                ""
            ).lower()

            if chatbot.patient_state[
                "conversation_history"
            ]

            else False
        ):

            if not fever_known:

                questions.append(

                    self._make_question_object(

                        "fever_level",

                        "Is your fever high, mild, or low?",

                        "fever",

                        "select",

                        [
                            "High",
                            "Mild",
                            "Low"
                        ],

                        symptom="fever"
                    )
                )


        # =====================================================
        # CURRENT DISEASE CANDIDATES
        # =====================================================

        candidates = chatbot.get_possible_diseases()

        if not candidates:
            return questions[:self.MAX_QUESTIONS]


        # =====================================================
        # DISEASE-SPECIFIC DETAIL QUESTIONS
        # =====================================================

        for candidate in candidates[:3]:

            if len(questions) >= self.MAX_QUESTIONS:
                break

            disease = candidate["disease"]

            disease_questions = chatbot.DETAIL_QUESTIONS.get(
                disease,
                {}
            )


            for symptom in disease_questions:

                if len(questions) >= self.MAX_QUESTIONS:
                    break


                # Only ask details for symptoms already reported
                if symptom not in chatbot.patient_state[
                    "present_symptoms"
                ]:
                    continue


                detail_key = (
                    disease,
                    symptom
                )


                if detail_key in chatbot.patient_state[
                    "detail_questions_asked"
                ]:
                    continue


                if detail_key in used_detail_questions:
                    continue


                question = chatbot.get_detail_question(
                    disease,
                    symptom
                )


                if not question:
                    continue


                used_detail_questions.add(
                    detail_key
                )


                questions.append(

                    self._make_question_object(

                        f"detail_{len(questions) + 1}",

                        question,

                        "detail",

                        "text",

                        symptom=symptom,

                        disease=disease
                    )
                )


        # =====================================================
        # NORMAL ADAPTIVE QUESTIONS
        # =====================================================

        while len(questions) < self.MAX_QUESTIONS:

            next_symptom = chatbot.get_next_question()


            if next_symptom is None:
                break


            if next_symptom in used_symptoms:
                break


            used_symptoms.add(
                next_symptom
            )


            question = chatbot.make_question(
                next_symptom
            )


            if question is None:

                chatbot.patient_state[
                    "asked_symptoms"
                ].add(
                    next_symptom
                )

                continue


            # -------------------------------------------------
            # NORMAL SYMPTOM QUESTION
            # -------------------------------------------------

            questions.append(

                self._make_question_object(

                    f"symptom_{len(questions) + 1}",

                    question,

                    "yes_no",

                    "yes_no",

                    [
                        "Yes",
                        "No"
                    ],

                    symptom=next_symptom
                )
            )


            # Temporarily mark it so get_next_question()
            # doesn't repeatedly return the same symptom.

            chatbot.patient_state[
                "asked_symptoms"
            ].add(
                next_symptom
            )


        # =====================================================
        # RETURN MAXIMUM 10
        # =====================================================

        return questions[:self.MAX_QUESTIONS]


    # =========================================================
    # QUESTION BATCH RESPONSE
    # =========================================================

    def _question_batch_response(self):

        questions = self._build_question_batch()

        self.current_questions = questions


        # -----------------------------------------------------
        # No questions left
        # -----------------------------------------------------

        if not questions:
            return self._prediction_response()


        return {

            "success": True,

            "reply": (
                "Please answer the following questions "
                "to help narrow down the possible conditions."
            ),

            "questions": questions,

            "question_count": len(questions),

            "max_questions": self.MAX_QUESTIONS,

            "finished": False,

            "possible_conditions":
                self._get_current_candidates()
        }


    # =========================================================
    # FINAL PREDICTION
    # =========================================================

    # =========================================================
# FINAL PREDICTION
# =========================================================

    def _prediction_response(self):

        ranked = chatbot.final_prediction()


        # -----------------------------------------------------
        # NO PREDICTION
        # -----------------------------------------------------

        if not ranked:

            self.finished = True
            self.current_questions = []

            return {

                "success": True,

                "reply": (
                    "I could not determine a likely "
                    "condition from the information provided."
                ),

                "finished": True,

                "prediction": None,

                "possible_conditions": [],

                "disease_information": {},

                "model_used":
                    "Logistic Regression + Random Forest",

                "model_weights": {

                    "logistic_regression":
                        0.80,

                    "random_forest":
                        0.20
                }
            }


        # -----------------------------------------------------
        # BEST DISEASE
        #
        # final_prediction() returns:
        #
        # (disease, final_score, ml_probability)
        # -----------------------------------------------------

        best_disease = ranked[0][0]


        # -----------------------------------------------------
        # OTHER POSSIBLE DISEASES
        #
        # ranked[1] = alternative 1
        # ranked[2] = alternative 2
        # ranked[3] = alternative 3
        #
        # We show the next 3.
        # -----------------------------------------------------

        other_conditions = []


        for disease, score, probability in ranked[1:4]:

            other_conditions.append({

                "disease":
                    disease,

                "score":
                    score,

                "ml_probability":
                    probability
            })


        # -----------------------------------------------------
        # DISEASE INFORMATION
        # -----------------------------------------------------

        info = chatbot.DISEASE_INFO.get(

            best_disease,

            {}
        )


        self.finished = True
        self.current_questions = []


        # -----------------------------------------------------
        # FINAL RESPONSE
        # -----------------------------------------------------

        return {

            "success": True,

            "reply": (
                "The assessment is complete. "
                "The following result is an educational "
                "machine-learning prediction."
            ),

            "finished": True,

            "prediction":
                best_disease,

            "possible_conditions":
                other_conditions,

            "disease_information":
                info,

            # -------------------------------------------------
            # KEEP YOUR LR + RF MODEL INFORMATION
            # -------------------------------------------------

            "model_used":
                "Logistic Regression + Random Forest",

            "model_weights": {

                "logistic_regression":
                    0.80,

                "random_forest":
                    0.20
            }
        }

    # =========================================================
    # PROCESS BATCH ANSWERS
    # =========================================================

    def send_batch_answers(
        self,
        answers
    ):

        if not self.started:
            self.start()


        if self.finished:

            return {

                "success": False,

                "reply": (
                    "This assessment has already finished. "
                    "Please start a new assessment."
                ),

                "finished": True
            }


        if not isinstance(
            answers,
            list
        ):

            return {

                "success": False,

                "reply":
                    "Answers must be provided as a list.",

                "finished": False
            }


        # -----------------------------------------------------
        # PROCESS EVERY QUESTION ANSWER
        # -----------------------------------------------------

        for answer_item in answers:

            question_id = answer_item.get(
                "question_id"
            )


            answer = str(

                answer_item.get(
                    "answer",
                    ""
                )

            ).strip()


            if not question_id or not answer:
                continue


            # Find question from current batch

            question_data = None


            for question in self.current_questions:

                if question["id"] == question_id:

                    question_data = question

                    break


            if question_data is None:
                continue


            # =================================================
            # FEVER
            # =================================================

            if question_data["question_type"] == "fever":

                text = answer.lower()


                if "high" in text:

                    fever = "high_fever"

                elif "mild" in text:

                    fever = "mild_fever"

                elif "low" in text:

                    fever = "low_fever"

                else:
                    continue


                chatbot.patient_state[
                    "present_symptoms"
                ].add(
                    fever
                )


                chatbot.patient_state[
                    "absent_symptoms"
                ].discard(
                    fever
                )


                chatbot.patient_state[
                    "conversation_history"
                ].append({

                    "type":
                        "fever",

                    "question":
                        question_data["question"],

                    "answer":
                        answer,

                    "symptom":
                        fever
                })


                continue


            # =================================================
            # DETAIL QUESTION
            # =================================================

            if question_data["question_type"] == "detail":

                disease = question_data.get(
                    "disease"
                )


                symptom = question_data.get(
                    "symptom"
                )


                if disease and symptom:

                    detail_key = (
                        disease,
                        symptom
                    )


                    chatbot.patient_state[
                        "patient_details"
                    ][
                        f"{disease}:{symptom}"
                    ] = answer


                    chatbot.apply_detail_clue(

                        disease,

                        symptom,

                        answer
                    )


                    chatbot.patient_state[
                        "conversation_history"
                    ].append({

                        "type":
                            "detail",

                        "disease":
                            disease,

                        "symptom":
                            symptom,

                        "question":
                            question_data["question"],

                        "answer":
                            answer
                    })


                continue


            # =================================================
            # YES / NO QUESTION
            # =================================================

            if question_data["question_type"] == "yes_no":

                symptom = question_data.get(
                    "symptom"
                )


                if not symptom:
                    continue


                answer_lower = answer.lower()


                if answer_lower in {

                    "yes",
                    "yeah",
                    "yep",
                    "yup",
                    "sure"
                }:

                    chatbot.patient_state[
                        "present_symptoms"
                    ].add(
                        symptom
                    )


                    chatbot.patient_state[
                        "absent_symptoms"
                    ].discard(
                        symptom
                    )


                elif answer_lower in {

                    "no",
                    "nope",
                    "nah"
                }:

                    chatbot.patient_state[
                        "absent_symptoms"
                    ].add(
                        symptom
                    )


                    chatbot.patient_state[
                        "present_symptoms"
                    ].discard(
                        symptom
                    )


                else:
                    continue


                chatbot.patient_state[
                    "asked_symptoms"
                ].add(
                    symptom
                )


                chatbot.patient_state[
                    "conversation_history"
                ].append({

                    "type":
                        "follow_up",

                    "question":
                        question_data["question"],

                    "answer":
                        answer,

                    "symptom":
                        symptom
                })


        # =====================================================
        # BATCH FINISHED
        # =====================================================

        self.current_questions = []


        return self._prediction_response()


    # =========================================================
    # SEND NORMAL MESSAGE
    # =========================================================

    def send_message(
        self,
        message
    ):

        if not self.started:
            self.start()


        if self.finished:

            return {

                "success": False,

                "reply": (
                    "This assessment has already finished. "
                    "Please start a new assessment."
                ),

                "finished": True
            }


        message = str(
            message
        ).strip()


        if not message:

            return {

                "success": False,

                "reply":
                    "Please enter your symptoms.",

                "finished": False
            }


        # -----------------------------------------------------
        # EXTRACT SYMPTOMS
        # -----------------------------------------------------

        present, absent = chatbot.extract_symptoms(
            message
        )


        # -----------------------------------------------------
        # NO SYMPTOMS FOUND
        # -----------------------------------------------------

        if not present and not absent:

            return {

                "success": True,

                "reply": (
                    "I could not identify symptoms from "
                    "your message. Please describe what "
                    "you are experiencing."
                ),

                "finished": False,

                "questions": []
            }


        # -----------------------------------------------------
        # SAVE SYMPTOMS
        # -----------------------------------------------------

        chatbot.update_patient_state(
            present,
            absent
        )


        self._save_patient_message(

            message,

            present,

            absent
        )


        # -----------------------------------------------------
        # BUILD QUESTION FORM
        # -----------------------------------------------------

        return self._question_batch_response()