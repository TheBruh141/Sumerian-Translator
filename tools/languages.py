import json
import requests
import re
from collections import defaultdict

old_languages = {
    "akk": "Akkadian",
    "sux": "Sumerian",
    "qpn": "Proper Nouns",
    "arc": "Aramaic",
    "elx": "Elamite",
    "grc": "Greek",
    "peo": "Old Persian",
    "ug": "Ugaritic",
    "xur": "Urartian",
}
transliterated_languages = {
    "akkts": "Akkadian",
    "suxts": "Sumerian",
    "qpnts": "Proper Nouns",
    "arcts": "Aramaic",
    "elxts": "Elamite",
    "grcts": "Greek",
    "peots": "Old Persian",
    "ugts": "Ugaritic",
}
modern_languages = {
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian"
}
ml_languages = {
    "ml_de": "German",
    "ml_en": "English",
    "ml_es": "Spanish",
    "ml_fr": "French",
    "ml_it": "Italian"
}

all_languages = {**old_languages, **transliterated_languages, **modern_languages, **ml_languages}

language_codes = set(list(all_languages.keys()))

unicode_en_to_ascii_en_replacements = [
    ("，", ", "),
    ("；", "; "),
    (" ̱", " "),
    (" ̄", " "),
    ("·", " "),
    ("−", "-"),
    ("≈", "="),
    ("⸢", ""),
    ("⸣", "#"),
    ("ʾ", "'"),
    ("ʿ", "'"),
    ("ʿ", "'"),
    ("˒", "'"),
    ("×", "x"),
    ("Ø", "0"),
    ("ā", "a"),
    ("Ā", "a"),
    ("ā", "a"),
    ("Ā", "a"),
    ("¯a", "a"),
    ("¯A", "A"),
    ("ã", "a"),
    ("Ã", "A"),
    ("á", "A"),
    ("Á", "A"),
    ("à", "a"),
    ("À", "A"),
    ("ḏ", "d"),
    ("Ḏ", "D"),
    ("d̄", "d"),
    ("D̄", "D"),
    ("\u0082", "e"),
    ("ē", "e"),
    ("Ē", "E"),
    ("è", "e"),
    ("È", "E"),
    ("ŋ", "g"),
    ("Ŋ", "G"),
    ("ĝ", "g"),
    ("Ĝ", "G"),
    ("ǵ", "g"),
    ("Ǵ", "g"),
    ("ḫ", "h"),
    ("Ḫ", "H"),
    ("ḥ", "h"),
    ("Ḥ", "H"),
    ("ȟ", "h"),
    ("Ȟ", "H"),
    ("ȟ", "h"),
    ("Ȟ", "H"),
    ("\u0068\u032e", "h"),
    ("\u0048\u032e", "H"),
    ("Ḫ̮", "H"),
    ("ī", "i"),
    ("Ī", "I"),
    ("ì", "i"),
    ("Ì", "I"),
    ("ȋ", "i"),
    ("Ȋ", "I"),
    ("í", "i"),
    ("Í", "I"),
    # ("î", "i"),
    # ("Î", "I"),
    ("\u0069\u0306", "î"),
    ("ř", "r"),
    ("Ř", "R"),
    ("šš", "sh"),
    ("š", "sh"),
    ("Š", "Sh"),
    ("š", "sh"),
    ("Š", "Sh"),
    ("ŝ", "sh"),
    ("Ŝ", "Sh"),
    ("ṣ", "sh"),
    ("Ṣ", "Sh"),
    ("ṣ", "sh"),
    ("Ṣ", "Sh"),
    ("ṧ", "sh"),
    ("Ṧ", "Sh"),
    ("Ş", "Sh"),
    ("Ś", "Sh"),
    ("ṭ", "t"),
    ("Ṭ", "T"),
    ("ṭ", "t"),
    ("Ṭ", "T"),
    ("ț", "T"),
    ("Ț", "T"),
    ("ṯ", "t"),
    ("Ṯ", "T"),
    ("ū", "u"),
    ("Ū", "U"),
    ("ȗ", "u"),
    ("Ȗ", "U"),
    ("û", "u"),
    ("Û", "U"),
    ("Û", "U"),
    ("ǔ", "u"),
    ("Ǔ", "U"),
    ("ũ", "u"),
    ("Ũ", "U"),
    ("ü", "u"),
    ("Ü", "U"),
    ("ù", "U"),
    ("Ù", "U"),
    ("ú", "u"),
    ("Ú", "U"),
    ("ẓ", "z"),
    ("Ẓ", "Z"),
    ("₀", "0"),
    ("₁", "1"),
    ("₂", "2"),
    ("₃", "3"),
    ("₄", "4"),
    ("₅", "5"),
    ("₆", "6"),
    ("₇", "7"),
    ("₈", "8"),
    ("₉", "9"),
    ("ₓ", "x"),
    ("¹", "1"),
    ("²", "2"),
    ("³", "3"),
    ("⁴", "4"),
    ("⁵", "5"),
    ("⁶", "6"),
    ("⁷", "7"),
    ("⁸", "8"),
    ("⁹", "9"),
    ("½", "1/2"),
    ("¼", "1/4"),
    ("¾", "3/4"),
    ("α", "alpha"),
    ("β", "beta"),
    ("β", "beta"),
    ("γ", "gamma"),
    ("δ", "delta"),
    ("ε", "epsilon"),
    ("η", "eta"),
    ("υ", "upsilon"),
    ("ζ", "zeta"),
    ("θ", "theta"),
    ("κ", "kappa"),
    ("ρ", "rho"),
    ("σ", "sigma"),
    ("τ", "tau"),
    ("φ", "phi"),
    ("π", "pi"),
    ("ω", "omega"),
    ("Ω", "Omega"),
    ("Ψ", "Psi"),
    ("ξ", "xi"),
    ("ϑ", "theta"),
    ("μ", "mu"),
    ("˚", "o"),
    ("º", "o"),
    ("✸", "*"),
    ("¤", "*"),
    ("¿", "?"),
]

