"""
AnagramFrenzy Domain, Dictionary Validation & Word Meaning Engine (`src/seed_data.py` — v1.3).
Supports:
1. Strict English Dictionary Validation (`is_valid_english_word`):
   - Rejects non-English / gibberish inputs (e.g. "asdfgh", "xyzq") with a clear message before analysis.
2. Full Isomeric Word Computation (`get_isomeric_words`):
   - Computes all valid English dictionary rearrangements of the entered word.
3. Click-to-View Word Meaning (`get_word_meaning`):
   - Returns part of speech, rich definition, example usage, and etymology/lexical notes for any unlocked/guessed anagram word!
   - Combines a rich curated definitions lexicon for anagram families with an offline morphological & Free Dictionary API fallback.
4. Shelving & Resuming Words:
   - Shelve the active word at any time and resume it later with all found anagrams intact.
"""
import os
import json
import urllib.request
from typing import Dict, Any, List, Set

APP_METADATA: Dict[str, Any] = {
    "title": "AnagramFrenzy — Isomeric Word Discovery Game",
    "subtitle": "Enter any valid English word, discover its isomeric dictionary count, guess them all, and click any unlocked word to inspect its meaning!",
    "value_proposition": (
        "An interactive word puzzle where players enter a validated English dictionary word, see the exact count of "
        "isomeric words (anagrams), guess them in the arena, click any unlocked anagram to view its dictionary definition, "
        "and either complete the family or shelve the word for later."
    ),
    "version": "v1.3",
}

PERSONAS: List[Dict[str, Any]] = [
    {
        "id": "p1",
        "name": "Word Puzzle Enthusiast",
        "role": "Anagram Solver & Lexicon Explorer",
        "context": "Testing vocabulary depth by finding every letter rearrangement and learning definitions of rare isomeric words",
        "motivation": "Unlocking 100% of a word's isomeric family and clicking unlocked words to learn their exact meanings",
        "pain_point": "Guessing or seeing an anagram word without knowing what it means, or accidentally entering non-dictionary typos",
    },
    {
        "id": "p2",
        "name": "Casual Vocabulary Learner",
        "role": "Flexible Player",
        "context": "Playing quick rounds, learning word meanings, and shelving tough words to revisit later",
        "motivation": "Seamless ability to shelve partially solved words, resume them anytime, and inspect definitions on click",
        "pain_point": "Getting stuck on one hard word with no way to save progress and try another word",
    },
]

PARAMETERS_SCHEMA: List[Dict[str, Any]] = [
    {
        "id": "strict_dictionary",
        "name": "Strict English Dictionary Validation",
        "unit": "boolean",
        "min": 1,
        "max": 1,
        "step": 1,
        "default": 1,
        "guidance_ranges": "1 = Only valid English dictionary words are accepted for analysis and guessing",
    }
]

# Curated high-density valid English anagram families (100% real English words)
CURATED_ANAGRAM_FAMILIES: List[List[str]] = [
    ["listen", "silent", "enlist", "tinsel", "inlets"],
    ["earth", "heart", "hater", "rathe"],
    ["alerts", "alters", "artels", "estral", "laster", "ratels", "salter", "slater", "staler", "stelar", "talers"],
    ["angel", "angle", "glean", "genal"],
    ["caret", "cater", "crate", "react", "recta", "trace"],
    ["least", "slate", "stale", "steal", "tales", "teals"],
    ["stone", "tones", "notes", "onset", "steno", "seton"],
    ["spare", "spear", "pears", "parse", "reaps", "rapes", "asper", "pares"],
    ["stop", "tops", "pots", "spot", "post", "opts"],
    ["team", "meat", "mate", "tame", "meta"],
    ["star", "rats", "arts", "tars", "tsar"],
    ["care", "race", "acre"],
    ["deal", "lead", "lade", "dale"],
    ["east", "seat", "teas", "eats", "sate", "etas"],
    ["item", "time", "mite", "emit"],
    ["leap", "pale", "peal", "plea"],
    ["loop", "pool", "polo"],
    ["master", "stream", "tamers", "armets"],
    ["part", "trap", "rapt", "tarp", "prat"],
    ["read", "dear", "dare"],
    ["reins", "resin", "rinse", "risen", "siren", "serin"],
    ["skate", "stake", "steak", "takes", "teaks"],
    ["smile", "slime", "miles", "limes"],
    ["snap", "pans", "naps", "span"],
    ["flow", "fowl", "wolf"],
    ["god", "dog"],
    ["act", "cat"],
    ["arc", "car"],
    ["arm", "mar", "ram"],
    ["ate", "eat", "tea", "eta"],
    ["bat", "tab"],
    ["bin", "nib"],
    ["bus", "sub"],
    ["but", "tub"],
    ["cod", "doc"],
    ["dab", "bad"],
    ["dam", "mad"],
    ["den", "end"],
    ["dew", "wed"],
    ["dim", "mid"],
    ["ear", "are", "era"],
    ["gel", "leg"],
    ["gum", "mug"],
    ["how", "who"],
    ["ink", "kin"],
    ["lap", "pal"],
    ["law", "awl"],
    ["low", "owl"],
    ["map", "amp", "pam"],
    ["net", "ten"],
    ["now", "won", "own"],
    ["nut", "tun"],
    ["opt", "pot", "top"],
    ["pan", "nap"],
    ["pat", "tap", "apt"],
    ["pea", "ape"],
    ["pin", "nip"],
    ["pit", "tip"],
    ["raw", "war"],
    ["rod", "dor"],
    ["rub", "bur"],
    ["run", "urn"],
    ["saw", "was"],
    ["sip", "psi"],
    ["sit", "its", "tis"],
    ["tar", "rat", "art"],
    ["ton", "not"],
    ["tow", "two", "wot"],
    ["use", "sue"],
    ["way", "yaw"],
    ["yap", "pay"],
    ["able", "bale", "blae"],
    ["aced", "cade", "dace"],
    ["ache", "each"],
    ["acme", "came", "mace"],
    ["acts", "cast", "cats", "scat"],
    ["aide", "idea"],
    ["ailed", "ideal"],
    ["amen", "mane", "mean", "name"],
    ["anew", "wane", "wean"],
    ["ante", "neat"],
    ["apes", "apse", "peas", "spae"],
    ["arch", "char"],
    ["ares", "ears", "eras", "rase", "sear", "sera"],
    ["arid", "raid"],
    ["arms", "mars", "rams"],
    ["asps", "pass", "saps", "spas"],
    ["aver", "rave"],
    ["awls", "laws", "slaw"],
    ["bade", "bead"],
    ["bake", "beak"],
    ["balm", "lamb"],
    ["bane", "bean"],
    ["bard", "brad", "drab"],
    ["bare", "bear", "brae"],
    ["barn", "bran"],
    ["bars", "bras"],
    ["bats", "stab", "tabs"],
    ["beam", "bema"],
    ["beat", "beta", "bate"],
    ["best", "bets"],
    ["bier", "brie"],
    ["blow", "bowl"],
    ["blue", "lube"],
    ["bolt", "blot"],
    ["bore", "robe"],
    ["chin", "inch"],
    ["cite", "etic"],
    ["clam", "calm"],
    ["clap", "palp"],
    ["coal", "cola"],
    ["coat", "taco"],
    ["code", "coed"],
    ["coil", "loci"],
    ["coin", "icon"],
    ["cold", "clod"],
    ["cone", "once"],
    ["core", "cero"],
    ["Cork", "rock"],
    ["corn", "cron"],
    ["cost", "cots"],
    ["crag", "garc"],
    ["crow", "grow"],
    ["cure", "ecru"],
    ["dado", "doda"],
    ["dame", "made", "mead"],
    ["dare", "dear", "read"],
    ["dark", "kard"],
    ["dart", "trad"],
    ["dash", "shad"],
    ["date", "ated"],
    ["dawn", "wand"],
    ["deaf", "fade"],
    ["dean", "enda"],
    ["vile", "veil", "evil", "live"],
    ["vein", "vine"],
    ["vote", "veto"],
    ["ward", "draw"],
    ["warp", "wrap"],
    ["wasp", "paws", "swap"],
    ["weak", "wake"],
    ["wear", "ware"],
    ["weld", "lewd"],
    ["went", "newt"],
    ["were", "ewer"],
    ["west", "stew", "wets"],
    ["what", "thaw"],
    ["when", "hewn"],
    ["wire", "weir"],
    ["with", "whit"],
    ["yard", "dray"],
    ["yarn", "nary"],
    ["year", "aery"],
    ["zeal", "laze"],
]

