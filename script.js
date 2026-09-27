const API_URL = "http://127.0.0.1:5000";



// =========================================================
// SESSION ID
// =========================================================

let userId = localStorage.getItem("dpredicto_user_id");

if (!userId) {

    userId =
        "user_" +
        Date.now() +
        "_" +
        Math.random()
            .toString(36)
            .substring(2, 9);

    localStorage.setItem(
        "dpredicto_user_id",
        userId
    );
}



// =========================================================
// ASSESSMENT FORM
// =========================================================

const assessmentForm =
    document.getElementById("assessment-form");

const nameInput =
    document.getElementById("name");

const ageInput =
    document.getElementById("age");

const sexInput =
    document.getElementById("sex");

const symptomsInput =
    document.getElementById("symptoms");

const durationInput =
    document.getElementById("duration");



// =========================================================
// PREDICTION ELEMENTS
// =========================================================

const diseaseName =
    document.getElementById("disease-name");

const mlModelName =
    document.getElementById("ml-model-name");

const diseaseOverview =
    document.getElementById("disease-overview");

const diseaseDiagnosis =
    document.getElementById("disease-diagnosis");

const diseaseTreatment =
    document.getElementById("disease-treatment");

const diseaseWarning =
    document.getElementById("disease-warning");

const diseaseSources =
    document.getElementById("disease-sources");



// =========================================================
// QUESTION AREA
// =========================================================

const questionArea =
    document.createElement("div");

questionArea.id =
    "chatbot-question-area";

questionArea.style.display =
    "none";

questionArea.style.marginTop =
    "40px";

assessmentForm.parentNode.insertBefore(
    questionArea,
    assessmentForm.nextSibling
);



// =========================================================
// QUESTION HEADING
// =========================================================

const questionHeading =
    document.createElement("h2");

questionHeading.textContent =
    "Follow-up Questions";

questionHeading.style.marginBottom =
    "10px";



// =========================================================
// QUESTION INTRO
// =========================================================

const questionIntro =
    document.createElement("p");

questionIntro.textContent =
    "Answer these questions to help narrow down the possible conditions.";

questionIntro.style.marginBottom =
    "25px";



// =========================================================
// QUESTION LIST
// =========================================================

const questionList =
    document.createElement("div");

questionList.id =
    "question-list";



// =========================================================
// SUBMIT BUTTON
// =========================================================

const submitAnswersButton =
    document.createElement("button");

submitAnswersButton.type =
    "button";

submitAnswersButton.textContent =
    "Submit Answers";

submitAnswersButton.className =
    "submit-assessment-btn";

submitAnswersButton.style.marginTop =
    "25px";



// =========================================================
// ADD QUESTION ELEMENTS
// =========================================================

questionArea.appendChild(
    questionHeading
);

questionArea.appendChild(
    questionIntro
);

questionArea.appendChild(
    questionList
);

questionArea.appendChild(
    submitAnswersButton
);



// =========================================================
// ASSESSMENT SUBMISSION
// =========================================================

assessmentForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // -------------------------------------------------
        // GET VALUES
        // -------------------------------------------------

        const name =
            nameInput.value.trim();

        const age =
            ageInput.value.trim();

        const sex =
            sexInput.value.trim();

        const symptoms =
            symptomsInput.value.trim();

        const duration =
            durationInput.value.trim();


        // -------------------------------------------------
        // VALIDATION
        // -------------------------------------------------

        if (!name) {

            alert("Please enter your name.");

            nameInput.focus();

            return;
        }


        if (!age) {

            alert("Please enter your age.");

            ageInput.focus();

            return;
        }


        if (!sex) {

            alert("Please select your sex.");

            sexInput.focus();

            return;
        }


        if (!symptoms) {

            alert("Please describe your symptoms.");

            symptomsInput.focus();

            return;
        }


        if (!duration) {

            alert(
                "Please enter the duration of your symptoms."
            );

            durationInput.focus();

            return;
        }


        // -------------------------------------------------
        // LOADING
        // -------------------------------------------------

        const submitButton =
            assessmentForm.querySelector(
                "button[type='submit']"
            );

        const originalText =
            submitButton
                ? submitButton.textContent
                : "Submit Assessment";


        if (submitButton) {

            submitButton.disabled =
                true;

            submitButton.textContent =
                "Analyzing Symptoms...";
        }


        try {

            // =============================================
            // START CHAT
            // =============================================

            const startResponse =
                await fetch(
                    `${API_URL}/api/chat/start`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            user_id: userId
                        })
                    }
                );


            if (!startResponse.ok) {

                throw new Error(
                    "Unable to start chatbot."
                );
            }


            await startResponse.json();


            // =============================================
            // SEND INITIAL PATIENT INFORMATION
            // =============================================

            const symptomMessage =
                `I am ${age} years old and ${sex}. ` +
                `My symptoms are: ${symptoms}. ` +
                `I have had these symptoms for ${duration}.`;


            console.log(
                "Sending patient information:",
                symptomMessage
            );


            const messageResponse =
                await fetch(
                    `${API_URL}/api/chat/message`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            user_id: userId,
                            message: symptomMessage
                        })
                    }
                );


            if (!messageResponse.ok) {

                throw new Error(
                    "Unable to communicate with chatbot."
                );
            }


            const result =
                await messageResponse.json();


            console.log(
                "Chatbot response:",
                result
            );


            // =============================================
            // HANDLE RESPONSE
            // =============================================

            handleChatbotResponse(result);

        }

        catch (error) {

            console.error(
                "Chatbot error:",
                error
            );


            alert(
                "Unable to connect to the DPredicto chatbot.\n\n" +
                "Please make sure Flask is running on port 5000."
            );
        }

        finally {

            if (submitButton) {

                submitButton.disabled =
                    false;

                submitButton.textContent =
                    originalText;
            }
        }
    }
);



// =========================================================
// HANDLE CHATBOT RESPONSE
// =========================================================

function handleChatbotResponse(result) {

    console.log(
        "Processing chatbot response:",
        result
    );


    // -----------------------------------------------------
    // FINAL PREDICTION
    // -----------------------------------------------------

    if (
        result.finished === true &&
        result.prediction
    ) {

        displayPrediction(result);

        return;
    }


    // -----------------------------------------------------
    // QUESTION BATCH
    // -----------------------------------------------------

    if (
        result.questions &&
        result.questions.length > 0
    ) {

        displayQuestions(
            result.questions
        );

        return;
    }


    // -----------------------------------------------------
    // SINGLE QUESTION
    // -----------------------------------------------------

    if (result.question) {

        displayQuestions([
            {
                id:
                    result.question_id ||
                    "question_1",

                question:
                    result.question,

                input_type:
                    result.input_type ||
                    "text",

                options:
                    result.options ||
                    []
            }
        ]);

        return;
    }


    // -----------------------------------------------------
    // NORMAL REPLY
    // -----------------------------------------------------

    if (result.reply) {

        alert(
            result.reply
        );
    }
}



// =========================================================
// DISPLAY QUESTION BATCH
// =========================================================

