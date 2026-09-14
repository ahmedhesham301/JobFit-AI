companies_blacklist = [r"\balignerr\b", r"\bUneeq Interns\b"]

description_blockers = [
    # US work authorization
    r"\b(?:legally )?authorized to work .*?\b(?:u\.?s\.?|united states)\b",
    r"\b(?:u\.?s\.?|united states) work authorization\b",
    # Citizenship requirements
    r"\bu\.?s\.? citizenship required\b",
    r"\bmust be (?:a )?u\.?s\.? citizen\b",
    r"\bmust have (?:u\.?s\.?|united states) citizenship\b",
    # Visa sponsorship
    r"\b(?:will|does|do) not sponsor\b",
    r"\bunable to sponsor\b",
    r"\bno visa sponsorship\b",
    r"\bvisa sponsorship is not available\b",
    r"\bnot eligible for visa sponsorship\b",
    r"\bsponsorship is not available\b",
    r"\bwithout (?:the )?need for (?:visa )?sponsorship\b",
    # Security clearance requirements
    r"\b(?:active|required|must have|must possess).*?security clearance\b",
    r"\b(?:active|required|must have|must possess).*?(?:secret|top secret|ts/sci|dod secret)\b",
    r"\b(?:secret|top secret|ts/sci|dod secret) clearance required\b",
    # US-only location restrictions
    r"\b(?:us|u\.s\.|usa)[ -]?only\b",
    r"\bremote\s*[-–—]?\s*(?:us|u\.s\.|usa)\b",
    r"\bremote .*?\b(?:united states only|us only|u\.s\. only|usa only)\b",
]

levels_to_skip = [
    r"\blead\b",
    r"\bmanager\b",
    r"\bconsultor\b",
    r"\bconsultant\b",
    r"\bconsulting\b",
    r"\bprincipal\b",
    r"\bprinciple\b",
    r"\bdirector",
    r"\bvice president\b",
    r"\bstaff\b",
    r"\bhead of\b",
    r"\bchief\b",
    r"\bdistinguished\b",
    r"\bproduct owner\b",
    r"\bbusiness analyst\b",
    r"\bleader\b",
]

abbreviations_to_skip = [
    r"\bvp\b",
    r"\bsvp\b",
    r"\bavp\b",
]

unrelated_tech_to_skip = [
    r"\bdata engineer\b",
    r"\bdata scientist\b",
    r"\bdata analyst\b",
    r"\bmachine learning engineer\b",
    r"\bml engineer\b",
    r"\bai engineer\b",
    r"\bfrontend\b",
    r"\bfront-end\b",
    r"\bfullstack\b",
    r"\bfull stack\b",
    r"\bfull-stack\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bmobile developer\b",
    r"\bmobile engineer\b",
    r"\bqa\b",
    r"\bsdet\b",
    r"\bquality assurance\b",
    r"\btest engineer\b",
    r"\btest automation\b",
    r"\btesting engineer\b",
    r"\bverification engineer\b",
    r"\bsalesforce\b",
    r"\bdynamics 365\b",
    r"\bservicenow\b",
    r"\bsap\b",
    r"\boracle fusion\b",
    r"\boracle hcm\b",
    r"\bjava developer\b",
    r"\bdata science\b",
    r"\berp developer\b",
    r"\bmainframe developer\b",
    r"\bios developer\b",
    r"\bandroid\b",
    r"\bjava\b",
    r"\brust\b",
    r"\bphp\b",
    r"\b\.net\b",
    r"(?<!\w)\.net\b",
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
    r"\bcustomer engagements\b",
    r"\bMechanical Design\b",
    r"\btruck\b",
    r"\bMercado\b",
    r"\bvideo editor\b",
    r"\bmanufacturing engineer\b",
    r"\bbusiness development\b",
    r"\bsales\b",
    r"\bmarketing\b",
    r"\baccount executive\b",
    r"\bcustomer success\b",
    r"\btalent acquisition\b",
    r"\brecruiter\b",
    r"\bhuman resources\b",
    r"\badministrative assistant\b",
    r"\bvirtual assistant\b",
    r"\bexecutive assistant\b",
    r"\bproject coordinator\b",
    r"\bprogram coordinator\b",
    r"\bforklift\b",
    r"\bproduction associate\b",
    r"\bmaintenance technician\b",
    r"\bnurse\b",
    r"\bnursing\b",
    r"\bpharmacy\b",
    r"\bpharmacist\b",
    r"\bphysician\b",
    r"\bCustomer Service\b",
    r"\bTeller\b",
    r"\bContent Creator\b",
    r"\bRobotics\b",
    r"\bcivil\b",
    r"\bmechanical\b",
    r"\belectrical\b",
    r"\bbridge design\b",
    r"\bstructural designer\b",
    r"\bsound system\b",
    r"\bplumbing\b",
    r"\bqc engineer\b",
    r"\bcnc\b",
    r"\bhvac\b",
    r"\bbim\b",
    r"\bpavement\b",
    r"\bsolar design\b",
    r"\btechnical office\b",
    r"\bsales engineer\b",
    r"\bpresales engineer\b",
    r"\bfire fighting\b",
    r"\bworkshop engineer\b",
]

languages_to_skip = [
    r"\bfrench speaker\b",
    r"\bgerman speaker\b",
]

blocked_titles_regex = "|".join(
    levels_to_skip
    + abbreviations_to_skip
    + unrelated_tech_to_skip
    + unrelated_non_tech_to_skip
    +languages_to_skip,
).lower()

blocked_companies_regex = "|".join(companies_blacklist)

blocked_descriptions_regex = "|".join(description_blockers)