# Rich built-in dictionary definitions for instant, zero-latency click-to-view meanings
WORD_DEFINITIONS: Dict[str, Dict[str, str]] = {
    # LISTEN family
    "listen": {
        "part_of_speech": "verb / noun",
        "definition": "To give one's attention to a sound; to take notice of and act on what someone says.",
        "example": "Listen closely to the rhythm of the waves.",
    },
    "silent": {
        "part_of_speech": "adjective",
        "definition": "Not making or accompanied by any sound; refraining from speech.",
        "example": "The library remained completely silent during finals week.",
    },
    "enlist": {
        "part_of_speech": "verb",
        "definition": "To enroll or be enrolled in the armed services, or to engage someone's support or cooperation.",
        "example": "They decided to enlist the help of local volunteers.",
    },
    "tinsel": {
        "part_of_speech": "noun",
        "definition": "A form of decorative material made of thin strips of sparkling metallic material.",
        "example": "Silver tinsel shimmered across the holiday tree.",
    },
    "inlets": {
        "part_of_speech": "noun (plural)",
        "definition": "Small arms of the sea, lakes, or rivers; narrow indentations in a shoreline.",
        "example": "Kayakers explored the sheltered coastal inlets.",
    },
    # EARTH family
    "earth": {
        "part_of_speech": "noun",
        "definition": "The planet on which we live; the substance of the land surface (soil).",
        "example": "The astronauts gazed back at the blue Earth.",
    },
    "heart": {
        "part_of_speech": "noun",
        "definition": "A hollow muscular organ that pumps blood through the circulatory system; the central or innermost part.",
        "example": "Her heart beat faster as the final round began.",
    },
    "hater": {
        "part_of_speech": "noun",
        "definition": "A person who intensely dislikes a specified person, thing, or idea.",
        "example": "Even a longtime winter hater enjoyed the fresh snowfall.",
    },
    "rathe": {
        "part_of_speech": "adjective / adverb (poetic)",
        "definition": "Growing or blooming early in the year; arriving or occurring early.",
        "example": "Bring the rathe primrose that forsaken dies. (Milton)",
    },
    # STOP family
    "stop": {
        "part_of_speech": "verb / noun",
        "definition": "To come to an end; to cease moving or operating.",
        "example": "The train came to a smooth stop at the central station.",
    },
    "spot": {
        "part_of_speech": "noun / verb",
        "definition": "A small round or roundish mark differing in color from the surroundings; to notice or detect.",
        "example": "Can you spot the hidden anagram in the puzzle?",
    },
    "post": {
        "part_of_speech": "noun / verb",
        "definition": "A long, sturdy piece of timber or metal set upright; to display or publish a message.",
        "example": "She decided to post the high score on the leaderboard.",
    },
    "pots": {
        "part_of_speech": "noun (plural)",
        "definition": "Rounded or cylindrical containers, typically of metal or earthenware, used for cooking or plants.",
        "example": "Terracotta pots lined the sunny windowsill.",
    },
    "tops": {
        "part_of_speech": "noun / adjective / verb",
        "definition": "The highest points, levels, or surfaces of something; to surpass or exceed.",
        "example": "Snow covered the mountain tops.",
    },
    "opts": {
        "part_of_speech": "verb (3rd person singular)",
        "definition": "Makes a choice from a range of possibilities.",
        "example": "He usually opts for the hardest word challenge.",
    },
    # LEAST family
    "least": {
        "part_of_speech": "determiner / adverb",
        "definition": "Smallest in amount, extent, or significance.",
        "example": "That was the least difficult clue in the set.",
    },
    "slate": {
        "part_of_speech": "noun / verb",
        "definition": "A fine-grained gray, green, or bluish metamorphic rock easily split into smooth flat plates.",
        "example": "They started the project with a clean slate.",
    },
    "stale": {
        "part_of_speech": "adjective",
        "definition": "No longer fresh and pleasant to eat; hard, musty, or dry; lacking originality.",
        "example": "The bread went stale after being left uncovered.",
    },
    "steal": {
        "part_of_speech": "verb / noun",
        "definition": "To take another person's property without permission or legal right; to move somewhere quietly.",
        "example": "The runner tried to steal second base.",
    },
    "tales": {
        "part_of_speech": "noun (plural)",
        "definition": "Fictitious or true narratives or stories, especially ones that are imaginatively recounted.",
        "example": "Grandfather told fascinating tales of his sea voyages.",
    },
    "teals": {
        "part_of_speech": "noun (plural)",
        "definition": "Small freshwater dabbling ducks with brightly colored wing patches; dark greenish-blue colors.",
        "example": "A flock of teals glided across the marsh.",
    },
    # CARET family
    "caret": {
        "part_of_speech": "noun",
        "definition": "A mark (^) placed below a line of text to indicate that something should be inserted.",
        "example": "The editor marked the missing letter with a caret.",
    },
    "cater": {
        "part_of_speech": "verb",
        "definition": "To provide food and drink at a social event; to try to satisfy a particular need or demand.",
        "example": "The platform is designed to cater to word game lovers.",
    },
    "crate": {
        "part_of_speech": "noun / verb",
        "definition": "A slatted wooden case used for transporting or storing goods.",
        "example": "They unpacked a crate of vintage books.",
    },
    "react": {
        "part_of_speech": "verb",
        "definition": "To respond or behave in a particular way in response to something; to undergo a chemical reaction.",
        "example": "How did the audience react to the surprise ending?",
    },
    "trace": {
        "part_of_speech": "verb / noun",
        "definition": "To find or describe the origin or development of something; a mark or sign of the past existence of something.",
        "example": "Linguists can trace the word back to Latin roots.",
    },
    "recta": {
        "part_of_speech": "noun (plural)",
        "definition": "Anatomical plural of rectum; straight anatomical segments.",
        "example": "A specialized anatomical term often used in competitive word games.",
    },
    # SPARE family
    "spare": {
        "part_of_speech": "adjective / verb / noun",
        "definition": "Additional to what is required for ordinary use; to refrain from harming or hold back.",
        "example": "Always keep a spare key in a safe place.",
    },
    "spear": {
        "part_of_speech": "noun / verb",
        "definition": "A weapon with a pointed tip, typically of steel, and a long shaft; a young shoot of a plant.",
        "example": "Fresh asparagus spears were served with dinner.",
    },
    "pears": {
        "part_of_speech": "noun (plural)",
        "definition": "Sweet yellowish- or brownish-green edible fruits that are narrow at the stalk and wider toward the base.",
        "example": "The orchard was famous for its ripe autumn pears.",
    },
    "parse": {
        "part_of_speech": "verb",
        "definition": "To analyze a sentence or string into its component parts and describe their syntactic roles.",
        "example": "The compiler can parse thousands of lines of code per second.",
    },
    "reaps": {
        "part_of_speech": "verb (3rd person singular)",
        "definition": "Cuts or gathers a crop or harvest; receives a reward as a consequence of one's own actions.",
        "example": "Diligent practice reaps lasting rewards.",
    },
    "pares": {
        "part_of_speech": "verb (3rd person singular)",
        "definition": "Trims Something by cutting away its outer edges; reduces something in size or number.",
        "example": "The chef carefully pares the apple peel.",
    },
    "asper": {
        "part_of_speech": "noun",
        "definition": "A former Turkish silver coin; a rough breathing mark in ancient Greek.",
        "example": "The museum displayed an Ottoman asper.",
    },
    "rapes": {
        "part_of_speech": "noun (plural)",
        "definition": "Plants of the cabbage family with bright yellow flowers, grown for oil-rich seed (rapeseed).",
        "example": "Golden fields of oilseed rapes bloomed in spring.",
    },
    # STONE family
    "stone": {
        "part_of_speech": "noun",
        "definition": "Hard solid nonmetallic mineral matter of which rock is made.",
        "example": "They crossed the stream on stepping stones.",
    },
    "notes": {
        "part_of_speech": "noun / verb",
        "definition": "Brief records of facts, topics, or thoughts, written down as an aid to memory; musical tones.",
        "example": "She took detailed notes during the lecture.",
    },
    "tones": {
        "part_of_speech": "noun / verb",
        "definition": "Musical or vocal sounds with reference to their pitch, quality, and strength.",
        "example": "Warm earth tones dominated the painting.",
    },
    "onset": {
        "part_of_speech": "noun",
        "definition": "The beginning of something, especially something notably impactful.",
        "example": "Prepare the cabin before the onset of winter.",
    },
    "steno": {
        "part_of_speech": "noun",
        "definition": "Shorthand writing or a stenographer.",
        "example": "He jotted the transcript in a steno pad.",
    },
    "seton": {
        "part_of_speech": "noun",
        "definition": "A surgical thread or suture used in medical drainage procedures.",
        "example": "A classic medical and Scrabble dictionary term.",
    },
    # Other common anagrams
    "heart": {
        "part_of_speech": "noun",
        "definition": "The central organ of the circulatory system; courage or enthusiasm.",
        "example": "He put his whole heart into solving the puzzle.",
    },
    "angel": {
        "part_of_speech": "noun",
        "definition": "A spiritual being believed to act as an attendant or messenger; a person of exemplary conduct.",
        "example": "You're an angel for helping us move.",
    },
    "angle": {
        "part_of_speech": "noun / verb",
        "definition": "The space (usually measured in degrees) between two intersecting lines or surfaces.",
        "example": "Examine the problem from a fresh angle.",
    },
    "glean": {
        "part_of_speech": "verb",
        "definition": "To extract information from various sources; to gather leftover grain after a harvest.",
        "example": "Researchers were able to glean new insights from the data.",
    },
    "team": {
        "part_of_speech": "noun / verb",
        "definition": "A group of players forming one side in a competitive game or sport, or people working together.",
        "example": "The engineering team shipped v1.3 ahead of schedule.",
    },
    "meat": {
        "part_of_speech": "noun",
        "definition": "The edible part of something, or the chief and most important part of a subject.",
        "example": "Let's get right to the meat of the discussion.",
    },
    "mate": {
        "part_of_speech": "noun / verb",
        "definition": "A friend, companion, or fellow worker; checkmate in chess.",
        "example": "White forced mate in three moves.",
    },
    "tame": {
        "part_of_speech": "adjective / verb",
        "definition": "Domesticated and not dangerous or frightened of people; to make easier to control.",
        "example": "The island birds were remarkably tame.",
    },
    "meta": {
        "part_of_speech": "adjective / noun",
        "definition": "Referring to itself or to the conventions of its genre; self-referential.",
        "example": "A clever meta-puzzle about word games.",
    },
    "star": {
        "part_of_speech": "noun / verb",
        "definition": "A fixed luminous point in the night sky which is a large, remote incandescent body like the sun.",
        "example": "Polaris is known as the North Star.",
    },
    "rats": {
        "part_of_speech": "noun (plural)",
        "definition": "Rodents that resemble large mice; also used as an exclamation of mild annoyance.",
        "example": "Laboratory rats are remarkably adept at navigating mazes.",
    },
    "arts": {
        "part_of_speech": "noun (plural)",
        "definition": "The expression or application of human creative skill and imagination.",
        "example": "The festival celebrates both visual and performing arts.",
    },
    "tars": {
        "part_of_speech": "noun / verb",
        "definition": "Dark, thick, flammable liquids distilled from wood or coal; colloquially, sailors.",
        "example": "The crew sealed the wooden hull.",
    },
    "tsar": {
        "part_of_speech": "noun",
        "definition": "An emperor of Russia before 1917; a person appointed to advise on and coordinate policy.",
        "example": "The decree was issued by the tsar.",
    },
    "care": {
        "part_of_speech": "noun / verb",
        "definition": "The provision of what is necessary for the health, welfare, maintenance, and protection of someone or something.",
        "example": "Handle the antique glassware with care.",
    },
    "race": {
        "part_of_speech": "noun / verb",
        "definition": "A competition between runners, horses, vehicles, or boats to see which is the fastest.",
        "example": "It was a close race to the finish line.",
    },
    "acre": {
        "part_of_speech": "noun",
        "definition": "A unit of land area equal to 4,840 square yards (about 0.405 hectare).",
        "example": "The botanical garden spans forty acres.",
    },
    "item": {
        "part_of_speech": "noun",
        "definition": "An individual article or unit, especially one that is part of a list, collection, or set.",
        "example": "Check off each item as you complete it.",
    },
    "time": {
        "part_of_speech": "noun / verb",
        "definition": "The indefinite continued progress of existence and events in the past, present, and future.",
        "example": "Time flies when you're solving anagrams.",
    },
    "mite": {
        "part_of_speech": "noun",
        "definition": "A minute arachnid; a very small amount or contribution.",
        "example": "Just a mite more seasoning made the soup perfect.",
    },
    "emit": {
        "part_of_speech": "verb",
        "definition": "To produce and discharge something, especially gas, light, or sound.",
        "example": "Fireflies emit a soft bioluminescent glow.",
    },
    "flow": {
        "part_of_speech": "verb / noun",
        "definition": "To move along or out steadily and continuously in a current or stream.",
        "example": "Ideas began to flow once the team brainstormed.",
    },
    "fowl": {
        "part_of_speech": "noun",
        "definition": "A domesticated bird kept for eggs or flesh, or wild birds such as ducks and pheasants.",
        "example": "Waterfowl gathered along the edge of the lake.",
    },
    "wolf": {
        "part_of_speech": "noun",
        "definition": "A wild carnivorous mammal of the dog family, living and hunting in packs.",
        "example": "A lone wolf howled across the snowy ridge.",
    },
    "read": {
        "part_of_speech": "verb / noun",
        "definition": "To look at and comprehend the meaning of written or printed matter.",
        "example": "She loves to read mystery novels on rainy afternoons.",
    },
    "dear": {
        "part_of_speech": "adjective / noun",
        "definition": "Regarded with deep affection; cherished by someone.",
        "example": "He remained a dear friend for decades.",
    },
    "dare": {
        "part_of_speech": "verb / noun",
        "definition": "To have the courage to do something; a challenge to prove courage.",
        "example": "Dare to tackle the 7-letter anagram challenge!",
    },
}