function displayQuestions(questions) {

    // -----------------------------------------------------
    // SHOW AREA
    // -----------------------------------------------------

    questionArea.style.display =
        "block";


    // -----------------------------------------------------
    // CLEAR OLD QUESTIONS
    // -----------------------------------------------------

    questionList.innerHTML =
        "";


    // -----------------------------------------------------
    // QUESTION COUNT
    // -----------------------------------------------------

    questionIntro.textContent =
        `Please answer these ${questions.length} questions. ` +
        "The questions are selected based on your symptoms.";


    // -----------------------------------------------------
    // CREATE QUESTIONS
    // -----------------------------------------------------

    questions.forEach(
        function (item, index) {

            const questionCard =
                document.createElement("div");

            questionCard.className =
                "chatbot-question-card";


            // -------------------------------------------------
            // CARD STYLE
            // -------------------------------------------------

            questionCard.style.marginBottom =
                "25px";

            questionCard.style.padding =
                "24px";

            questionCard.style.border =
                "1px solid #dfe8df";

            questionCard.style.borderRadius =
                "16px";

            questionCard.style.background =
                "#ffffff";


            // -------------------------------------------------
            // QUESTION NUMBER
            // -------------------------------------------------

            const number =
                document.createElement("div");

            number.textContent =
                `Question ${index + 1}`;

            number.style.fontWeight =
                "700";

            number.style.marginBottom =
                "12px";


            // -------------------------------------------------
            // QUESTION TEXT
            // -------------------------------------------------

            const questionText =
                document.createElement("p");

            questionText.textContent =
                item.question;

            questionText.style.fontSize =
                "18px";

            questionText.style.fontWeight =
                "500";

            questionText.style.marginBottom =
                "18px";


            // -------------------------------------------------
            // ANSWER CONTAINER
            // -------------------------------------------------

            const answerContainer =
                document.createElement("div");

            answerContainer.className =
                "answer-container";


            // =================================================
            // SELECT QUESTION
            // =================================================

            if (
                item.input_type === "select"
            ) {

                const select =
                    document.createElement("select");

                select.className =
                    "chatbot-answer";

                select.dataset.questionId =
                    item.id || index;


                select.style.width =
                    "100%";

                select.style.padding =
                    "12px";

                select.style.borderRadius =
                    "8px";

                select.style.border =
                    "1px solid #ccc";

                select.style.fontSize =
                    "16px";


                // DEFAULT OPTION

                const defaultOption =
                    document.createElement("option");

                defaultOption.value =
                    "";

                defaultOption.textContent =
                    "Select your answer";

                defaultOption.disabled =
                    true;

                defaultOption.selected =
                    true;


                select.appendChild(
                    defaultOption
                );


                // OPTIONS

                if (
                    item.options &&
                    item.options.length > 0
                ) {

                    item.options.forEach(
                        function (option) {

                            const optionElement =
                                document.createElement(
                                    "option"
                                );

                            optionElement.value =
                                option;

                            optionElement.textContent =
                                option;

                            select.appendChild(
                                optionElement
                            );
                        }
                    );
                }


                answerContainer.appendChild(
                    select
                );
            }


            // =================================================
            // YES / NO QUESTION
            // =================================================

            else if (
                item.input_type === "yes_no"
            ) {

                const select =
                    document.createElement("select");

                select.className =
                    "chatbot-answer";

                select.dataset.questionId =
                    item.id || index;


                select.style.width =
                    "100%";

                select.style.padding =
                    "12px";

                select.style.borderRadius =
                    "8px";

                select.style.border =
                    "1px solid #ccc";

                select.style.fontSize =
                    "16px";


                // DEFAULT

                const defaultOption =
                    document.createElement("option");

                defaultOption.value =
                    "";

                defaultOption.textContent =
                    "Select your answer";

                defaultOption.disabled =
                    true;

                defaultOption.selected =
                    true;


                select.appendChild(
                    defaultOption
                );


                // YES

                const yesOption =
                    document.createElement("option");

                yesOption.value =
                    "Yes";

                yesOption.textContent =
                    "Yes";


                // NO

                const noOption =
                    document.createElement("option");

                noOption.value =
                    "No";

                noOption.textContent =
                    "No";


                select.appendChild(
                    yesOption
                );

                select.appendChild(
                    noOption
                );


                answerContainer.appendChild(
                    select
                );
            }


            // =================================================
            // TEXT QUESTION
            // =================================================

            else {

                const input =
                    document.createElement("input");

                input.type =
                    "text";

                input.className =
                    "chatbot-answer";

                input.dataset.questionId =
                    item.id || index;

                input.placeholder =
                    "Type your answer";


                input.style.width =
                    "100%";

                input.style.padding =
                    "12px";

                input.style.borderRadius =
                    "8px";

                input.style.border =
                    "1px solid #ccc";

                input.style.fontSize =
                    "16px";


                answerContainer.appendChild(
                    input
                );
            }


            // =================================================
            // ADD QUESTION CARD
            // =================================================

            questionCard.appendChild(
                number
            );

            questionCard.appendChild(
                questionText
            );

            questionCard.appendChild(
                answerContainer
            );


            questionList.appendChild(
                questionCard
            );
        }
    );


    // -----------------------------------------------------
    // SCROLL
    // -----------------------------------------------------

    questionArea.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}



// =========================================================
// SUBMIT ALL ANSWERS
// =========================================================