unicode_atf_to_ascii_atf_replacements = [
                                            ("⸢", ""),
                                            ("⸣", "#"),
                                            ("ʾ", "'"),
                                            ("ʿ", "'"),
                                            ("ĝ", "g^"),
                                            ("Ĝ", "G^"),
                                            ("ŋ", "g"),
                                            ("Ŋ", "G"),
                                            ("ē", "e"),
                                            ("Ē", "E"),
                                            ("ḫ", "h"),
                                            ("Ḫ", "H"),
                                            ("š", "sz"),
                                            ("Š", "SZ"),
                                            ("ṣ", "s,"),
                                            ("Ṣ", "S,"),
                                            ("ś", "s'"),
                                            ("Ś", "S'"),
                                            ("ṭ", "t,"),
                                            ("Ṭ", "T,"),
                                            ("ū", "u"),
                                            ("Ū", "U"),
                                            ("ȗ", "u"),
                                            ("Ȗ", "U"),
                                            ("†", "x"),
                                            ("ₓ", "x2"),
                                            ("ₓ", "X2"),
                                            ("₀", "0"),
                                            ("₁", "1"),
                                            ("₂", "2"),
                                            ("₃", "3"),
                                            ("₄", "4"),
                                            ("₅", "5"),
                                            ("₆", "6"),
                                            ("₇", "7"),
                                            ("₈", "8"),
                                            ("₉", "9"),
                                        ] + unicode_en_to_ascii_en_replacements

