#model = "gpt-3.5-turbo-0125"
#model="gpt-4o"
#model="meta-llama/llama-3-8b",
#model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"
standard_model = "gpt-3.5-turbo-0125"

config_file ="./config/config.yaml"
prompts_file="./config/prompts.yaml"
db_conn_file='./config/db_config.yaml'
action_file='./config/action.yaml'

default_mode = "serial"
default_page = "demo"
default_model_family = "openai"
default_model = "gpt-4o"
default_usecase = "demo"
default_temperature=0.1
default_run_mode = "same-llm"
default_run_count = 1
default_sleep = 0.75
default_accuracy_check = "ON"
default_encoding = "cl100k_base"
default_fuzzy_matching_threshold = 80
default_negative_prompt="ON"
default_formatter = "ros_pe_formatter"
default_use_for_training = False
default_error_detection = True
 

summary = """ <div>
  <h2>Patient Summary</h2>

  <p><strong>Patient ID:</strong> 12345</p>

  <h3>Vital Signs</h3>
  <ul>
    <li>Temperature: 36.8°C (normal)</li>
    <li>Heart Rate: 83 bpm (normal)</li>
    <li>Blood Pressure: 100/85 mmHg (slightly low)</li>
    <li>Respiratory Rate: 16 breaths/min (normal)</li>
    <li>Oxygen Saturation: 95% (normal)</li>
  </ul>

  <h3>Allergies</h3>
  <ul>
    <li>Aspirin</li>
    <li>Milk</li>
    <li>Wheat</li>
  </ul>

  <h3>Immunizations</h3>
  <ul>
    <li>Shingles (2022-12-24)</li>
    <li>Varicella (2023-08-03)</li>
    <li>HPV (2022-09-24)</li>
  </ul>

  <h3>Medications</h3>
  <ul>
    <li>Lisinopril 20 mg, once daily (prescribed on 2024-04-14)</li>
    <li>Amlodipine 20 mg, three times daily (prescribed on 2024-04-11)</li>
    <li>Metformin 5 mg, once daily (prescribed on 2024-03-20)</li>
  </ul>

  <h3>Lab Results</h3>
  <ul>
    <li>Urinalysis (2023-11-18): 0.55 U/L (within normal range)</li>
    <li>Comprehensive Metabolic Panel (2023-12-04): 1.44 mg/dL (normal)</li>
    <li>Thyroid Function Tests (2024-06-10): 1.81 U/L (normal)</li>
  </ul>

  <h3>Procedures</h3>
  <ul>
    <li>Tonsillectomy performed on 2022-04-03 by Dr. Cynthia Gomez</li>
  </ul>

  <h3>Appointments</h3>
  <ul>
    <li>Follow-up on 2024-09-13 at 10:30 AM with Loretta Reed</li>
  </ul>

  <h3>SOAP Note</h3>
  <p><strong>Chief Complaint:</strong> Persistent nausea, no vomiting</p>
  <p><strong>History of Present Illness:</strong> Acute stabbing pain, worsened by movement, relieved by medication, present for the past day</p>

  <h4>Review of Systems</h4>
  <ul>
    <li>Tinnitus, nasal congestion, shortness of breath, cough, wheezing, dysuria, urgency</li>
  </ul>

  <h4>Physical Exam</h4>
  <ul>
    <li>General: Distressed</li>
    <li>HEENT: Mild erythema, oropharynx clear</li>
    <li>Neck: Thyromegaly</li>
    <li>Chest: Rhonchi, wheezes</li>
    <li>Cardiovascular: Murmur, S4 gallop</li>
    <li>Abdomen: Distended</li>
    <li>Musculoskeletal: Deformity present</li>
    <li>Neurological: Alert and oriented, CN II-XII intact</li>
    <li>Skin: No rashes</li>
  </ul>

  <h3>Messages</h3>
  <p>Various messages regarding referrals, health questions, and prescription refill requests on 2024-09-12.</p>
</div>
"""


INSERT_QUERY = """
        INSERT INTO Run_stats (
            usecase,
            functionality,
            llm,
            llm_parameters,
            isBaseline,
            run_no,
            system_prompt,
            user_prompt,
            response,
            ideal_response,
            execution_time,
            matches_baseline,
            matches_ideal,
            difference,
            ideal_response_difference,
            mode,
            similarity_metric,
            run_date,
            use_for_training

        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
READ_QUERY = """
        SELECT 
            run_no,
            execution_time,
            usecase,
            functionality,
            isbaseline,
            matches_baseline,
            matches_ideal,
            difference,
            ideal_response_difference,
            response 
        FROM Run_stats
        """
