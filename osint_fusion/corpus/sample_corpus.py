"""Benchmark multilingual test corpus for the OSINT Fusion Workbench."""

from typing import List
from ..models.source import Source, SourceType, LanguageCode, AudioMetadata
from ..multilingual.detector import LanguageDetector
from ..multilingual.translation import TranslationManager


def get_default_benchmark_corpus() -> List[Source]:
    """Returns the standardized, multilingual evaluation corpus."""
    sources: List[Source] = []

    # SRC-001: Bengali Local Daily
    bn_text = (
        "শিলিগুড়ি, ৮ অক্টোবর: মঙ্গলবার সন্ধ্যায় ফুলবাড়ি চেকপোস্ট করিডোরে স্থানীয় পুলিশ ও আবগারি বাহিনীর "
        "যৌথ অভিযানে একটি ১০ চাকার মালবাহী লরি আটক করা হয়। গাড়িটি 'রূপালী ট্রান্সপোর্ট' সংস্থার অধীনে চলছিল "
        "(রেজিস্ট্রেশন নম্বর WB-73-E-4421)। গাড়ির ভিতর থেকে ১২০ কেজি নামহীন ড্রামভর্তি রাসায়নিক তরল ও গুঁড়ো উদ্ধার হয়েছে। "
        "ঘটনাস্থল থেকে চালক সুব্রত মুখার্জী (৩৮, মালদহ নিবাসী)-কে আটক করা হয়েছে। প্রাথমিক জিজ্ঞাসাবাদে চালক দাবি করেন "
        "যে অসমের ধুবুৰী নদীঘাট সংলগ্ন একটি অস্থায়ী গুদাম থেকে এই মাল বোঝাই করা হয়েছিল এবং জলপাইগুড়ির একটি কারখানায় পাঠানোর কথা ছিল।"
    )
    src1_det = LanguageDetector.analyze_text(bn_text)
    trans1, status1 = TranslationManager.get_translation_with_badges("SRC-001", bn_text, src1_det["primary_language"])
    s1 = Source(
        id="SRC-001",
        title="ফুলবাড়ি সীমান্তে রাসায়নিক বোঝাই লরি আটক, চালক ধৃত",
        source_org="উত্তরবঙ্গ সংবাদ (Uttarbanga Sambad)",
        source_type=SourceType.NEWS_ARTICLE,
        original_url="https://uttarbangasambad.example.in/news/2026-10-08/fulbari-seizure-4421",
        publication_date="2026-10-08",
        original_language=src1_det["primary_language"],
        original_language_name=src1_det["language_name"],
        is_mixed_language=src1_det["is_mixed"],
        languages_detected=src1_det["detected_languages"],
        original_text=bn_text,
        english_translation=trans1,
        translation_status=status1,
        page_numbers="Page 3, Column 2",
        paragraph_reference="Paragraphs 1-2",
        is_primary_source=True,
        source_reliability_score=0.78,
        reliability_notes="Regional daily newspaper with established local reporting network in North Bengal."
    )
    sources.append(s1)

    # SRC-002: Hindi Official Police Press Release
    hi_text = (
        "पश्चिम बंगाल पुलिस विज्ञप्ति | सिलीगुड़ी पुलिस कमिश्नरेट | दिनांक ०९ अक्टूबर २०२६:\n"
        "दिनांक ०८ अक्टूबर २०२६ की संध्या को फुलबाड़ी सीमा चौकी पर विशेष तलाशी अभियान के दौरान एक भारी मालवाहक वाहन "
        "(पंजीकरण संख्या WB-73-E-4421) को रोका गया। तलाशी में १२० किलोग्राम संदिग्ध प्रतिबंधित रासायनिक मिश्रण (Precursor Chemicals) "
        "बरामद किया गया। वाहन का पंजीकृत वाणिज्यिक स्वामी 'विक्रमादित्य लॉजिस्टिक्स प्राइवेट लिमिटेड' (कोलकाता/हल्दिया) पाया गया है। "
        "चालक सुब्रतो मुखर्जी (पुत्र बी. मुखर्जी, निवासी इंग्लिश बाजार, मालदा) को हिरासत में लेकर पूछताछ की जा रही है। "
        "चालक ने बयान दिया है कि उसे मालदा निवासी 'पी. के. बिस्वास' नामक एक मध्यस्थ दलाल द्वारा भाड़े पर नियुक्त किया गया था। "
        "थाना भक्तिनगर में सुसंगत धाराओं के अंतर्गत मामला दर्ज कर अग्रेतर विवेचना जारी है।"
    )
    src2_det = LanguageDetector.analyze_text(hi_text)
    trans2, status2 = TranslationManager.get_translation_with_badges("SRC-002", hi_text, src2_det["primary_language"])
    s2 = Source(
        id="SRC-002",
        title="फुलबाड़ी चौकी पर संदिग्ध रासायनिक पदार्थ की बरामदगी बाबत आधिकारिक प्रेस विज्ञप्ति",
        source_org="পশ্চিমবঙ্গ পুলিশ (West Bengal Police / Siliguri Commissionerate)",
        source_type=SourceType.POLICE_REPORT,
        original_url="https://wbpolice.gov.in/press/siliguri/2026/pr-10-09-fulbari.pdf",
        filename="PR_SIL_2026_10_09_FULBARI.pdf",
        publication_date="2026-10-09",
        original_language=src2_det["primary_language"],
        original_language_name=src2_det["language_name"],
        is_mixed_language=src2_det["is_mixed"],
        languages_detected=src2_det["detected_languages"],
        original_text=hi_text,
        english_translation=trans2,
        translation_status=status2,
        page_numbers="Official Bulletin 1/1",
        paragraph_reference="Full Official Release",
        is_primary_source=True,
        source_reliability_score=0.92,
        reliability_notes="Official law enforcement public release signed by authorized public relations officer."
    )
    sources.append(s2)

    # SRC-003: English Investigative News Dispatch
    en_text = (
        "SILIGURI / KOLKATA — The interception of a chemical freight carrier at the Fulbari border corridor has exposed "
        "a tangled web of interstate logistics operations. According to corporate filings, 'Rupali Transport', the entity "
        "operating the vehicle, is a wholly owned operating subsidiary of Kolkata-based Vikramaditya Logistics Private Limited. "
        "However, significant discrepancies have emerged regarding the seizure: while initial statements cited Oct 8, a senior "
        "customs clerk speaking on condition of strict anonymity asserted that the vehicle was quietly detained as early as Oct 7, "
        "and that the total seized weight of industrial precursors approached 200 kg rather than the officially cited 120 kg. "
        "Company representatives in Kolkata have declined repeated requests for comment."
    )
    src3_det = LanguageDetector.analyze_text(en_text)
    trans3, status3 = TranslationManager.get_translation_with_badges("SRC-003", en_text, src3_det["primary_language"])
    s3 = Source(
        id="SRC-003",
        title="Discrepancies Emerge in Fulbari Chemical Interception as Subsidiary Ties Surface",
        source_org="The Eastern Sentinel (Investigative Desk)",
        source_type=SourceType.INVESTIGATIVE_REPORT,
        original_url="https://easternsentinel.example.com/investigations/2026/fulbari-subsidiary-trail",
        publication_date="2026-10-10",
        original_language=src3_det["primary_language"],
        original_language_name=src3_det["language_name"],
        is_mixed_language=src3_det["is_mixed"],
        languages_detected=src3_det["detected_languages"],
        original_text=en_text,
        english_translation=trans3,
        translation_status=status3,
        page_numbers="Online Edition",
        paragraph_reference="Paragraphs 1-4",
        is_primary_source=True,
        source_reliability_score=0.72,
        reliability_notes="Investigative journalism with mixed primary and anonymous sources; contains unverified claims."
    )
    sources.append(s3)

    # SRC-004: Assamese Radio Broadcast Transcript (Authorized speech material with timestamps)
    as_text = (
        "[সম্প্ৰচাৰ সময়: ১০ অক্টোবৰ ২০২৬, পুৱা ০৭:৩০ বজা | অসম বাৰ্তা ৰেডিঅ', ধুবুৰী কেন্দ্ৰ]\n"
        "[00:04] বাতৰি পঢ়িছো অনামিকা বৰুৱা। ধুবুৰী ব্ৰহ্মপুত্ৰ ঘাটত নদীপথেৰে অস্বাভাৱিক সামগ্ৰী পৰিবহণৰ তথ্য পোহৰলৈ আহিছে।\n"
        "[00:45] [ambient river current noise] যোৱা দেওবাৰে নিশা দুখন কাঠৰ মটৰ নাওৰ পৰা কিছুমান ছীল কৰা প্লাষ্টিক ড্ৰাম এখন বন্ধ ট্ৰাকত তোলা দেখা গৈছিল বুলি স্থানীয় মাছমৰীয়াসকলে জনাইছে।\n"
        "[01:23] [uncertain: 'সন্দেজনক' / suspicious cargo] এই মালবাহী বাহনখনত মালদহৰ এটা ব্যৱসায়িক প্ৰতিষ্ঠানৰ চিন আছিল বুলি একাংশ প্ৰত্যক্ষদৰ্শীয়ে প্ৰকাশ কৰিছে।\n"
        "[02:10] নদী আৰক্ষীৰ স্পষ্ট অনুমতি অবিহনে এই সামগ্ৰী গোৱালপাৰা দিশৰ পৰা ধুবুৰী অভিমুখে অনা হৈছিল নেকি, সেই সন্দৰ্ভত স্থানীয় ৰাইজে তদন্ত দাবী কৰিছে।"
    )
    src4_det = LanguageDetector.analyze_text(as_text)
    trans4, status4 = TranslationManager.get_translation_with_badges("SRC-004", as_text, src4_det["primary_language"])
    s4 = Source(
        id="SRC-004",
        title="ধুবুৰী ঘাটত নদীপথেৰে সন্দেহজনক সামগ্ৰী উঠা-নমাৰ অভিযোগ",
        source_org="অসম বাৰ্তা (Asom Barta Community Radio, Dhubri Studio)",
        source_type=SourceType.AUDIO_BROADCAST,
        original_url="https://asombarta-radio.example.org/broadcasts/2026-10-10-dhubri-ghat.mp3",
        filename="ASOM_BARTA_DHUBRI_20261010_0730.mp3",
        publication_date="2026-10-10",
        original_language=src4_det["primary_language"],
        original_language_name=src4_det["language_name"],
        is_mixed_language=src4_det["is_mixed"],
        languages_detected=src4_det["detected_languages"],
        original_text=as_text,
        english_translation=trans4,
        translation_status=status4,
        audio_timestamps=[
            {"time": "00:04", "speaker": "Anamika Baruah", "content": "News bulletin introduction"},
            {"time": "00:45", "speaker": "Eyewitness account", "content": "Country boat offloading plastic drums at Dhubri ghat"},
            {"time": "01:23", "speaker": "Reporter note", "content": "Logistics signage linked to Malda commercial firm [uncertain word flagged]"},
            {"time": "02:10", "speaker": "Public inquiry", "content": "Unpermitted river transit from Goalpara corridor"}
        ],
        audio_metadata=AudioMetadata(
            is_audio=True,
            duration_seconds=185.0,
            sample_rate_hz=44100,
            channel_info="Mono Community FM 102.4 MHz",
            has_timestamps=True,
            transcription_engine="Human Linguist Certified with Machine Timing",
            uncertain_segments_count=1,
            analyst_authorization_ref="AUTH-OSINT-PUBLIC-RADIO-AIRWAVES-2026-09"
        ),
        is_primary_source=True,
        transcription_uncertainty_flag=True,
        source_reliability_score=0.74,
        reliability_notes="Public community radio broadcast; contains timestamped eyewitness accounts; acoustic uncertainty at 01:23 noted."
    )
    sources.append(s4)

    # SRC-005: Secondary Aggregator Portal (Demonstrates Circular Reporting / Copycat)
    s5_text = (
        "GLOBAL LOGISTICS PORTAL (Oct 11, 2026) — Security and customs watchers report that following an interception at Fulbari, "
        "Rupali Transport, an operating subsidiary of Vikramaditya Logistics, has come under scrutiny. According to customs accounts, "
        "the carrier was intercepted on Oct 7 carrying 200 kg of industrial chemicals, contradicting regional police statements. "
        "Authorities are investigating corporate linkages in Kolkata."
    )
    src5_det = LanguageDetector.analyze_text(s5_text)
    trans5, status5 = TranslationManager.get_translation_with_badges("SRC-005", s5_text, src5_det["primary_language"])
    s5 = Source(
        id="SRC-005",
        title="Fulbari Seizure Raises Questions Over Vikramaditya Logistics Freight Chain",
        source_org="Global Logistics Daily (Aggregator Portal)",
        source_type=SourceType.SECONDARY_AGGREGATOR,
        original_url="https://globallogisticsdaily.example.net/feed/2026-10-11/fulbari-seizure-discrepancy",
        publication_date="2026-10-11",
        original_language=src5_det["primary_language"],
        original_language_name=src5_det["language_name"],
        is_mixed_language=src5_det["is_mixed"],
        languages_detected=src5_det["detected_languages"],
        original_text=s5_text,
        english_translation=trans5,
        translation_status=status5,
        is_primary_source=False,
        derived_from_source_id="SRC-003",
        possible_duplicate_flag=True,
        source_reliability_score=0.45,
        reliability_notes="Secondary syndication portal; verbatim restatement of SRC-003 without original reporting. High circularity risk."
    )
    sources.append(s5)

    # SRC-006: Tamil Maritime Commerce Gazette (Official port registry)
    ta_text = (
        "சென்னை துறைமுக வர்த்தக அறிக்கை | அரசிதழ் பதிவு எண்: CHN-PRT-2026-0925 | தேதி: 25 செப்டம்பர் 2026:\n"
        "கப்பல் போக்குவரத்து மற்றும் சரக்கு கையாளுதல் உரிமப் பிரிவு: விக்ரமாதித்யா லாஜிஸ்டிக்ஸ் பிரைவேட் லிமிடெட் "
        "(Vikramaditya Logistics Private Limited) நிறுவனம் ஹால்டியா துறைமுகம் (Haldia) மற்றும் சென்னை துறைமுகத்திற்கு இடையிலான "
        "கடலோர சரக்குக் கப்பல் போக்குவரத்து அனுமதியைப் புதுப்பித்துள்ளது. இந்நிறுவனத்தின் நிர்வாக இயக்குநர் (Managing Director) "
        "திரு. ஏ. கே. ராய் (A. K. Roy) எனப் பதிவு செய்யப்பட்டுள்ளது. இந்நிறுவனத்தின் முதன்மை வங்கிக் கணக்கு கொல்கத்தா நேதாஜி சுபாஷ் சாலை கிளையில் செயல்படுகிறது."
    )
    src6_det = LanguageDetector.analyze_text(ta_text)
    trans6, status6 = TranslationManager.get_translation_with_badges("SRC-006", ta_text, src6_det["primary_language"])
    s6 = Source(
        id="SRC-006",
        title="சென்னை துறைமுக சரக்குக் கையாளுதல் உரிமம் புதுப்பித்தல் - விக்ரமாதித்யா லாஜிஸ்டிக்ஸ்",
        source_org="சென்னை துறைமுக வர்த்தக அரசிதழ் (Chennai Port Commercial Gazette)",
        source_type=SourceType.COMMERCE_REGISTRY,
        original_url="https://chennaiport.gov.in/gazette/2026/09/coastal-shipping-registry.pdf",
        filename="CHN_PORT_REGISTRY_20260925.pdf",
        publication_date="2026-09-25",
        original_language=src6_det["primary_language"],
        original_language_name=src6_det["language_name"],
        is_mixed_language=src6_det["is_mixed"],
        languages_detected=src6_det["detected_languages"],
        original_text=ta_text,
        english_translation=trans6,
        translation_status=status6,
        page_numbers="Gazette Section IV, p. 14",
        paragraph_reference="Entry 22B",
        is_primary_source=True,
        source_reliability_score=0.96,
        reliability_notes="Official statutory government port authority gazette registry."
    )
    sources.append(s6)

    # SRC-007: Court Bail Application Order Summary (Jalpaiguri District Court)
    # Vital test case for conservative entity resolution preventing false merge of "Subrata Mukherjee"
    crt_text = (
        "IN THE COURT OF THE DISTRICT & SESSIONS JUDGE, JALPAIGURI DIVISION\n"
        "Criminal / Civil Miscellaneous Docket | Bail Application No. 892/2026 | Order Date: 11 October 2026\n"
        "In re: Application for Anticipatory Bail filed on behalf of Subrata Mukherjee (Age 42), son of Late N. Mukherjee, "
        "resident of Dinhata Road, Cooch Behar, West Bengal.\n"
        "Subject Matter: Arising from Civil Title Suit No. 44/2024 regarding ancestral agricultural land boundary demarcation.\n"
        "Order Summary: Heard learned counsel. The Court specifically records that the applicant is a private school teacher "
        "and land claimant with no criminal antecedents and no connection whatsoever to interstate commercial logistics, "
        "chemical carriage, or vehicular operations. Bail is granted upon furnishing personal bond of Rs. 10,000."
    )
    src7_det = LanguageDetector.analyze_text(crt_text)
    trans7, status7 = TranslationManager.get_translation_with_badges("SRC-007", crt_text, src7_det["primary_language"])
    s7 = Source(
        id="SRC-007",
        title="Order in Bail Application 892/2026 (Subrata Mukherjee, Cooch Behar - Civil Boundary Matter)",
        source_org="District & Sessions Judge Court, Jalpaiguri Division",
        source_type=SourceType.COURT_DOCUMENT,
        original_url="https://districts.ecourts.gov.in/jalpaiguri/orders/2026/bail-892-order.pdf",
        filename="EC_JAL_BAIL_892_2026.pdf",
        publication_date="2026-10-11",
        original_language=src7_det["primary_language"],
        original_language_name=src7_det["language_name"],
        is_mixed_language=src7_det["is_mixed"],
        languages_detected=src7_det["detected_languages"],
        original_text=crt_text,
        english_translation=trans7,
        translation_status=status7,
        page_numbers="Order Sheet pp. 1-2",
        paragraph_reference="Paragraphs 3-5",
        is_primary_source=True,
        source_reliability_score=0.98,
        reliability_notes="Certified public judicial order sheet from official e-Courts record repository."
    )
    sources.append(s7)

    return sources
