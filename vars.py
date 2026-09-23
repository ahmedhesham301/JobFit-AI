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
    r"\bu\.?s\.? citizenship is required\b",
    r"\bno sponsorship (?:can|will) be provided\b",
    r"\bvisa sponsor(?:ship)? is not available\b",
    r"\bnot eligible for (?:visa|immigration) sponsorship\b",
    r"\bwithout (?:current or future )?(?:visa )?sponsorship\b",
    r"\bwe (?:cannot|can't|do not|don't) provide (?:visa )?sponsorship\b",
    r"\bwe (?:cannot|can't|do not|don't) sponsor\b",
    r"\b(?:company|employer) does not sponsor\b",
    # Security clearance requirements
    r"\b(?:active|required|must have|must possess).*?security clearance\b",
    r"\b(?:active|required|must have|must possess).*?(?:secret|top secret|ts/sci|dod secret)\b",
    r"\b(?:secret|top secret|ts/sci|dod secret) clearance required\b",
    r"\bmust be eligible to obtain(?: and maintain)? .*?clearance\b",
    r"\bability to obtain(?: and maintain)? .*?clearance\b",
    r"\bmust be able to obtain(?: and maintain)? .*?clearance\b",
    r"\bactive (?:secret|top secret|ts/sci|dod secret) clearance\b",
    r"\bts/sci(?: with polygraph)?\b",
    # US-only location restrictions
    r"\b(?:us|u\.s\.|usa)[ -]?only\b",
    r"\bremote\s*[-–—]?\s*(?:us|u\.s\.|usa)\b",
    r"\bremote .*?\b(?:united states only|us only|u\.s\. only|usa only)\b",
    # Experience requirements — hard skip at 5+ years
    r"\b(?:minimum(?: of)?|at least)\s+(?:5|6|7|8|9|10|11|12|13|14|15)\+?\s+years?(?: of)? .*?experience\b",
    r"\b(?:requires?|required|requiring)\s+(?:a )?(?:minimum(?: of)? )?(?:5|6|7|8|9|10|11|12|13|14|15)\+?\s+years?(?: of)? .*?experience\b",
    r"\bmust have\s+(?:at least )?(?:5|6|7|8|9|10|11|12|13|14|15)\+?\s+years?(?: of)? .*?experience\b",
    r"(?<!or )(?<!\d-)(?<!\d–)(?<!\d—)(?<!\d - )(?<!\d – )(?<!\d — )"
    r"\b(?:5|6|7|8|9|10|11|12|13|14|15)"
    r"(?:\s*[-–—]\s*\d+)?\+?\s*(?:years?|yrs?)\s+of"
    r"(?:\s+[\w/-]+){0,5}\s+experience\b",
    # US location restrictions
    r"\bmust (?:currently )?(?:reside|live|be located|be based) in (?:the )?(?:u\.?s\.?|united states)\b",
    r"\bremote(?:\s+(?:position|role))?(?:\s+is)?\s+(?:only\s+)?(?:within|in|from)\s+(?:the\s+)?(?:u\.?s\.?|united states)\b",
    r"\bopen only to (?:candidates|applicants) (?:in|based in|located in) (?:the )?(?:u\.?s\.?|united states)\b",
]

levels_to_skip = [
    r"\blead\b",
    r"\bmanager\b",
    r"\bconsultor\b",
    r"\bconsultant\b",
    r"\bconsulting\b",
    r"\bprincipal\b",
    r"\bprinciple\b",
    r"\bdirector\b",
    r"\bvice president\b",
    r"\bstaff\b",
    r"\bhead of\b",
    r"\bchief\b",
    r"\bdistinguished\b",
    r"\bproduct owner\b",
    r"\bbusiness analyst\b",
    r"\bleader\b",
    r"\bsupervisorr?\b",
    r"\bservice owner\b",
    r"\bplatform owner\b",
    r"\bsenior\b",
    r"\bsr\.?\b",
    r"\bsnr\b",
    r"\barchitect\b",
    r"\bsection head\b",
    r"\bsubject matter expert\b",
    r"\bsme\b",
]

abbreviations_to_skip = [
    r"\bvp\b",
    r"\bsvp\b",
    r"\bavp\b",
    r"\bcto\b",
    r"\bcio\b",
    r"\bciso\b",
    r"\bcoo\b",
    r"\bceo\b",
    r"\bevp\b",
]

