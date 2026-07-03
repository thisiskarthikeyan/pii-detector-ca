"""Clinical note templates with named PII slots.

Each template is a list of segments. A segment is either literal text or a
slot tuple ("SLOT", entity_type). The assembler fills slots via the
generators in pii_generators.py and records exact character spans, so the
corpus is span-labeled by construction — no post-hoc annotation.

Slot types used across locales: PERSON, DATE, ADDRESS plus the
locale-specific identifier entities.
"""

CLINICAL_FINDINGS = [
    "Lungs are clear bilaterally with no focal consolidation, effusion, or "
    "pneumothorax. Cardiomediastinal silhouette is within normal limits.",
    "There is a 6 mm ground-glass nodule in the right upper lobe, unchanged "
    "from the prior examination. No new pulmonary nodules identified.",
    "Mild degenerative changes of the lumbar spine with disc height loss at "
    "L4-L5. No acute fracture or subluxation.",
    "The liver is normal in size and echotexture. No focal hepatic lesion. "
    "Gallbladder is unremarkable without cholelithiasis.",
    "Post-contrast images demonstrate no abnormal enhancement. Ventricles "
    "and sulci are age-appropriate. No acute infarct or hemorrhage.",
    "Moderate hepatomegaly with diffuse fatty infiltration. Spleen and "
    "pancreas are unremarkable. No free fluid.",
    "There is a stable 2.3 cm simple cyst in the lower pole of the left "
    "kidney. No hydronephrosis or calculus.",
]

IMPRESSIONS = [
    "No acute cardiopulmonary abnormality.",
    "Stable pulmonary nodule; recommend follow-up CT in 12 months.",
    "Degenerative spondylosis without acute osseous abnormality.",
    "Fatty liver; clinical correlation recommended.",
    "No acute intracranial abnormality.",
    "Stable renal cyst, Bosniak I; no follow-up required.",
]

DIAGNOSES = [
    "type 2 diabetes mellitus", "essential hypertension", "community-acquired pneumonia",
    "chronic kidney disease stage 3", "hypothyroidism", "coronary artery disease",
    "acute gastroenteritis", "iron deficiency anemia",
]

MEDICATIONS = [
    "metformin 500 mg twice daily", "amlodipine 5 mg once daily",
    "atorvastatin 20 mg at bedtime", "levothyroxine 50 mcg every morning",
    "pantoprazole 40 mg before breakfast",
]


def radiology_report_ca(hospital):
    return [
        f"{hospital}\nDEPARTMENT OF DIAGNOSTIC IMAGING\n\n",
        "Patient: ", ("SLOT", "PERSON"), "\n",
        "Health card: ", ("SLOT", "HEALTH_ID"), "\n",
        "DOB: ", ("SLOT", "DATE"), "\n",
        "Exam date: ", ("SLOT", "DATE"), "\n",
        "Referring physician: Dr. ", ("SLOT", "PERSON"), "\n\n",
        "CLINICAL HISTORY: ", ("SLOT", "CLINICAL"), "\n\n",
        "FINDINGS: ", ("SLOT", "FINDINGS"), "\n\n",
        "IMPRESSION: ", ("SLOT", "IMPRESSION"), "\n",
    ]


def discharge_summary_ca(hospital):
    return [
        f"{hospital} — DISCHARGE SUMMARY\n\n",
        "Name: ", ("SLOT", "PERSON"), "\n",
        "SIN (billing): ", ("SLOT", "CA_SIN"), "\n",
        "Health number: ", ("SLOT", "HEALTH_ID"), "\n",
        "Address: ", ("SLOT", "ADDRESS"), "\n",
        "Admitted: ", ("SLOT", "DATE"), "   Discharged: ", ("SLOT", "DATE"), "\n\n",
        "Primary diagnosis: ", ("SLOT", "DIAGNOSIS"), ".\n",
        "The patient was admitted with the above and improved with treatment. ",
        "Discharge medications include ", ("SLOT", "MEDICATION"), ". ",
        "Follow-up with the family physician in two weeks.\n",
    ]


def referral_letter_ca(hospital):
    return [
        "Dear colleague,\n\n",
        "Re: ", ("SLOT", "PERSON"), " (health card ", ("SLOT", "HEALTH_ID"), ")\n\n",
        "Thank you for seeing this patient, residing at ", ("SLOT", "ADDRESS"),
        ", regarding ", ("SLOT", "DIAGNOSIS"), ". ",
        "Imaging performed on ", ("SLOT", "DATE"), " showed: ", ("SLOT", "FINDINGS"), "\n\n",
        "Sincerely,\nDr. ", ("SLOT", "PERSON"), f"\n{hospital}\n",
    ]