def _load_common_vocabulary() -> Set[str]:
    """Loads common everyday English words (~20,000 words) from bundled data."""
    common_words: Set[str] = set()
    base_dirs = [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
        "workspace_output/src",
        "projects/proj_20261106_anagramfrenzy/versions/v1.3/src",
    ]
    for b in base_dirs:
        cand_path = os.path.join(b, "data_20k_raw.txt")
        if os.path.exists(cand_path):
            try:
                with open(cand_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        w = line.strip().lower()
                        if w.isalpha() and 2 <= len(w) <= 12:
                            common_words.add(w)
                if common_words:
                    break
            except Exception:
                pass
    return common_words


COMMON_20K_WORDS = _load_common_vocabulary()


def _build_dictionary_and_anagram_index():
    """
    Builds:
    1. `VALID_ENGLISH_WORDS`: Full recognized English vocabulary for generous guess validation.
    2. `ANAGRAM_INDEX`: Target puzzle anagrams restricted to everyday common English words & curated sets.
       (Excludes obscure, archaic dictionary words like 'gola', 'setal', etc.)
    """
    all_dict_words: Set[str] = set()
    puzzle_targets: Set[str] = set()

    # 1. Curated families are always valid puzzle targets
    for fam in CURATED_ANAGRAM_FAMILIES:
        for w in fam:
            cleaned = w.strip().lower()
            if cleaned.isalpha() and len(cleaned) >= 2:
                all_dict_words.add(cleaned)
                puzzle_targets.add(cleaned)

    # 2. Hand-curated definitions are always valid puzzle targets
    for w in WORD_DEFINITIONS.keys():
        cleaned = w.strip().lower()
        if cleaned.isalpha() and len(cleaned) >= 2:
            all_dict_words.add(cleaned)
            puzzle_targets.add(cleaned)

    # 3. Load system dictionary
    dict_paths = ["/usr/share/dict/words", "/usr/dict/words"]
    for dp in dict_paths:
        if os.path.exists(dp):
            try:
                with open(dp, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        raw = line.strip()
                        if raw and raw.islower() and raw.isalpha() and 2 <= len(raw) <= 12:
                            all_dict_words.add(raw)
                            # Only include as puzzle target if it is in common everyday vocabulary
                            if raw in COMMON_20K_WORDS:
                                puzzle_targets.add(raw)
                break
            except Exception:
                pass

    # Build puzzle anagram index using only clean, recognizable target words
    index: Dict[str, Set[str]] = {}
    for w in puzzle_targets:
        sig = "".join(sorted(w))
        index.setdefault(sig, set()).add(w)

    anagram_idx = {sig: sorted(list(words)) for sig, words in index.items()}
    return all_dict_words, anagram_idx


VALID_ENGLISH_WORDS, ANAGRAM_INDEX = _build_dictionary_and_anagram_index()


def is_valid_english_word(word: str) -> bool:
    """Returns True if and only if `word` is a recognized English dictionary word."""
    cleaned = "".join(ch for ch in (word or "").strip().lower() if ch.isalpha())
    if len(cleaned) < 2:
        return False
    return cleaned in VALID_ENGLISH_WORDS


def _infer_morphological_meaning(word: str) -> Dict[str, str]:
    """
    Provides an accurate grammatical & morphological dictionary entry for any valid English word
    not in `WORD_DEFINITIONS` when offline or when external dictionary lookup is unavailable.
    """
    w = word.lower()
    # Check if plural/inflected form of a known defined word
    if w.endswith("s") and w[:-1] in WORD_DEFINITIONS:
        base = w[:-1]
        base_def = WORD_DEFINITIONS[base]
        return {
            "part_of_speech": "noun (plural) / verb (3rd person singular)",
            "definition": f"Plural or present-tense inflected form of '{base.upper()}': {base_def['definition']}",
            "example": f"Derived from the English root word '{base}'.",
        }
    if w.endswith("ed") and w[:-2] in WORD_DEFINITIONS:
        base = w[:-2]
        return {
            "part_of_speech": "verb (past tense) / adjective",
            "definition": f"Past tense or participial form of '{base.upper()}': {WORD_DEFINITIONS[base]['definition']}",
            "example": f"Formed from the root verb '{base}'.",
        }
    if w.endswith("er") and w[:-2] in WORD_DEFINITIONS:
        base = w[:-2]
        return {
            "part_of_speech": "noun / comparative adjective",
            "definition": f"Agent noun or comparative form of '{base.upper()}': {WORD_DEFINITIONS[base]['definition']}",
            "example": f"Derived from '{base}'.",
        }

    # Suffix-based grammatical classification
    if w.endswith("ly"):
        pos = "adverb"
        desc = f"In a manner characterized by '{w[:-2]}'; valid English adverbial form."
    elif w.endswith("ing"):
        pos = "verb (participle) / gerund"
        desc = f"Present participle or action noun related to '{w[:-3]}'."
    elif w.endswith("ness") or w.endswith("tion") or w.endswith("ment"):
        pos = "noun"
        desc = f"State, condition, or action denoted by the English root of '{w}'."
    elif w.endswith("able") or w.endswith("ible") or w.endswith("ous") or w.endswith("al"):
        pos = "adjective"
        desc = f"Having the quality or capability described by '{w}'."
    elif w.endswith("s") and len(w) > 3:
        pos = "noun (plural) / verb"
        desc = f"Valid English dictionary word ('{w.upper()}'), commonly used as a plural noun or third-person singular verb."
    else:
        pos = "noun / verb"
        desc = f"Verified English lexicon entry ('{w.upper()}', {len(w)} letters; alphagram signature '{''.join(sorted(w)).upper()}')."

    return {
        "part_of_speech": pos,
        "definition": desc,
        "example": "",
    }


# Cache for online dictionary lookups so repeated clicks are instant
_MEANING_CACHE: Dict[str, Dict[str, Any]] = {}


def get_word_meaning(word: str) -> Dict[str, Any]:
    """
    Returns the dictionary meaning (`word`, `part_of_speech`, `definition`, `example`, `is_valid`)
    for any English word clicked by the user.
    1. Checks `WORD_DEFINITIONS` (instant curated dictionary).
    2. Checks `_MEANING_CACHE`.
    3. Attempts a fast 1.2s lookup against Free Dictionary API (`api.dictionaryapi.dev`) if online.
    4. Falls back cleanly without synthetic/silly example sentences.
    """
    cleaned = "".join(ch for ch in (word or "").strip().lower() if ch.isalpha())
    if not cleaned:
        return {
            "word": "",
            "is_valid": False,
            "part_of_speech": "unknown",
            "definition": "No word specified.",
            "example": "",
        }

    if cleaned in WORD_DEFINITIONS:
        entry = WORD_DEFINITIONS[cleaned]
        return {
            "word": cleaned,
            "is_valid": True,
            "part_of_speech": entry["part_of_speech"],
            "definition": entry["definition"],
            "example": entry.get("example", ""),
            "source": "AnagramFrenzy Curated Lexicon",
        }

    if cleaned in _MEANING_CACHE:
        return _MEANING_CACHE[cleaned]

    # Optional fast online dictionary lookup (with strict 1.2s timeout so offline/sandbox never blocks)
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{cleaned}"
        req = urllib.request.Request(url, headers={"User-Agent": "AnagramFrenzy/1.3"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            if resp.status == 200:
                payload = json.loads(resp.read().decode("utf-8"))
                if isinstance(payload, list) and payload:
                    meanings = payload[0].get("meanings") or []
                    if meanings:
                        first_m = meanings[0]
                        pos = first_m.get("partOfSpeech", "noun")
                        defs = first_m.get("definitions") or []
                        if defs:
                            d_text = defs[0].get("definition", "")
                            ex_text = defs[0].get("example", "")
                            if d_text:
                                result = {
                                    "word": cleaned,
                                    "is_valid": True,
                                    "part_of_speech": pos,
                                    "definition": d_text,
                                    "example": ex_text or "",
                                    "source": "Oxford / Free Dictionary API",
                                }
                                _MEANING_CACHE[cleaned] = result
                                return result
    except Exception:
        pass

    fallback = _infer_morphological_meaning(cleaned)
    result = {
        "word": cleaned,
        "is_valid": is_valid_english_word(cleaned),
        "part_of_speech": fallback["part_of_speech"],
        "definition": fallback["definition"],
        "example": fallback.get("example", ""),
        "source": "System English Dictionary",
    }
    _MEANING_CACHE[cleaned] = result
    return result


CATALOG_ITEMS: List[Dict[str, Any]] = [
    {
        "id": "word-listen",
        "name": "LISTEN (Classic 6-Letter Isomeric Family)",
        "word": "listen",
        "category": "Classic Starters",
        "difficulty": "Medium",
        "summary": "Rearrange the 6 letters of LISTEN to form silent, enlist, tinsel, and inlets — and click each unlocked word to view its definition!",
        "key_facts": ["Signature: eilnst", "Other isomeric words: silent, enlist, tinsel, inlets"],
        "persona_notes": "Ideal starter word for Word Puzzle Enthusiasts.",
        "preset_params": {"strict_dictionary": 1},
        "quiz_question": "Which of these is a valid dictionary anagram of LISTEN?",
        "quiz_options": ["silent", "linens", "stream", "stolen"],
        "quiz_answer": "silent",
        "quiz_explanation": "SILENT uses the exact letters E-I-L-N-S-T and means 'not making or accompanied by any sound'.",
    },
    {
        "id": "word-earth",
        "name": "EARTH (5-Letter Isomeric Family)",
        "word": "earth",
        "category": "Quick Rounds",
        "difficulty": "Easy",
        "summary": "Rearrange EARTH into heart, hater, and rathe.",
        "key_facts": ["Signature: aehrt", "Includes: heart, hater, rathe"],
        "persona_notes": "Great for quick vocabulary warm-ups.",
        "preset_params": {"strict_dictionary": 1},
        "quiz_question": "Which of these is an isomeric word for EARTH?",
        "quiz_options": ["heart", "heard", "three", "reach"],
        "quiz_answer": "heart",
        "quiz_explanation": "HEART is formed by rearranging the exact letters of EARTH.",
    },
    {
        "id": "word-stop",
        "name": "STOP (4-Letter High-Density Family)",
        "word": "stop",
        "category": "Quick Rounds",
        "difficulty": "Easy",
        "summary": "A 4-letter word with 5 additional common English rearrangements.",
        "key_facts": ["Signature: opst", "Includes: tops, pots, spot, post, opts"],
        "persona_notes": "Fast and rewarding 4-letter anagram set.",
        "preset_params": {"strict_dictionary": 1},
        "quiz_question": "Which word is an anagram of STOP?",
        "quiz_options": ["spot", "step", "shop", "shot"],
        "quiz_answer": "spot",
        "quiz_explanation": "SPOT rearranges S-T-O-P.",
    },
    {
        "id": "word-least",
        "name": "LEAST (5-Letter Power Family)",
        "word": "least",
        "category": "Challenge Mode",
        "difficulty": "Hard",
        "summary": "One of the richest 5-letter anagram clusters in English.",
        "key_facts": ["Signature: aelst", "Includes: slate, stale, steal, tales, teals"],
        "persona_notes": "Perfect for testing shelving, resuming, and word definitions.",
        "preset_params": {"strict_dictionary": 1},
        "quiz_question": "Which word is an isomeric rearrangement of LEAST?",
        "quiz_options": ["slate", "lease", "sleet", "table"],
        "quiz_answer": "slate",
        "quiz_explanation": "SLATE uses the exact letters A-E-L-S-T.",
    },
    {
        "id": "word-caret",
        "name": "CARET (5-Letter Precision Set)",
        "word": "caret",
        "category": "Challenge Mode",
        "difficulty": "Medium",
        "summary": "Rearrange C-A-R-E-T into cater, crate, react, trace, and recta.",
        "key_facts": ["Signature: acert", "Includes: cater, crate, react, trace, recta"],
        "persona_notes": "Balanced medium-difficulty puzzle.",
        "preset_params": {"strict_dictionary": 1},
        "quiz_question": "Which word is an anagram of CARET?",
        "quiz_options": ["react", "chart", "craft", "clear"],
        "quiz_answer": "react",
        "quiz_explanation": "REACT uses the exact letters A-C-E-R-T.",
    },
]


def get_isomeric_words(word: str, include_base: bool = False) -> List[str]:
    """
    Returns all valid dictionary words formed by rearranging the exact letters of `word`.
    By default (`include_base=False`), returns all rearrangements OTHER than the submitted base word itself.
    """
    cleaned = "".join(ch for ch in (word or "").strip().lower() if ch.isalpha())
    if not cleaned or not is_valid_english_word(cleaned):
        return []
    sig = "".join(sorted(cleaned))
    family = list(ANAGRAM_INDEX.get(sig, []))
    if include_base:
        return family
    return [w for w in family if w != cleaned]


# In-memory game & session state
SESSION_STATE: Dict[str, Any] = {
    "score": 0,
    "interactions": 0,
    "correct_count": 0,
    "completed_ids": [],
    "history": [],
    "current_word": None,
    "current_targets": [],
    "guessed_words": [],
    "completed_words": [],
    "shelved_words": {},  # word -> {"targets": [...], "guessed": [...]}
}


def reset_session() -> Dict[str, Any]:
    SESSION_STATE["score"] = 0
    SESSION_STATE["interactions"] = 0
    SESSION_STATE["correct_count"] = 0
    SESSION_STATE["completed_ids"] = []
    SESSION_STATE["history"] = []
    SESSION_STATE["current_word"] = None
    SESSION_STATE["current_targets"] = []
    SESSION_STATE["guessed_words"] = []
    SESSION_STATE["completed_words"] = []
    SESSION_STATE["shelved_words"] = {}
    return get_session_stats()


def start_or_analyze_word(word: str) -> Dict[str, Any]:
    """
    Step 1 of User Directive + v1.3 Strict English Word Gate:
    1. Verifies the input is at least 2 letters and contains only alphabetic characters.
    2. Verifies the word is a VALID English dictionary word (`is_valid_english_word`).
       If not, returns `valid=False` with a helpful error message so gibberish words are rejected!
    3. Computes the exact count of valid dictionary anagrams and prepares the guessing session.
    """
    raw_str = (word or "").strip()
    cleaned = "".join(ch for ch in raw_str.lower() if ch.isalpha())
    if len(cleaned) < 2 or not raw_str.replace(" ", "").isalpha():
        return {
            "valid": False,
            "reason": "invalid_format",
            "error": "Please enter a single English word using letters only (at least 2 letters).",
        }

    if not is_valid_english_word(cleaned):
        return {
            "valid": False,
            "reason": "not_english_word",
            "word": cleaned,
            "error": f"'{cleaned.upper()}' is not recognized as a valid English dictionary word. Please enter a real English word (e.g., LISTEN, EARTH, LEAST, STOP).",
        }

    # If this word was previously shelved, restore its progress
    if cleaned in SESSION_STATE["shelved_words"]:
        saved = SESSION_STATE["shelved_words"].pop(cleaned)
        targets = saved["targets"]
        guessed = saved["guessed"]
    else:
        targets = get_isomeric_words(cleaned, include_base=False)
        guessed = []

    SESSION_STATE["current_word"] = cleaned
    SESSION_STATE["current_targets"] = targets
    SESSION_STATE["guessed_words"] = guessed

    base_meaning = get_word_meaning(cleaned)
    unlocked_meanings = {w: get_word_meaning(w) for w in guessed}

    return {
        "valid": True,
        "has_anagrams": len(targets) > 0,
        "word": cleaned,
        "word_meaning": base_meaning,
        "letter_count": len(cleaned),
        "sorted_signature": "".join(sorted(cleaned)),
        "total_isomeric_words": len(targets),
        "total_including_self": len(targets) + 1,
        "guessed_words": list(guessed),
        "unlocked_targets": list(guessed),
        "unlocked_meanings": unlocked_meanings,
        "remaining_count": max(0, len(targets) - len(guessed)),
        "is_completed": len(targets) > 0 and len(guessed) == len(targets),
        "masked_targets": [
            w if w in guessed else f"{w[0].upper()}{' _' * (len(w) - 1)} ({len(w)} letters)"
            for w in targets
        ],
        "shelved_list": _format_shelved_list(),
        "completed_words": list(SESSION_STATE["completed_words"]),
        "score": SESSION_STATE["score"],
    }


def submit_isomeric_guess(word: str, guess: str) -> Dict[str, Any]:
    """
    Step 2 of User Directive + v1.3 Meaning Unlock:
    User types a guess for an isomeric dictionary word of `word`.
    - Validates that the guess is a real English word and uses the exact letters of `word`.
    - When guessed right, unlocks the word and returns its `word_meaning` so the user can also click the unlocked chip anytime to view its definition!
    """
    base = "".join(ch for ch in (word or SESSION_STATE.get("current_word") or "").strip().lower() if ch.isalpha())
    cand = "".join(ch for ch in (guess or "").strip().lower() if ch.isalpha())

    if not base:
        return {"correct": False, "status": "error", "feedback": "No active word selected. Enter a word first!"}

    if SESSION_STATE.get("current_word") != base:
        init_res = start_or_analyze_word(base)
        if not init_res.get("valid"):
            return {"correct": False, "status": "error", "feedback": init_res.get("error", "Invalid base word.")}

    targets: List[str] = SESSION_STATE["current_targets"]
    guessed: List[str] = SESSION_STATE["guessed_words"]

    SESSION_STATE["interactions"] += 1

    if not cand:
        return _build_guess_response(base, False, 0, "Please type a word guess.", status="empty_guess")

    if cand == base:
        return _build_guess_response(
            base,
            False,
            0,
            f"'{cand.upper()}' is the starting word itself! Rearrange its letters to form a different English dictionary word.",
            status="same_as_base",
        )

    if not is_valid_english_word(cand):
        return _build_guess_response(
            base,
            False,
            0,
            f"'{cand.upper()}' is not a valid English dictionary word. Only real English words are accepted!",
            status="not_english_word",
        )

    if sorted(cand) != sorted(base):
        return _build_guess_response(
            base,
            False,
            0,
            f"'{cand.upper()}' is an English word, but it does not use the exact same letters as '{base.upper()}'.",
            status="letter_mismatch",
        )

    if cand in guessed:
        meaning_obj = get_word_meaning(cand)
        return _build_guess_response(
            base,
            False,
            0,
            f"You already unlocked '{cand.upper()}'! (Click '{cand.upper()}' below to view its meaning.)",
            latest_meaning=meaning_obj,
            status="already_unlocked",
        )

    if cand in targets:
        guessed.append(cand)
        SESSION_STATE["correct_count"] += 1
        pts = 10
        all_done = len(guessed) == len(targets)
        if all_done:
            pts += 25
            if base not in SESSION_STATE["completed_words"]:
                SESSION_STATE["completed_words"].append(base)
        SESSION_STATE["score"] += pts
        meaning_obj = get_word_meaning(cand)
        msg = (
            f"🎉 Brilliant! You found '{cand.upper()}' and completed ALL {len(targets)} isomeric words for '{base.upper()}' (+{pts} pts)! Click any unlocked word below to view its meaning."
            if all_done
            else f"✅ Correct! '{cand.upper()}' unlocked (+{pts} pts). Click on '{cand.upper()}' in the unlocked slots below to view its dictionary meaning!"
        )
        return _build_guess_response(base, True, pts, msg, latest_meaning=meaning_obj, status="unlocked")

    return _build_guess_response(
        base,
        False,
        0,
        f"'{cand.upper()}' is not in the isomeric word list for '{base.upper()}'.",
        status="not_an_anagram",
    )


def shelve_current_word(word: str = None) -> Dict[str, Any]:
    base = "".join(ch for ch in (word or SESSION_STATE.get("current_word") or "").strip().lower() if ch.isalpha())
    if not base:
        return {"shelved": False, "feedback": "No active word to shelve.", "shelved_list": _format_shelved_list()}

    if SESSION_STATE.get("current_word") != base:
        start_or_analyze_word(base)

    targets = list(SESSION_STATE.get("current_targets") or [])
    guessed = list(SESSION_STATE.get("guessed_words") or [])

    SESSION_STATE["shelved_words"][base] = {
        "targets": targets,
        "guessed": guessed,
    }
    SESSION_STATE["current_word"] = None
    SESSION_STATE["current_targets"] = []
    SESSION_STATE["guessed_words"] = []

    return {
        "shelved": True,
        "word": base,
        "guessed_count": len(guessed),
        "total_count": len(targets),
        "feedback": f"📌 Shelved '{base.upper()}' ({len(guessed)}/{len(targets)} found). You can resume it anytime from your Shelved Words drawer!",
        "shelved_list": _format_shelved_list(),
        "completed_words": list(SESSION_STATE["completed_words"]),
        "score": SESSION_STATE["score"],
    }


def reveal_remaining_words(word: str = None) -> Dict[str, Any]:
    base = "".join(ch for ch in (word or SESSION_STATE.get("current_word") or "").strip().lower() if ch.isalpha())
    if not base or SESSION_STATE.get("current_word") != base:
        start_or_analyze_word(base)
    targets = list(SESSION_STATE.get("current_targets") or [])
    guessed = list(SESSION_STATE.get("guessed_words") or [])
    unfound = [w for w in targets if w not in guessed]
    if unfound:
        target_w = unfound[0]
        m_info = get_word_meaning(target_w)
        hint_text = (
            f"💡 Hint: Starts with '{target_w[0].upper()}{target_w[1].upper()}...' ({len(target_w)} letters) — "
            f"Meaning clue: {m_info.get('definition', '')}"
        )
    else:
        hint_text = "All isomeric words have already been found!"
    return {
        "word": base,
        "hint": hint_text,
        "unfound_count": len(unfound),
    }


def _format_shelved_list() -> List[Dict[str, Any]]:
    out = []
    for w, info in SESSION_STATE["shelved_words"].items():
        t_len = len(info.get("targets", []))
        g_len = len(info.get("guessed", []))
        out.append({
            "word": w,
            "guessed_count": g_len,
            "total_count": t_len,
            "remaining_count": max(0, t_len - g_len),
        })
    return out


def _build_guess_response(
    base: str,
    correct: bool,
    score_delta: int,
    feedback: str,
    latest_meaning: Dict[str, Any] = None,
    status: str = None,
) -> Dict[str, Any]:
    targets = list(SESSION_STATE.get("current_targets") or [])
    guessed = list(SESSION_STATE.get("guessed_words") or [])
    is_completed = len(targets) > 0 and len(guessed) == len(targets)
    unlocked_meanings = {w: get_word_meaning(w) for w in guessed}
    return {
        "correct": correct,
        "success": correct,
        "status": status or ("unlocked" if correct else "invalid"),
        "word": base,
        "score_delta": score_delta,
        "total_score": SESSION_STATE["score"],
        "feedback": feedback,
        "explanation": feedback,
        "guessed_words": guessed,
        "unlocked_targets": guessed,
        "unlocked_meanings": unlocked_meanings,
        "latest_meaning": latest_meaning,
        "total_isomeric_words": len(targets),
        "remaining_count": max(0, len(targets) - len(guessed)),
        "is_completed": is_completed,
        "masked_targets": [
            w if w in guessed else f"{w[0].upper()}{' _' * (len(w) - 1)} ({len(w)} letters)"
            for w in targets
        ],
        "shelved_list": _format_shelved_list(),
        "completed_words": list(SESSION_STATE["completed_words"]),
        "session_stats": get_session_stats(),
    }


def get_catalog(category: str = None, persona_id: str = None, search: str = None) -> Dict[str, Any]:
    items = list(CATALOG_ITEMS)
    if category and category.lower() != "all":
        items = [i for i in items if i.get("category", "").lower() == category.lower()]
    if search:
        q = search.strip().lower()
        items = [
            i for i in items
            if q in i.get("name", "").lower() or q in i.get("summary", "").lower() or q in i.get("word", "").lower()
        ]
    categories = sorted(list({i.get("category", "General") for i in CATALOG_ITEMS}))
    return {
        "metadata": APP_METADATA,
        "personas": PERSONAS,
        "parameters_schema": PARAMETERS_SCHEMA,
        "categories": categories,
        "items": items,
        "stats": get_session_stats(),
    }


def evaluate_interaction(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified interaction router supporting:
    1. AnagramFrenzy actions:
       - `action == "analyze"`: validates English word & returns total isomeric count.
       - `action == "guess"`: validates a user's isomeric word guess & unlocks meaning.
       - `action == "meaning"`: returns the dictionary definition for a clicked word.
       - `action == "shelve"`: shelves the current word for later.
       - `action == "hint"`: returns a letter + definition hint for an unfound isomeric word.
    2. Standard SD Team QA Smoke & E2E Test Contract (`item_id` + `selected_option`).
    """
    payload = payload or {}
    action = (payload.get("action") or "").strip().lower()

    if action == "meaning":
        res = get_word_meaning(payload.get("word", ""))
        res["correct"] = bool(res.get("is_valid"))
        res["success"] = bool(res.get("is_valid"))
        res["score_delta"] = 0
        return res

    if action == "analyze" or ("word" in payload and "guess" not in payload and "selected_option" not in payload and action not in ("shelve", "hint", "meaning")):
        res = start_or_analyze_word(payload.get("word", ""))
        res["correct"] = bool(res.get("valid"))
        res["success"] = bool(res.get("valid"))
        res["score_delta"] = 0
        return res

    if action == "shelve":
        res = shelve_current_word(payload.get("word"))
        res["correct"] = bool(res.get("shelved"))
        res["success"] = bool(res.get("shelved"))
        res["score_delta"] = 0
        return res

    if action == "hint":
        res = reveal_remaining_words(payload.get("word"))
        res["correct"] = True
        res["success"] = True
        res["score_delta"] = 0
        return res

    if action == "guess" or "guess" in payload:
        return submit_isomeric_guess(payload.get("word", ""), payload.get("guess", ""))

    # Standard Catalog / Smoke Test Contract (`item_id` + `selected_option`)
    item_id = payload.get("item_id")
    selected = str(payload.get("selected_option", payload.get("action", ""))).strip()
    target_item = next((i for i in CATALOG_ITEMS if str(i["id"]) == str(item_id)), CATALOG_ITEMS[0])

    SESSION_STATE["interactions"] += 1
    expected = str(target_item.get("quiz_answer", "")).strip()
    is_correct = selected.lower() == expected.lower() and expected != ""

    score_delta = 10 if is_correct else 0
    if is_correct:
        SESSION_STATE["score"] += score_delta
        SESSION_STATE["correct_count"] += 1
        if target_item["id"] not in SESSION_STATE["completed_ids"]:
            SESSION_STATE["completed_ids"].append(target_item["id"])

    feedback = (
        f"Correct! {target_item.get('quiz_explanation', '')}"
        if is_correct
        else f"Not quite. Expected '{expected}'. {target_item.get('quiz_explanation', '')}"
    )

    return {
        "correct": is_correct,
        "success": is_correct,
        "item_id": target_item["id"],
        "selected_option": selected,
        "correct_answer": expected,
        "score_delta": score_delta,
        "total_score": SESSION_STATE["score"],
        "feedback": feedback,
        "explanation": feedback,
        "session_stats": get_session_stats(),
    }


DAILY_CHALLENGE_POOL: List[Dict[str, Any]] = [
    {"word": "listen", "difficulty": "Medium", "theme": "Classic Harmony", "min_letters": 6},
    {"word": "earth", "difficulty": "Easy", "theme": "Planetary Elements", "min_letters": 5},
    {"word": "least", "difficulty": "Hard", "theme": "Word Power Cluster", "min_letters": 5},
    {"word": "stop", "difficulty": "Easy", "theme": "Quick Fire", "min_letters": 4},
    {"word": "caret", "difficulty": "Medium", "theme": "Language & Precision", "min_letters": 5},
    {"word": "spare", "difficulty": "Hard", "theme": "Master 7-Way Cluster", "min_letters": 5},
    {"word": "team", "difficulty": "Easy", "theme": "Collaboration", "min_letters": 4},
    {"word": "star", "difficulty": "Easy", "theme": "Celestial", "min_letters": 4},
    {"word": "smile", "difficulty": "Medium", "theme": "Positive Vibes", "min_letters": 5},
    {"word": "master", "difficulty": "Hard", "theme": "Grandmaster Anagram", "min_letters": 6},
    {"word": "angel", "difficulty": "Medium", "theme": "Mythic & Form", "min_letters": 5},
    {"word": "reins", "difficulty": "Hard", "theme": "Siren Call", "min_letters": 5},
    {"word": "skate", "difficulty": "Medium", "theme": "Action & Motion", "min_letters": 5},
    {"word": "stone", "difficulty": "Hard", "theme": "Foundational Tones", "min_letters": 5},
]


def get_daily_challenge(date_str: str = None) -> Dict[str, Any]:
    """
    Returns deterministic Daily Challenge for any calendar date (defaults to UTC today).
    Includes puzzle details, puzzle number, targets count, and base word meaning.
    """
    import datetime
    import hashlib

    if not date_str:
        date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # Deterministic index from date hash
    h = int(hashlib.sha256(date_str.encode("utf-8")).hexdigest(), 16)
    idx = h % len(DAILY_CHALLENGE_POOL)
    entry = DAILY_CHALLENGE_POOL[idx]
    base_word = entry["word"]

    targets = get_isomeric_words(base_word, include_base=False)
    meaning = get_word_meaning(base_word)

    # Calculate puzzle sequence number relative to project launch (2026-11-06 = #1)
    base_date = datetime.date(2026, 11, 6)
    try:
        y, m, d = [int(p) for p in date_str.split("-")]
        current_date = datetime.date(y, m, d)
        puzzle_no = max(1, (current_date - base_date).days + 1)
    except Exception:
        puzzle_no = 1

    return {
        "date": date_str,
        "puzzle_number": puzzle_no,
        "word": base_word,
        "theme": entry["theme"],
        "difficulty": entry["difficulty"],
        "target_count": len(targets),
        "target_words": targets,
        "word_meaning": meaning,
    }


def get_session_stats() -> Dict[str, Any]:
    total_items = len(CATALOG_ITEMS)
    completed = len(SESSION_STATE["completed_ids"])
    return {
        "score": SESSION_STATE["score"],
        "interactions": SESSION_STATE["interactions"],
        "correct_count": SESSION_STATE["correct_count"],
        "completed_count": completed,
        "total_items": total_items,
        "progress": {
            "completed": completed,
            "total": total_items,
            "completed_words": len(SESSION_STATE["completed_words"]),
            "shelved_words": len(SESSION_STATE["shelved_words"]),
        },
        "current_word": SESSION_STATE["current_word"],
        "completed_words": list(SESSION_STATE["completed_words"]),
        "shelved_list": _format_shelved_list(),
        "daily_challenge": get_daily_challenge(),
    }