unrelated_tech_to_skip = [
    # data
    r"\bdata engineer(?:ing)?\b",
    r"\bdata scientist\b",
    r"\bdata developer\b",
    r"\bdata analyst\b",
    r"\bdatabricks\b",
    # ml & ai
    r"\bmachine learning engineer(?:ing)?\b",
    r"\bml engineer(?:ing)?\b",
    r"\bai engineer(?:ing)?\b",
    r"\bArtificial Intelligence Engineer(?:ing)?\b",
    r"\bai researcher\b",
    r"\bmachine learning researcher\b",
    r"\bAI Systems Engineer(?:ing)?\b",
    r"\bllm application engineer(?:ing)?\b",
    # frontend, mobile
    r"\bfrontend\b",
    r"\bfront-end\b",
    r"\bfullstack\b",
    r"\bfull stack\b",
    r"\bfull-stack\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bmobile developer\b",
    r"\bmobile engineer\b",
    # c++
    r"\bC\+\+ Software Engineer\b",
    r"\bC\+\+ Developer\b",
    r"\bC\+\+ Integration Engineer\b",
    # testing
    r"\bqa\b",
    r"\bsdet\b",
    r"\bquality assurance\b",
    r"\btest engineer\b",
    r"\btest automation\b",
    r"\btesting engineer\b",
    r"\bQuality Control\b",
    r"\bverification engineer\b",
    r"\bvalidation engineer\b",
    # etc
    r"\bsalesforce\b",
    r"\bdynamics 365\b",
    r"\bservicenow\b",
    r"\bsap\b",
    r"\boracle fusion\b",
    r"\boracle hcm\b",
    # java
    r"\bjava developer\b",
    r"\bjava software engineer\b",
    r"\bJava Backend Developer\b",
    r"\bdata science\b",
    r"\berp developer\b",
    r"\bmainframe developer\b",
    r"\bios developer\b",
    r"\brust\b",
    r"\bphp\b",
    r"(?<!\w)\.net\b",
    # Design and client applications
    r"\bui[ /-]?ux\b",
    r"\bui developer\b",
    r"\bux designer\b",
    r"\bweb designer\b",
    r"\bgraphic designer\b",
    r"\bproduct designer\b",
    r"\bdesktop developer\b",
    # Embedded and gaming
    r"\bembedded(?: systems?| software)? engineer\b",
    r"\bfirmware engineer\b",
    r"\bfirmware developer\b",
    r"\bgame developer\b",
    r"\bgame engineer\b",
    # Unrelated development stacks
    r"\bwordpress\b",
    r"\bruby developer\b",
    r"\brails developer\b",
    r"\belixir developer\b",
    # Enterprise and analytics platforms
    r"\bsharepoint\b",
    r"\bpower platform\b",
    r"\bpower bi\b",
    r"\bbi developer\b",
    r"\bbusiness intelligence\b",
    r"\brpa developer\b",
    r"\buipath\b",
    # Hardware
    r"\bhardware engineer\b",
    r"\bhardware developer\b",
    # Make Rust/PHP/.NET filtering title-specific
    r"\brust developer\b",
    r"\brust engineer\b",
    r"\bphp developer\b",
    r"\bphp engineer\b",
    r"(?<!\w)\.net developer\b",
    r"(?<!\w)\.net engineer\b",
    r"\brpa\b",
    r"\brobotic process automation\b",
    r"\bmern stack\b",
    r"\bHPC Engineer\b",
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
    # Additional construction and physical engineering
    r"\bsite engineer\b",
    r"\bmep engineer\b",
    r"\bmep designer\b",
    r"\barchitectural engineer\b",
    r"\barchitectural designer\b",
    r"\bmarine engineer\b",
    r"\btechnical superintendent\b",
    r"\brailway engineer\b",
    r"\brail engineer\b",
    r"\bcommissioning engineer\b",
    r"\bpackaging engineer\b",
    r"\bquantity surveyor\b",
    r"\bland surveyor\b",
    r"\bgeotechnical engineer\b",
    r"\bpiping engineer\b",
    r"\binstrumentation engineer\b",
    r"\bpetroleum engineer\b",
    r"\bchemical engineer\b",
    r"\bindustrial engineer\b",
    r"\bprocess engineer\b",
    r"\bplanning engineer\b",
    r"\bestimation engineer\b",
    r"\bcost engineer\b",
    r"\bfacilities engineer\b",
    r"\bfire protection\b",
    r"\bsmart[ -]?home\b",
    r"\bknx\b",
    # Support and field roles
    r"\bhelp[ -]?desk\b",
    r"\bservice desk\b",
    r"\bdesktop support\b",
    r"\bit support\b",
    r"\bfield service engineer\b",
    r"\bcall center\b",
    r"\bsecurity guard\b",
    r"\bcontent writer\b",
    r"\bsocial media\b",
    r"\bquality engineer\b",
    r"\bplant engineer\b",
    r"\binjection molding\b",
    r"\binjection moulding\b",
    r"\bproduct design(?:\s*&\s*innovation)? analyst\b",
    r"\bmigration analyst\b",
    r"\bmanufacturing (?:engineering )?specialist\b",
    r"\bmanufacturing engineering coordinator\b",
    r"\bMaintenance Engineer\b",
    r"\bMechatronics Engineer\b",
    # Manufacturing / physical engineering
    r"\btextile engineer\b",
    r"\bproduction planner\b",
    r"\brolling stock\b",
    r"\bgenerator commissioning\b",
    r"\bwell services\b",
    r"\bWelding Engineer\b",
    r"\bHydrology & Drainage Engineer\b",
    r"\bElectronics Technician\b",
    r"\bSteel Production Engineer\b",
    # Arabic physical-engineering titles
    r"\bمهندس\s+مدن[ىي]\b",
    r"\bمهندس\s+ميكانيكا\b",
    r"\bمهندس\s+كهرباء\b",
    r"\bمهندس\s+إ?نتاج\b",
    r"\bمدير\s+إ?نتاج\b",
]