def ed_triage_note_ca(hospital):
    return [
        f"{hospital} — EMERGENCY DEPARTMENT TRIAGE RECORD\n\n",
        "Arrival: ", ("SLOT", "DATE"), "   CTAS level 3\n",
        "Patient: ", ("SLOT", "PERSON"), "   Health card: ", ("SLOT", "HEALTH_ID"), "\n",
        "Home address: ", ("SLOT", "ADDRESS"), "\n\n",
        "Presenting complaint: ", ("SLOT", "CLINICAL"), "\n",
        "Triage vitals stable. Assigned to acute bed; reassessment in 30 minutes.\n",
    ]


def consult_note_ca(hospital):
    # PII embedded in running prose rather than labelled header lines —
    # deliberately harder for both NER and context-word boosting.
    return [
        f"{hospital} — INTERNAL MEDICINE CONSULTATION\n\n",
        "I was asked to see ", ("SLOT", "PERSON"), " on ", ("SLOT", "DATE"),
        " regarding ", ("SLOT", "DIAGNOSIS"),
        ". The patient's health card number ", ("SLOT", "HEALTH_ID"),
        " was confirmed at registration.\n\n",
        "ASSESSMENT: ", ("SLOT", "FINDINGS"), "\n\n",
        "PLAN: Started on ", ("SLOT", "MEDICATION"),
        ". Will follow during admission.\n\n",
        "Dictated by Dr. ", ("SLOT", "PERSON"), "\n",
    ]


def lab_requisition_ca(hospital):
    return [
        f"{hospital} — OUTPATIENT LABORATORY REQUISITION\n\n",
        "Patient: ", ("SLOT", "PERSON"), "\n",
        "DOB: ", ("SLOT", "DATE"), "\n",
        "Health number: ", ("SLOT", "HEALTH_ID"), "\n",
        "SIN (third-party billing): ", ("SLOT", "CA_SIN"), "\n",
        "Mailing address: ", ("SLOT", "ADDRESS"), "\n\n",
        "Tests ordered: CBC, electrolytes, creatinine, HbA1c.\n",
        "Ordering physician: Dr. ", ("SLOT", "PERSON"), "\n",
    ]


def radiology_report_in(hospital):
    return [
        f"{hospital}\nRADIOLOGY REPORT\n\n",
        "Patient name: ", ("SLOT", "PERSON"), "\n",
        "UHID: ", ("SLOT", "IN_UHID"), "\n",
        "ABHA no: ", ("SLOT", "IN_ABHA"), "\n",
        "Study date: ", ("SLOT", "DATE"), "\n",
        "Referred by: Dr. ", ("SLOT", "PERSON"), "\n\n",
        "CLINICAL DETAILS: ", ("SLOT", "CLINICAL"), "\n\n",
        "OBSERVATIONS: ", ("SLOT", "FINDINGS"), "\n\n",
        "IMPRESSION: ", ("SLOT", "IMPRESSION"), "\n",
    ]


def discharge_summary_in(hospital):
    return [
        f"{hospital} — DISCHARGE SUMMARY\n\n",
        "Patient: ", ("SLOT", "PERSON"), "  (UHID ", ("SLOT", "IN_UHID"), ")\n",
        "Aadhaar: ", ("SLOT", "IN_AADHAAR"), "\n",
        "Mobile: ", ("SLOT", "IN_MOBILE"), "\n",
        "Address: ", ("SLOT", "ADDRESS"), "\n",
        "Date of admission: ", ("SLOT", "DATE"), "   Date of discharge: ", ("SLOT", "DATE"), "\n\n",
        "Final diagnosis: ", ("SLOT", "DIAGNOSIS"), ".\n",
        "Hospital course was uneventful. Discharged on ", ("SLOT", "MEDICATION"), ". ",
        "Review in OPD after 14 days; bring this summary and ID proof (",
        ("SLOT", "ID_PROOF"), ").\n",
    ]


def referral_letter_in(hospital):
    return [
        "Dear Doctor,\n\n",
        "Re: ", ("SLOT", "PERSON"), ", ABHA ", ("SLOT", "IN_ABHA"), "\n\n",
        "I am referring this patient (contact ", ("SLOT", "IN_MOBILE"),
        ", PAN on record ", ("SLOT", "IN_PAN"), " for insurance) for further ",
        "management of ", ("SLOT", "DIAGNOSIS"), ". ",
        "Recent imaging dated ", ("SLOT", "DATE"), " demonstrated: ", ("SLOT", "FINDINGS"), "\n\n",
        "With regards,\nDr. ", ("SLOT", "PERSON"), f"\n{hospital}\n",
    ]


TEMPLATES = {
    "ca": [
        radiology_report_ca,
        discharge_summary_ca,
        referral_letter_ca,
        ed_triage_note_ca,
        consult_note_ca,
        lab_requisition_ca,
    ],
    "in": [radiology_report_in, discharge_summary_in, referral_letter_in],
}
