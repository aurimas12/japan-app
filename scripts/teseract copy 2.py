import cv2
import pytesseract

# Nurodykite teisingą Tesseract kelią
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

# Sukurkite Japonų simbolių žodyną su reikšmėmis
katakana_dict = {
    "ア": "a",  "イ": "i",  "ウ": "u",  "エ": "e",  "オ": "o",
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    "サ": "sa", "シ": "shi", "ス": "su", "セ": "se", "ソ": "so",
    "タ": "ta", "チ": "chi", "ツ": "tsu", "テ": "te", "ト": "to",
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
    "ハ": "ha", "ヒ": "hi", "フ": "fu", "ヘ": "he", "ホ": "ho",
    "マ": "ma", "ミ": "mi", "ム": "mu", "メ": "me", "モ": "mo",
    "ヤ": "ya",        "ユ": "yu",        "ヨ": "yo",
    "ラ": "ra", "リ": "ri", "ル": "ru", "レ": "re", "ロ": "ro",
    "ワ": "wa", "ヲ": "wo",
    "ン": "n",

    # Dakuon (su nigarintais taškais „゛“)
    "ガ": "ga", "ギ": "gi", "グ": "gu", "ゲ": "ge", "ゴ": "go",
    "ザ": "za", "ジ": "ji", "ズ": "zu", "ゼ": "ze", "ゾ": "zo",
    "ダ": "da", "ヂ": "ji", "ヅ": "zu", "デ": "de", "ド": "do",
    "バ": "ba", "ビ": "bi", "ブ": "bu", "ベ": "be", "ボ": "bo",

    # Handakuon (su mažaisiais apskritimais „゜“)
    "パ": "pa", "ピ": "pi", "プ": "pu", "ペ": "pe", "ポ": "po",

    # Mažosios katakana (naudojamos junginiams)
    "ァ": "a", "ィ": "i", "ゥ": "u", "ェ": "e", "ォ": "o",
    "ャ": "ya", "ュ": "yu", "ョ": "yo",
    "ッ": "small tsu (dvigubina priebalsį)",

    # Specialūs simboliai
    "ー": "ilginimas",
    "。": "taškas",
    "、": "kablelis",
    "「": "kairysis kabutės ženklas",
    "」": "dešinysis kabutės ženklas"
}
hiragana_dict = {
    "あ": "a",  "い": "i",  "う": "u",  "え": "e",  "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya",        "ゆ": "yu",        "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "wo",
    "ん": "n",

    # Dakuon (su nigarintais taškais „゛“)
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",

    # Handakuon (su mažaisiais apskritimais „゜“)
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",

    # Mažosios hiragana (naudojamos junginiams)
    "ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o",
    "ゃ": "ya", "ゅ": "yu", "ょ": "yo",
    "っ": "small tsu (dvigubina priebalsį)",

    # Specialūs simboliai
    "ー": "ilginimas",
    "。": "taškas",
    "、": "kablelis",
    "「": "kairysis kabutės ženklas",
    "」": "dešinysis kabutės ženklas"
}


# Įkelti paveikslėlį
image = cv2.imread("C:/Users/aurimas/Downloads/k-a.png")

# Konvertuoti į pilką spalvą
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Binarizuoti paveikslėlį
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Atpažinti simbolį
text = pytesseract.image_to_string(binary, lang='jpn', config='--psm 8').strip()

# Surasti reikšmę žodyne
meaning = katakana_dict.get(text, "Nerasta")

# Atspausdinti rezultatą
print(f"Nuskaitytas simbolis: {text}")
print(f"Reikšmė: {meaning}")

# Išsaugoti apdorotą paveikslėlį (patikrinimui)
cv2.imwrite("processed_image.png", binary)