submitAnswersButton.addEventListener(
    "click",
    async function () {

        const answerElements =
            document.querySelectorAll(
                ".chatbot-answer"
            );


        const answers = [];


        // -------------------------------------------------
        // COLLECT ANSWERS
        // -------------------------------------------------

        for (
            let i = 0;
            i < answerElements.length;
            i++
        ) {

            const element =
                answerElements[i];

            const answer =
                element.value.trim();


            if (!answer) {

                alert(
                    `Please answer question ${i + 1}.`
                );

                element.focus();

                return;
            }


            answers.push({

                question_id:
                    element.dataset.questionId,

                answer:
                    answer
            });
        }


        // -------------------------------------------------
        // LOADING
        // -------------------------------------------------

        submitAnswersButton.disabled =
            true;

        submitAnswersButton.textContent =
            "Analyzing Answers...";


        try {

            // =============================================
            // SEND ANSWERS TO FLASK
            // =============================================

            const response =
                await fetch(
                    `${API_URL}/api/chat/answers`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            user_id:
                                userId,

                            answers:
                                answers
                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Server returned ${response.status}`
                );
            }


            const result =
                await response.json();


            console.log(
                "Answer response:",
                result
            );


            // =============================================
            // HANDLE NEXT STEP
            // =============================================

            handleChatbotResponse(result);

        }

        catch (error) {

            console.error(
                "Answer submission error:",
                error
            );


            alert(
                "Unable to submit your answers.\n\n" +
                "Please make sure the Flask server is running."
            );
        }

        finally {

            submitAnswersButton.disabled =
                false;

            submitAnswersButton.textContent =
                "Submit Answers";
        }
    }
);



// =========================================================
// DISPLAY FINAL PREDICTION
// =========================================================

function displayPrediction(result) {

    // -----------------------------------------------------
    // PREDICTED DISEASE
    // -----------------------------------------------------

    const predictedDisease =
        result.prediction ||
        "Prediction unavailable";


    diseaseName.textContent =
        predictedDisease;


    // -----------------------------------------------------
    // MODEL NAME
    // -----------------------------------------------------

    mlModelName.textContent =
        "Logistic Regression + Random Forest (80% / 20%)";


    // -----------------------------------------------------
    // DISEASE INFORMATION
    // -----------------------------------------------------

    const info =
        result.disease_information ||
        {};


    diseaseOverview.textContent =
        getInformation(
            info,
            [
                "overview",
                "description"
            ],
            "Disease information is not available."
        );


    diseaseDiagnosis.textContent =
        getInformation(
            info,
            [
                "diagnosis",
                "tests"
            ],
            "Diagnostic information is not available."
        );


    diseaseTreatment.textContent =
        getInformation(
            info,
            [
                "treatment",
                "treatment_options"
            ],
            "Treatment information is not available."
        );


    diseaseWarning.textContent =
        getInformation(
            info,
            [
                "warning",
                "when_to_seek_medical_attention",
                "red_flags",
                "when_to_seek"
            ],
            "Please consult a qualified healthcare professional for medical advice."
        );


    diseaseSources.textContent =
        getInformation(
            info,
            [
                "sources",
                "references"
            ],
            "Please consult reliable medical sources or a healthcare professional."
        );


    // =====================================================
    // SHOW OTHER POSSIBLE CONDITIONS
    // =====================================================

    displayOtherConditions(
        result.possible_conditions || []
    );


    // -----------------------------------------------------
    // HIDE QUESTIONS
    // -----------------------------------------------------

    questionArea.style.display =
        "none";


    // -----------------------------------------------------
    // SCROLL TO PREDICTION
    // -----------------------------------------------------

    const predictionSection =
        document.getElementById(
            "prediction"
        );


    if (predictionSection) {

        predictionSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}



// =========================================================
// OTHER POSSIBLE CONDITIONS
// =========================================================

function displayOtherConditions(conditions) {

    let container =
        document.getElementById(
            "other-possible-conditions"
        );


    // -----------------------------------------------------
    // CREATE CONTAINER
    // -----------------------------------------------------

    if (!container) {

        container =
            document.createElement("div");

        container.id =
            "other-possible-conditions";


        const predictionSection =
            document.getElementById(
                "prediction"
            );


        if (predictionSection) {

            predictionSection.appendChild(
                container
            );
        }
    }


    // -----------------------------------------------------
    // CONTAINER STYLE
    // -----------------------------------------------------

    container.style.marginTop =
        "30px";

    container.style.fontFamily =
        "inherit";

    container.style.width =
        "100%";


    // -----------------------------------------------------
    // CLEAR OLD CONTENT
    // -----------------------------------------------------

    container.innerHTML =
        "";


    // -----------------------------------------------------
    // HEADING
    // -----------------------------------------------------

    const heading =
        document.createElement("h3");

    heading.textContent =
        "Other Possible Conditions";

    heading.style.fontSize =
        "20px";

    heading.style.fontWeight =
        "700";

    heading.style.marginBottom =
        "10px";

    heading.style.fontFamily =
        "inherit";


    container.appendChild(
        heading
    );


    // -----------------------------------------------------
    // DESCRIPTION
    // -----------------------------------------------------

    const description =
        document.createElement("p");

    description.textContent =
        "These are alternative conditions that may share similar symptoms. The result is not a confirmed medical diagnosis.";

    description.style.fontSize =
        "15px";

    description.style.lineHeight =
        "1.6";

    description.style.marginBottom =
        "20px";

    description.style.fontFamily =
        "inherit";


    container.appendChild(
        description
    );


    // -----------------------------------------------------
    // NO CONDITIONS
    // -----------------------------------------------------

    if (!conditions.length) {

        const text =
            document.createElement("p");

        text.textContent =
            "No additional conditions were identified.";

        text.style.fontSize =
            "16px";

        text.style.fontFamily =
            "inherit";


        container.appendChild(
            text
        );

        return;
    }


    // -----------------------------------------------------
    // CONDITIONS
    // -----------------------------------------------------

    conditions.forEach(
        function (item, index) {

            const disease =
                typeof item === "string"
                    ? item
                    : item.disease;


            if (!disease) {
                return;
            }


            // =================================================
            // CONDITION CARD
            // =================================================

            const card =
                document.createElement("div");

            card.className =
                "possible-condition-card";


            // -------------------------------------------------
            // CARD STYLE
            // -------------------------------------------------

            card.style.boxSizing =
                "border-box";

            card.style.width =
                "100%";

            card.style.padding =
                "18px 20px";

            card.style.marginBottom =
                "12px";

            card.style.border =
                "1px solid #dfe8df";

            card.style.borderRadius =
                "12px";

            card.style.background =
                "#ffffff";

            card.style.fontFamily =
                "inherit";


            // -------------------------------------------------
            // CONDITION NUMBER
            // -------------------------------------------------

            const number =
                document.createElement("span");

            number.textContent =
                `Alternative ${index + 1}`;

            number.style.display =
                "block";

            number.style.fontSize =
                "13px";

            number.style.fontWeight =
                "600";

            number.style.marginBottom =
                "5px";

            number.style.fontFamily =
                "inherit";


            // -------------------------------------------------
            // DISEASE NAME
            // -------------------------------------------------

            const name =
                document.createElement("strong");

            name.textContent =
                disease;

            name.style.display =
                "block";

            name.style.fontSize =
                "17px";

            name.style.fontWeight =
                "600";

            name.style.lineHeight =
                "1.5";

            name.style.fontFamily =
                "inherit";


            // -------------------------------------------------
            // ADD TO CARD
            // -------------------------------------------------

            card.appendChild(
                number
            );

            card.appendChild(
                name
            );


            // -------------------------------------------------
            // ADD CARD TO CONTAINER
            // -------------------------------------------------

            container.appendChild(
                card
            );
        }
    );
}



// =========================================================
// INFORMATION HELPER
// =========================================================

function getInformation(
    information,
    possibleKeys,
    fallback
) {

    for (
        const key of possibleKeys
    ) {

        if (
            information[key] !== undefined &&
            information[key] !== null &&
            information[key] !== ""
        ) {

            if (
                Array.isArray(
                    information[key]
                )
            ) {

                return information[key]
                    .join(", ");
            }


            return String(
                information[key]
            );
        }
    }


    return fallback;
}



// =========================================================
// NAVIGATION
// =========================================================

document.querySelectorAll(
    ".nav-links a"
).forEach(
    function (link) {

        link.addEventListener(
            "click",
            function (event) {

                event.preventDefault();


                const targetId =
                    this.getAttribute(
                        "href"
                    );


                const target =
                    document.querySelector(
                        targetId
                    );


                if (target) {

                    target.scrollIntoView({
                        behavior:
                            "smooth"
                    });
                }
            }
        );
    }
);



// =========================================================
// HERO BUTTONS
// =========================================================

document.querySelectorAll(
    ".hero-buttons a"
).forEach(
    function (button) {

        button.addEventListener(
            "click",
            function (event) {

                event.preventDefault();


                const targetId =
                    this.getAttribute(
                        "href"
                    );


                const target =
                    document.querySelector(
                        targetId
                    );


                if (target) {

                    target.scrollIntoView({
                        behavior:
                            "smooth"
                    });
                }
            }
        );
    }
);



// =========================================================
// INITIAL PAGE SETUP
// =========================================================

window.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "DPredicto frontend loaded."
        );


        console.log(
            "Flask backend:",
            API_URL
        );


        console.log(
            "User session:",
            userId
        );
    }
);