cdli_inconsistencies = {  # this cost me a lot of time.
    "sumun2": "sun2",
}
unicode_atf_to_ascii_atf_token_replacements = {

    "GIR₃": "GIRI3",
    "ŋiri₂": "gir2",
    "IR₃": "ARAD2",
    "ti₇": "te",
    "GÁN": "GAN2",
    "sá": "sa2",
    "sìla": "sila3",
    "lú": "lu2",
    "gur₇": "guru7",
    "taka₄": "tak4",
    "líd": "lid2",
    "zíd": "zi3",
    "teŋ₄": "ti",
    "šaru": "szar'u",
    "úš": "us2",
    "giggi": "kukku5",
    "sag₁₀": "saga",
    "gurum": "gur2",
    "aḫ₃": "had2",
    "tu₄": "tum",
    "gab₂": "kab",
    "zid": "zi",
    "bán": "ban2",
    "buru": "bur'u",
    "èše": "esze3",
    "géš": "gesz2",
    "šár": "szar2",
    "bùr": "bur3",
    "dug₄": "du11",
    "diŋir": "dingir",
    "àm": "am3",
    "íb": "ib2",
    "íl": "il2",
    "kùš": "kusz3",
    "kug": "ku3",
    "sig₁₀": "si3",
    "zid₂": "zi3",
    "gud": "gu4",
    "bí": "bi2",
    "su₁₃": "su3",
    "tum₁₂": "tu",
    "GEME₂": "dam",
    "šag₄": "sza3",
    "kud": "ku5",
}

blank_string = [
    "(blank)",
    "($blank$)",
    "($ blank $)",
    "(blank space)",
    "((blank space))",
    "($blank space$)",
    "($ blank space $)",
    "(space)",
    "( space )",
    "($space$)",
    "($ space $)",
    "((traces))",
    "(traces)",
    "($traces$)",
    "($ traces $)",
    "((lost))",
    "($lost$)",
    "($ lost $)",
]

li_start_re = re.compile(
    r"^\[?_?\d+(/\d+)?\((asz|ban2|barig|disz|gesz2|iku|u)\)\]?")  # just got this from chatgpt and it works. hopefully.

underline_sign_names_re = re.compile(r"\b([A-Z][A-Z0-9#\. &]*[A-Z0-9#])")

en_index_ignore_words = set([
    "#tren", "&", "-", "--", "xxx", "—", "x",
    "in", "the", "were",
    "of", "and", "to", "if", "or", "for", "let", "but", "then",
    "a", "is", "was", "all", "an", "are", "am", "as",
    "at", "be", "by", "do", "did", "does", "from", "had",
    "has", "have", "he", "her", "him", "his", "i", "in",
    "i", "my", "me",
    "you", "your", "he",
    "his", "she", "her", "him",
    "it", "we", "our",
    "us", "they", "their",
    "them", "this", "that",
    "these", "those", "here",
    "there", "which", "who",
    "whom", "whose", "what",
    "when", "where", "why",
    "how", "be", "have", "had", "has",
    "do", "did", "done",
    "can", "could", "will",
    "would", "shall", "should",
    "may", "might", "must",
    "for", "with", "from",
    "not", "on", "as", "no",
    "its", "by", "at", "together", "also", "around",
    "out", "into", "about", "over", "up", "down",
    "off", "after", "under", "again", "further",
    "come", "go", "went", "gone", "went", "goes",
    "built", "made", "make", "makes", "making",
])


def replace_unsupported_atf(text):
    r = text
    for s, t in unicode_atf_to_ascii_atf_replacements:
        r = r.replace(s, t)
    return r


def replace_unsupported(text: str, language: str):
    if language == "en":
        return replace_unsupported_en(text)
    else:
        return replace_unsupported_atf(text)


def replace_unsupported_en(text):
    r = text
    for s, t in unicode_en_to_ascii_en_replacements:
        r = r.replace(s, t)
    return r


cuneiform_unicode = json.loads(
    requests.get("https://github.com/darth-cheney/cuneiform-signs-unicode/raw/master/cuneiform-unicode.json").text)[
    "signs"]

cuneiform_unicode_replacements = {x["value"].lower(): x["character"] for x in cuneiform_unicode}


def cuneiform_text_to_unicode(atf_text, language):
    words = atf_text.split(" ")
    for i, word in enumerate(words):
        lemmas = split_cuneiform_word(word)
        for j, lemma in enumerate(lemmas):
            lemma = lemma.lower()
            if lemma in cuneiform_unicode_replacements:
                lemmas[j] = cuneiform_unicode_replacements[lemma]
        words[i] = "".join(lemmas)
    return " ".join(words)


