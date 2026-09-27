# symptom_mapping.py
# Complete mapping for the exact symptom features in Training.csv.
# Target column (prognosis) and CSV artifact (Unnamed: 133) are excluded.

# Exact symptom feature count: 132

SYMPTOM_MAPPING = {
    'itching': [
        'itching',
        'itchy',
        'itch',
    ],
    'skin_rash': [
        'skin rash',
        'rash',
        'rashes',
    ],
    'nodal_skin_eruptions': [
        'nodal skin eruptions',
        'skin nodules',
        'nodules on skin',
    ],
    'continuous_sneezing': [
        'continuous sneezing',
        'constant sneezing',
        'sneezing continuously',
        'sneezing a lot',
        'sneezing'
    ],
    'shivering': [
        'shivering',
        'shivering badly',
        'shaking',
    ],
    'chills': [
        'chills',
        'chill',
        'cold chills',
    ],
    'joint_pain': [
        'joint pain',
        'pain in my joints',
        'aching joints',
        'joints hurt',
    ],
    'stomach_pain': [
        'stomach pain',
        'stomach ache',
        'stomachache',
        'pain in my stomach',
    ],
    'acidity': [
        'acidity',
        'acid reflux',
        'heartburn',
        'burning after eating',
    ],
    'ulcers_on_tongue': [
        'ulcers on tongue',
        'tongue ulcers',
        'sores on tongue',
        'I have tongue on my tongue',
        'I have pain on tongue'
    ],
    'muscle_wasting': [
        'muscle wasting',
        'muscle loss',
        'loss of muscle',
    ],
    'vomiting': [
        'vomiting',
        'throwing up',
        'throw up',
        'threw up',
    ],
    'burning_micturition': [
        'burning while urinating',
        'burning when I pee',
        'burning urination',
        'pain while urinating',
    ],
    'spotting_ urination': [
        'spotting in urine',
        'spotting while urinating',
        'blood spotting in urine',
    ],
    'fatigue': [
        'fatigue',
        'tired',
        'very tired',
        'tiredness',
        'exhausted',
    ],
    'weight_gain': [
        'weight gain',
        'gaining weight',
        'gained weight',
    ],
    'anxiety': [
        'anxiety',
        'anxious',
        'feeling anxious',
        'nervousness',
    ],
    'cold_hands_and_feets': [
        'cold hands and feet',
        'cold hands',
        'cold feet',
        'hands and feet feel cold',
    ],
    'mood_swings': [
        'mood swings',
        'mood changes',
        'changing moods',
    ],
    'weight_loss': [
        'weight loss',
        'losing weight',
        'lost weight',
        'unexplained weight loss',
    ],
    'restlessness': [
        'restlessness',
        'restless',
        'feeling restless',
    ],
    'lethargy': [
        'lethargy',
        'lethargic',
        'sluggish',
        'very low energy',
    ],
    'patches_in_throat': [
        'patches in throat',
        'white patches in throat',
        'spots in throat',
    ],
    'irregular_sugar_level': [
        'irregular sugar level',
        'abnormal blood sugar',
        'blood sugar fluctuations',
    ],
    'cough': [
        'cough',
        'coughing',
        'dry cough',
        'persistent cough',
    ],
    'high_fever': [
        'high fever',
        'very high fever',
        'high temperature',
        
    ],
    'sunken_eyes': [
        'sunken eyes',
        'eyes look sunken',
    ],
    'breathlessness': [
        'breathlessness',
        'shortness of breath',
        'difficulty breathing',
        'trouble breathing',
    ],
    'sweating': [
        'sweating',
        'excessive sweating',
        'unusual sweating',
    ],
    'dehydration': [
        'dehydration',
        'dehydrated',
        'lack of fluids',
    ],
    'indigestion': [
        'indigestion',
        'difficulty digesting',
        'upset stomach after eating',
    ],
    'headache': [
        'headache',
        'head ache',
        'pain in my head',
        'my head hurts',
    ],
    'yellowish_skin': [
        'yellowish skin',
        'yellow skin',
        'skin looks yellow',
        'yellowing skin',
    ],
    'dark_urine': [
        'dark urine',
        'dark pee',
        'urine is dark',
        'brown urine',
    ],
    'nausea': [
        'nausea',
        'feeling nauseous',
        'feel nauseous',
        'sick to my stomach',
    ],
    'loss_of_appetite': [
        'loss of appetite',
        'no appetite',
        'poor appetite',
        "don't feel like eating",
    ],
    'pain_behind_the_eyes': [
        'pain behind the eyes',
        'pain behind my eyes',
        'eye pain behind the eyes',
    ],
    'back_pain': [
        'back pain',
        'backache',
        'pain in my back',
    ],
    'constipation': [
        'constipation',
        'constipated',
        'hard stool',
        'difficulty passing stool',
    ],
    'abdominal_pain': [
        'abdominal pain',
        'pain in abdomen',
        'pain in my abdomen',
        'pain is my upper abdomen'
    ],
    'diarrhoea': [
        'diarrhoea',
        'diarrhea',
        'loose motion',
        'loose motions',
        'watery stool',
    ],
    'mild_fever': [
        'mild fever',
        'slight fever',
        'low fever',
        'slightly feverish',
        
    ],
    'yellow_urine': [
        'yellow urine',
        'yellow pee',
        'urine is yellow',
    ],
    'yellowing_of_eyes': [
        'yellowing of eyes',
        'yellow eyes',
        'eyes look yellow',
    ],
    'acute_liver_failure': [
        'acute liver failure',
        'liver failure',
    ],
    'fluid_overload': [
        'fluid overload',
        'too much fluid in body',
        'excess fluid',
    ],
    'swelling_of_stomach': [
        'swelling of stomach',
        'swollen stomach',
        'stomach swelling',
    ],
    'swelled_lymph_nodes': [
        'swollen lymph nodes',
        'swelled lymph nodes',
        'enlarged lymph nodes',
    ],
    'malaise': [
        'malaise',
        'feeling unwell',
        'generally unwell',
        'not feeling well',
    ],
    'blurred_and_distorted_vision': [
        'blurred vision',
        'blurry vision',
        'distorted vision',
        'vision is blurry',
    ],
    'phlegm': [
        'phlegm',
        'mucus',
        'mucus in throat',
        'mucous',
        'mucous in throat'
    ],
    'throat_irritation': [
        'throat irritation',
        'irritated throat',
        'scratchy throat',
    ],
    'redness_of_eyes': [
        'red eyes',
        'redness of eyes',
        'eyes are red',
        'bloodshot eyes',
    ],
    'sinus_pressure': [
        'sinus pressure',
        'pressure in sinuses',
        'sinus pain',
        'pressure around my nose',
    ],
    'runny_nose': [
        'runny nose',
        'running nose',
        'nose is running',
        'watery nose',
    ],
    'congestion': [
        'congestion',
        'blocked nose',
        'stuffy nose',
        'nasal congestion',
    ],
    'chest_pain': [
        'chest pain',
        'pain in my chest',
        'chest hurts',
    ],
    'weakness_in_limbs': [
        'weakness in limbs',
        'weak arms and legs',
        'weakness in arms',
        'weakness in legs',
    ],
    'fast_heart_rate': [
        'fast heart rate',
        'heart beating fast',
        'rapid heartbeat',
        'heart is racing',
    ],
    'pain_during_bowel_movements': [
        'pain during bowel movements',
        'pain when passing stool',
        'pain while passing stool',
    ],
    'pain_in_anal_region': [
        'pain in anal region',
        'anal pain',
        'pain around anus',
    ],
    'bloody_stool': [
        'bloody stool',
        'blood in stool',
        'blood when passing stool',
        'stool with blood',
    ],
    'irritation_in_anus': [
        'irritation in anus',
        'anal irritation',
        'irritation around anus',
    ],
    'neck_pain': [
        'neck pain',
        'pain in neck',
        'neck hurts',
    ],
    'dizziness': [
        'dizziness',
        'dizzy',
        'feeling dizzy',
        'lightheaded',
    ],
    'cramps': [
        'cramps',
        'muscle cramps',
        'stomach cramps',
    ],
    'bruising': [
        'bruising',
        'bruises',
        'easy bruising',
        'bruises easily',
    ],
    'obesity': [
        'obesity',
        'obese',
    ],
    'swollen_legs': [
        'swollen legs',
        'legs are swollen',
        'swelling in legs',
    ],
    'swollen_blood_vessels': [
        'swollen blood vessels',
        'enlarged blood vessels',
    ],
    'puffy_face_and_eyes': [
        'puffy face',
        'puffy eyes',
        'swollen face',
        'swollen eyes',
    ],
    'enlarged_thyroid': [
        'enlarged thyroid',
        'swollen thyroid',
        'thyroid is enlarged',
    ],
    'brittle_nails': [
        'brittle nails',
        'weak nails',
        'nails break easily',
    ],
    'swollen_extremeties': [
        'swollen extremities',
        'swollen hands and feet',
        'swollen arms and legs',
    ],
    'excessive_hunger': [
        'excessive hunger',
        'very hungry',
        'extreme hunger',
        'always hungry',
    ],
    'extra_marital_contacts': [
        'extra marital contacts',
        'sexual contact outside marriage',
    ],
    'drying_and_tingling_lips': [
        'dry lips',
        'tingling lips',
        'dry and tingling lips',
    ],
    'slurred_speech': [
        'slurred speech',
        'speech is slurred',
        'difficulty speaking clearly',
    ],
    'knee_pain': [
        'knee pain',
        'pain in knee',
        'knees hurt',
    ],
    'hip_joint_pain': [
        'hip joint pain',
        'hip pain',
        'pain in hip',
    ],
    'muscle_weakness': [
        'muscle weakness',
        'weak muscles',
        'muscles feel weak',
    ],
    'stiff_neck': [
        'stiff neck',
        'neck stiffness',
        'neck feels stiff',
    ],
    'swelling_joints': [
        'swollen joints',
        'swelling in joints',
        'joints are swollen',
    ],
    'movement_stiffness': [
        'movement stiffness',
        'stiffness while moving',
        'difficulty moving because of stiffness',
    ],
    'spinning_movements': [
        'spinning sensation',
        'room is spinning',
        'everything is spinning',
    ],
    'loss_of_balance': [
        'loss of balance',
        'losing my balance',
        'balance problems',
    ],
    'unsteadiness': [
        'unsteadiness',
        'unsteady',
        'feeling unsteady',
        'walking unsteadily',
    ],
    'weakness_of_one_body_side': [
        'weakness on one side',
        'one side of body is weak',
        'weakness on one side of my body',
    ],
    'loss_of_smell': [
        'loss of smell',
        "can't smell",
        'cannot smell',
        'lost my sense of smell',
    ],
    'bladder_discomfort': [
        'bladder discomfort',
        'bladder pain',
        'discomfort in bladder',
    ],
    'foul_smell_of urine': [
        'foul smelling urine',
        'bad smelling urine',
        'strong smelling urine',
        'urine smells bad',
    ],
    'continuous_feel_of_urine': [
        'constant urge to urinate',
        'constant urge to pee',
        'always feel like urinating',
        'frequent urge to pee',
    ],
    'passage_of_gases': [
        'passing gas',
        'excessive gas',
        'too much gas',
        'gas',
    ],
    'internal_itching': [
        'internal itching',
        'itching inside',
        'itching from inside',
    ],
    'toxic_look_(typhos)': [
        'toxic appearance',
        'very ill appearance',
        'looks seriously ill',
    ],
    'depression': [
        'depression',
        'feeling depressed',
        'depressed mood',
        'feeling very low',
    ],
    'irritability': [
        'irritability',
        'irritable',
        'easily irritated',
    ],
    'muscle_pain': [
        'muscle pain',
        'muscle ache',
        'muscle aches',
        'aching muscles',
        'body aches',
    ],
    'altered_sensorium': [
        'altered sensorium',
        'confusion',
        'confused',
        'change in consciousness',
        'not thinking clearly',
    ],
    'red_spots_over_body': [
        'red spots over body',
        'red spots on my body',
        'red spots',
        'red marks on body',
    ],
    'belly_pain': [
        'belly pain',
        'pain in my belly',
        'belly ache',
    ],
    'abnormal_menstruation': [
        'abnormal menstruation',
        'irregular periods',
        'irregular menstruation',
        'periods are irregular',
    ],
    'dischromic _patches': [
        'discolored patches',
        'discoloured patches',
        'dark patches on skin',
        'skin discoloration',
    ],
    'watering_from_eyes': [
        'watering eyes',
        'watery eyes',
        'eyes watering',
        'teary eyes',
    ],
    'increased_appetite': [
        'increased appetite',
        'increased hunger',
        'eating more than usual',
    ],
    'polyuria': [
        'frequent urination',
        'urinating frequently',
        'peeing frequently',
        'urinating a lot',
    ],
    'family_history': [
        'family history',
        'disease runs in my family',
        'family medical history',
    ],
    'mucoid_sputum': [
        'mucoid sputum',
        'mucus sputum',
        'mucus when coughing',
        'clear mucus when coughing',
    ],
    'rusty_sputum': [
        'rusty sputum',
        'rust colored sputum',
        'rust coloured sputum',
        'brownish sputum',
    ],
    'lack_of_concentration': [
        'lack of concentration',
        'difficulty concentrating',
        "can't concentrate",
        'poor concentration',
    ],
    'visual_disturbances': [
        'visual disturbances',
        'vision problems',
        'visual problems',
        'disturbances in vision',
    ],
    'receiving_blood_transfusion': [
        'received blood transfusion',
        'blood transfusion',
        'had a blood transfusion',
    ],
    'receiving_unsterile_injections': [
        'received unsterile injections',
        'unsterile injection',
        'unsafe injection',
    ],
    'coma': [
        'coma',
        'unconscious',
        'unconsciousness',
    ],
    'stomach_bleeding': [
        'stomach bleeding',
        'bleeding in stomach',
        'blood in stomach',
    ],
    'distention_of_abdomen': [
        'abdominal distention',
        'distended abdomen',
        'swollen abdomen',
        'bloated abdomen',
    ],
    'history_of_alcohol_consumption': [
        'history of alcohol consumption',
        'history of drinking alcohol',
        'regular alcohol consumption',
        'alcohol use',
    ],
    'fluid_overload.1': [
        'fluid overload',
        'too much fluid in body',
        'excess fluid in body',
    ],
    'blood_in_sputum': [
        'blood in sputum',
        'blood when coughing',
        'coughing blood',
        'blood in mucus',
    ],
    'prominent_veins_on_calf': [
        'prominent veins on calf',
        'visible veins on calf',
        'bulging veins on calf',
    ],
    'palpitations': [
        'palpitations',
        'heart palpitations',
        'heart pounding',
        'feeling my heartbeat',
    ],
    'painful_walking': [
        'painful walking',
        'walking is painful',
        'pain when walking',
        'walking hurts',
    ],
    'pus_filled_pimples': [
        'pus filled pimples',
        'pus-filled pimples',
        'pimples with pus',
        'pus pimples',
    ],
    'blackheads': [
        'blackheads',
        'black heads',
    ],
    'scurring': [
        'scurring',
        'scarring',
        'skin scars',
    ],
    'skin_peeling': [
        'skin peeling',
        'peeling skin',
        'skin is peeling',
    ],
    'silver_like_dusting': [
        'silver like dusting',
        'silvery dusting on skin',
        'silver scales on skin',
    ],
    'small_dents_in_nails': [
        'small dents in nails',
        'tiny dents in nails',
        'pits in nails',
        'nail pits',
    ],
    'inflammatory_nails': [
        'inflammatory nails',
        'inflamed nails',
        'inflammation of nails',
    ],
    'blister': [
        'blister',
        'blisters',
        'skin blisters',
    ],
    'red_sore_around_nose': [
        'red sore around nose',
        'red sore near nose',
        'sore around my nose',
    ],
    'yellow_crust_ooze': [
        'yellow crust',
        'yellow crust on skin',
        'yellow ooze',
        'yellow discharge from skin',
    ],
    'fever': [
        'fever',
        'temperature',
        'feverish',
],
}

# Verification: 132 exact symptom features are represented.
