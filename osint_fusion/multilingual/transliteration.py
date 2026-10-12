"""Cross-script transliteration normalizer and phonetic matching for Indic languages."""

import unicodedata
from typing import Dict, List, Tuple, Set


# Standard Indic to Roman phonetic approximations
BENGALI_TO_ROMAN = {
    'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'i', 'উ': 'u', 'ঊ': 'u', 'ঋ': 'ri',
    'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
    'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
    'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
    'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
    'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
    'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
    'য': 'y', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
    'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't', 'ং': 'ng', 'ঃ': 'h', 'ঁ': 'n',
    'া': 'a', 'ি': 'i', 'ী': 'i', 'ু': 'u', 'ূ': 'u', 'ৃ': 'ri',
    'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou', '্': '',
    # Assamese specific
    'ৰ': 'r', 'ৱ': 'w'
}

DEVANAGARI_TO_ROMAN = {
    'अ': 'a', 'आ': 'a', 'इ': 'i', 'ई': 'i', 'उ': 'u', 'ऊ': 'u', 'ऋ': 'ri',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'n',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
    'ा': 'a', 'ि': 'i', 'ी': 'i', 'ु': 'u', 'ू': 'u', 'ृ': 'ri',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', '्': '', 'ं': 'n', 'ः': 'h',
    'ळ': 'l'
}

TAMIL_TO_ROMAN = {
    'அ': 'a', 'ஆ': 'a', 'இ': 'i', 'ஈ': 'i', 'உ': 'u', 'ஊ': 'u', 'எ': 'e', 'ஏ': 'e', 'ஐ': 'ai',
    'ஒ': 'o', 'ஓ': 'o', 'ஔ': 'au',
    'க': 'k', 'ங': 'ng', 'ச': 'ch', 'ஞ': 'n', 'ட': 't', 'ண': 'n', 'த': 't', 'ந': 'n', 'ப': 'p',
    'ம': 'm', 'ய': 'y', 'ர': 'r', 'ல': 'l', 'வ': 'v', 'ழ': 'zh', 'ள': 'l', 'ற': 'r', 'ன': 'n',
    'ா': 'a', 'ி': 'i', 'ீ': 'i', 'ு': 'u', 'ூ': 'u', 'ெ': 'e', 'ே': 'e', 'ை': 'ai', 'ொ': 'o',
    'ோ': 'o', 'ௌ': 'au', '்': ''
}


def indic_to_roman(text: str) -> str:
    """Converts Indic script text to a normalized Roman phonetic representation."""
    result = []
    for ch in text:
        if ch in BENGALI_TO_ROMAN:
            result.append(BENGALI_TO_ROMAN[ch])
        elif ch in DEVANAGARI_TO_ROMAN:
            result.append(DEVANAGARI_TO_ROMAN[ch])
        elif ch in TAMIL_TO_ROMAN:
            result.append(TAMIL_TO_ROMAN[ch])
        else:
            result.append(ch)
    normalized = "".join(result).lower()
    # Normalize common phonetic double consonants and vowels
    normalized = normalized.replace("oo", "u").replace("ee", "i").replace("sh", "s").replace("v", "b")
    normalized = "".join(c for c in normalized if c.isalnum() or c.isspace())
    return " ".join(normalized.split())


def phonetic_key(text: str) -> str:
    """Generates an Indic phonetic hash for fuzzy entity matching."""
    roman = indic_to_roman(text)
    if not roman:
        return ""
    # Strip vowels except first letter, reduce identical adjacent consonants
    words = roman.split()
    keys = []
    for w in words:
        if not w:
            continue
        first = w[0]
        rest = "".join(c for c in w[1:] if c not in "aeiouy")
        # deduplicate adjacent
        dedup = [first]
        for c in rest:
            if not dedup or dedup[-1] != c:
                dedup.append(c)
        keys.append("".join(dedup))
    return "-".join(keys)


def string_similarity(s1: str, s2: str) -> float:
    """Calculates Levenshtein-based similarity score [0.0 - 1.0]."""
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)
    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost,
            )

    dist = matrix[len1][len2]
    max_len = max(len1, len2)
    return 1.0 - (dist / max_len)


class TransliterationEngine:
    """Detects alternative transliterations and cross-lingual spellings."""

    KNOWN_CANONICAL_SYNONYMS: Dict[str, List[str]] = {
        "Subrata Mukherjee": [
            "সুব্রত মুখার্জী",
            "সুব্রত মুখোপাধ্যায়",
            "सुब्रतो मुखर्जी",
            "Subroto Mukherjee",
            "Subrata Mukhopadhyay",
            "S. Mukherjee",
        ],
        "Vikramaditya Logistics Pvt Ltd": [
            "विक्रमादित्य लॉजिस्टिक्स प्राइवेट लिमिटेड",
            "বিক্রমাদিত্য লজিস্টিকস",
            "Vikramaditya Logistics",
            "Vikramaditya Transport",
            "விக்ரமாதித்யா லாஜிஸ்டிக்ஸ்",
        ],
        "Rupali Transport": [
            "রূপালী ট্রান্সপোর্ট",
            "रुपाली ट्रांसपोर्ट",
            "Rupali Roadways",
        ],
        "Siliguri": [
            "শিলিগুড়ি",
            "सिलीगुड़ी",
            "Siliguri Corridor",
            "Shiliguri",
        ],
        "Petrapole": [
            "পেট্রাপোল",
            "पेत्रापोल",
            "Petrapole ICP",
        ],
        "Benapole": [
            "বেনাপোল",
            "बेनापोल",
            "Benapole Land Port",
        ],
        "Fulbari": [
            "ফুলবাড়ি",
            "फूलबाड़ी",
            "Phulbari Checkpost",
        ],
        "Dhubri": [
            "ধুবুৰী",
            "धुबरी",
            "Dhubri River Port",
        ],
        "Haldia": [
            "হলদিয়া",
            "हल्दिया",
            "Haldia Dock",
        ],
        "Chennai Port": [
            "சென்னை துறைமுகம்",
            "चेन्नई पोर्ट",
            "Madras Port",
        ],
    }

    @classmethod
    def match_entity_name(cls, name_candidate: str, canonical_target: str) -> Tuple[bool, float, str]:
        """
        Conservative match between a candidate name and a canonical target.
        Returns: (is_match, similarity_score, reason)
        """
        c_cand = name_candidate.strip()
        c_target = canonical_target.strip()

        # Check known dictionary synonyms
        if c_target in cls.KNOWN_CANONICAL_SYNONYMS:
            synonyms = cls.KNOWN_CANONICAL_SYNONYMS[c_target]
            if c_cand.lower() == c_target.lower():
                return True, 1.0, "Exact canonical match"
            for syn in synonyms:
                if c_cand.lower() == syn.lower() or c_cand == syn:
                    return True, 0.98, f"Known cross-script alias match with '{syn}'"

        # Check Roman transliteration
        rom_cand = indic_to_roman(c_cand)
        rom_target = indic_to_roman(c_target)

        if rom_cand == rom_target and rom_cand != "":
            return True, 0.92, "Identical Romanized phonetic form"

        # Check phonetic keys
        pk_cand = phonetic_key(c_cand)
        pk_target = phonetic_key(c_target)

        sim = string_similarity(rom_cand, rom_target)
        if pk_cand == pk_target and pk_cand != "" and sim >= 0.75:
            return True, sim, f"Phonetic key match ({pk_cand}) with string similarity {sim:.2f}"

        if sim >= 0.85:
            return True, sim, f"High string similarity ({sim:.2f})"

        return False, sim, "Insufficient evidence for cross-script match"