def split_cuneiform_word(word):
    parts = [""]
    for c in word:
        if c == "{" or c == "}":
            parts.append(c)
            parts.append("")
        elif c == "-" or c == "#" or c == "_":
            parts.append("")
        else:
            parts[-1] = parts[-1] + c
    return [p for p in parts if len(p) > 0]


def underline_sign_names_repl(match):
    return '_' + match.group(1).lower() + '_'


def underline_sign_names(text):
    #     return text
    return underline_sign_names_re.sub(underline_sign_names_repl, text).replace(".", "-")


def remove_extraneous_space(s):
    return " ".join(x for x in s.split(" ") if len(x) > 0)


def target_ok(target_text):
    if len(target_text) == 0:
        return False
    if len(set(target_text.replace(" ", ""))) < 2:
        return False
    if "o translation warranted" in target_text:
        return False
    if "o translation possible" in target_text:
        return False
    if "oo fragmentary for translation" in target_text:
        return False
    return True


def remove_blanks(s):
    for b in blank_string:
        s = s.replace(b, "")
    return s


def dashes_to_dots(s):
    return s.replace("[---]", "[...]").replace("[---", "[...").replace("---]", "...]").replace("---", "...")


def looks_like_li(line, lang):
    return li_start_re.match(line)


def unicode_words_to_normalized_ascii(tokens):
    def proc_token(token):
        if token in unicode_atf_to_ascii_atf_token_replacements:
            return unicode_atf_to_ascii_atf_token_replacements[token]
        token = replace_unsupported_atf(token)
        return token

    retokenized = "".join(proc_token(x) for x in tokens)
    return retokenized.strip()


def replace_quotes(text):
    return text.replace("“", "\"").replace("”", "\"").replace("‟", "\"").replace("’", "'").replace("‘", "'").replace(
        "‛", "'").replace("„", "\"").replace("´", "'").replace("ˊ", "'")


def replace_spaces(text):
    return text.replace("\n", " ").replace("\t", " ").replace("\u00a0", " ").replace("\u0005", "").replace("\u0015",
                                                                                                           "").replace(
        "\u2060", " ").replace("\u202c", " ").replace("\u202f", " ").replace("\ufeff", "").replace("\u2006",
                                                                                                   "").replace("\\1",
                                                                                                               "")


def count_suffix_repeats(text, suffix_length):
    if suffix_length > len(text):
        return 0
    suffix = text[-suffix_length:]
    # print("suffix", repr(suffix))
    count = 0
    index = len(text) - suffix_length
    while index >= 0 and text[index:(index + suffix_length)] == suffix:
        count += 1
        index -= suffix_length
    return count


def get_longest_suffix_repeat(text):
    histogram = defaultdict(int)
    for suffix_length in range(1, min(16, len(text))):
        histogram[suffix_length] = count_suffix_repeats(text, suffix_length)
    # print(histogram)
    return max(histogram.items(), key=lambda x: x[1])


def remove_suffix_repeats(text):
    if len(text) < 16:
        return text
    longest_length, longest_count = get_longest_suffix_repeat(text)
    if longest_count < 2:
        return text
    return text[:-(longest_length * (longest_count - 1))]


def test_remove_suffix_repeats(text):
    print("I:", text, "\nO:", remove_suffix_repeats(text))


def prep_src_for_nn(src, lang, corpus_id):
    src = replace_quotes(src)
    src = replace_spaces(src)
    src = remove_blanks(src)
    src = underline_sign_names(src)
    src = dashes_to_dots(src)
    src = src.replace("{", "(").replace("}", ")").replace("<", "(").replace(">", ")")
    src = src.replace("~", "-")
    src = replace_unsupported_atf(src)
    src = remove_extraneous_space(src)
    return src


def prep_tgt_for_nn(tgt, lang, corpus_id):
    tgt = replace_quotes(tgt)
    tgt = replace_spaces(tgt)
    tgt = remove_blanks(tgt)
    tgt = tgt.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("<", "").replace(">",
                                                                                                           "").replace(
        "{", "").replace("}", "").replace("‹", "").replace("›", "")
    tgt = tgt.replace("~", "").replace("§", "")
    tgt = replace_unsupported_en(tgt)
    tgt = remove_extraneous_space(tgt)
    return tgt
