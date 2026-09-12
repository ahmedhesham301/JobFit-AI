companies_blacklist = ["alignerr", "Uneeq Interns"]


levels_to_skip = [
    r"\blead\b",
    r"\bmanager\b",
    r"\bconsultor\b",
    r"\bconsultant\b",
    r"\bprincipal\b",
    r"\bprinciple\b",
    r"\bdirector",
    r"\bvice president\b",
    r"\bstaff\b",
    r"\bhead of\b",
    r"\bchief\b",
    r"\bdistinguished\b",
]

abbreviations_to_skip = [
    r"\bvp\b",
    r"\bsvp\b",
    r"\bavp\b",
]

unrelated_tech_to_skip = [
    r"\bdata engineer\b",
    r"\bdata scientist\b",
    r"\bmachine learning engineer\b",
    r"\bml engineer\b",
    r"\bai engineer\b",
    r"\bfrontend\b",
    r"\bfront-end\b",
    r"\bfullstack\b",
    r"\bfull-stack\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bmobile developer\b",
    r"\bmobile engineer\b",
    r"\bqa\b",
    r"\bsdet\b",
    r"\bquality assurance\b",
    r"\btest engineer\b",
    r"\btesting engineer\b",
    r"\bsalesforce\b",
    r"\bdynamics 365\b",
    r"\bservicenow\b",
    r"\bsap\b",
    r"\boracle fusion\b",
]

unrelated_non_tech_to_skip = [
    r"\bcivil engineer\b",
    r"\belectrical engineer\b",
    r"\bmechanical engineer\b",
    r"\bstructural engineer\b",
    r"\bpharmacy\b",
    r"\bpharmacist\b",
    r"\bpharm tech\b",
    r"\bsupply chain\b",
    r"\bpostdoctoral\b",
    r"\bCopywriting\b",
    r"\bsales\b",
    r"\bAccountant\b",
]

title_key_word_blacklist = [
    r"\blatin\b",
    r"\belixir\b",
]


all_title_skip = "|".join(
    levels_to_skip
    + abbreviations_to_skip
    + unrelated_tech_to_skip
    + unrelated_non_tech_to_skip,
).lower()