languages_to_skip = [
    r"\b(?:french|german|dutch|spanish|italian|portuguese|polish|"
    r"czech|swedish|danish|norwegian|finnish)\s*[- ]?"
    r"(?:speaker|speaking)\b",
]

positive_keywords = [
    # =========================
    # Cloud
    # =========================
    r"\baws\b",
    r"\bamazon web services\b",
    r"\bgcp\b",
    r"\bgoogle cloud(?: platform)?\b",
    r"\bazure\b",
    r"\bmicrosoft azure\b",
    r"\bhetzner\b",
    r"\bhetzner cloud\b",
    r"\bdigitalocean\b",
    # =========================
    # Kubernetes / Containers
    # =========================
    r"\bkubernetes\b",
    r"\bk8s\b",
    r"\bdocker\b",
    r"\bcontainers?\b",
    r"\bcontainerization\b",
    r"\bhelm\b",
    r"\beks\b",
    r"\bgke\b",
    r"\baks\b",
    r"\bk3s\b",
    r"\bmicrok8s\b",
    r"\bopenshift\b",
    # =========================
    # Infrastructure as Code
    # =========================
    r"\bterraform\b",
    r"\bansible\b",
    r"\bpulumi\b",
    r"\bcloudformation\b",
    r"\baws cloudformation\b",
    r"\bcrossplane\b",
    r"\bpacker\b",
    # =========================
    # CI/CD
    # =========================
    r"\bgithub actions\b",
    r"\bjenkins\b",
    r"\bgitlab ci\b",
    r"\bgitlab ci\/cd\b",
    r"\bargo ?cd\b",
    r"\bargocd\b",
    r"\bargo workflows?\b",
    r"\bflux ?cd\b",
    r"\bfluxcd\b",
    r"\btekton\b",
    r"\bcircleci\b",
    r"\btravis ci\b",
    r"\bci\/cd\b",
    r"\bcontinuous integration\b",
    r"\bcontinuous delivery\b",
    r"\bcontinuous deployment\b",
    # =========================
    # GitOps
    # =========================
    r"\bgitops\b",
    # =========================
    # Observability / Monitoring
    # =========================
    r"\bprometheus\b",
    r"\bgrafana\b",
    r"\bopentelemetry\b",
    r"\bopen telemetry\b",
    r"\bloki\b",
    r"\btempo\b",
    r"\bgrafana alloy\b",
    r"\bdatadog\b",
    r"\bnew relic\b",
    r"\belasticsearch\b",
    r"\belastic stack\b",
    r"\belk\b",
    r"\bmonitoring\b",
    r"\bobservability\b",
    # =========================
    # Linux / Systems
    # =========================
    r"\blinux\b",
    r"\bubuntu\b",
    r"\bdebian\b",
    r"\brhel\b",
    r"\bred hat\b",
    r"\bcentos\b",
    r"\bsystemd\b",
    r"\bbash\b",
    r"\bshell scripting\b",
    # =========================
    # Networking / Proxies
    # =========================
    r"\bnginx\b",
    r"\bhaproxy\b",
    r"\benvoy\b",
    r"\btraefik\b",
    r"\bload balanc(?:er|ing)\b",
    r"\breverse prox(?:y|ies)\b",
    r"\bdns\b",
    r"\btcp\/ip\b",
    # =========================
    # Infrastructure / Platform
    # =========================
    r"\binfrastructure automation\b",
    r"\binfrastructure engineering\b",
    r"\bplatform engineering\b",
    r"\bplatform engineer(?:ing)?\b",
    r"\bcloud engineering\b",
    r"\bcloud infrastructure\b",
    r"\bdeveloper platform\b",
    r"\binternal developer platform\b",
    # =========================
    # DevOps / SRE
    # =========================
    r"\bdevops\b",
    r"\bdevsecops\b",
    r"\bsite reliability\b",
    r"\bsite reliability engineer(?:ing)?\b",
    r"\bsre\b",
    r"\breliability engineering\b",
    r"\bproduction engineering\b",
    # =========================
    # Programming
    # =========================
    # Don't use \bgo\b because "go" is a very common English word
    r"\bgolang\b",
    r"\bpython\b",
    r"\bnode\.?js\b",
    r"\btypescript\b",
    r"\bjava\b",
    # =========================
    # Backend
    # =========================
    r"\bbackend\b",
    r"\bback-end\b",
    r"\brest(?:ful)? api(?:s)?\b",
    r"\bmicroservices?\b",
    r"\bapi development\b",
    r"\bdistributed systems?\b",
    r"\bhigh availability\b",
    r"\bfault toleran(?:t|ce)\b",
    r"\bscalab(?:le|ility)\b",
    # =========================
    # Databases / Caches
    # =========================
    r"\bpostgres(?:ql)?\b",
    r"\bmysql\b",
    r"\bmongodb\b",
    r"\bredis\b",
    r"\bdatabases?\b",
    # =========================
    # Messaging / Streaming
    # =========================
    r"\bkafka\b",
    r"\bapache kafka\b",
    r"\brabbitmq\b",
    r"\bmessage queu(?:e|es|ing)\b",
    r"\bevent[- ]driven\b",
    r"\bevent streaming\b",
    # =========================
    # Security / DevSecOps
    # =========================
    r"\bvault\b",
    r"\bhashicorp vault\b",
    r"\btrivy\b",
    r"\bsonarqube\b",
    r"\bdevsecops\b",
    r"\biam\b",
    r"\bidentity and access management\b",
    r"\bsecrets management\b",
    # =========================
    # Cloud architecture
    # =========================
    r"\bvpc\b",
    r"\bautoscal(?:e|er|ing)\b",
    r"\bauto[- ]scaling\b",
    r"\bserverless\b",
    r"\blambda\b",
    r"\bcloud native\b",
    r"\bcloud-native\b",
    # =========================
    # Operations concepts
    # =========================
    r"\bincident response\b",
    r"\bon[- ]call\b",
    r"\broot cause analysis\b",
    r"\brca\b",
    r"\bdisaster recovery\b",
    r"\bcapacity planning\b",
    r"\bperformance tuning\b",
]
blocked_titles_regex = "|".join(
    levels_to_skip
    + abbreviations_to_skip
    + unrelated_tech_to_skip
    + unrelated_non_tech_to_skip
    + languages_to_skip,
).lower()

positive_keywords_regex = "|".join(positive_keywords)

blocked_companies_regex = "|".join(companies_blacklist)

blocked_descriptions_regex = "|".join(description_blockers)
