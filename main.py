import fitz  # PyMuPDF
from translate import Translator

def extract_highlighted_words(pdf_path):
    document = fitz.open(pdf_path)
    highlighted_words = []

    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        for annot in page.annots():
            if annot.type[0] == 8:  # 8 corresponds to highlight annotation
                quad_points = annot.vertices
                if len(quad_points) % 4 == 0:
                    for i in range(0, len(quad_points), 4):
                        rect = fitz.Rect(quad_points[i], quad_points[i+3])
                        words_in_rect = page.get_text("words", clip=rect)
                        for word in words_in_rect:
                            text = word[4]  # word[4] contains the actual text
                            if len(text) > 1:  # Ignore single characters
                                highlighted_words.append(text)

    return highlighted_words

def translate_words(words, src_lang='en', dest_lang='pt'):
    translator = Translator(from_lang=src_lang, to_lang=dest_lang)
    translated_words = [translator.translate(word) for word in words]
    return translated_words

if __name__ == "__main__":
    pdf_path = "livre_francois.pdf"  # Certifique-se de que o PDF está na mesma pasta que este script
    words = extract_highlighted_words(pdf_path)

    # Perguntar ao usuário qual é a língua original do texto
    src_lang = input("Qual é a língua original do texto? (ex: en para inglês, fr para francês): ").strip()
    dest_lang = 'pt'  # Definir a língua de destino para português

    # Translate the highlighted words
    translated_words = translate_words(words, src_lang=src_lang, dest_lang=dest_lang)

    # Print the highlighted words with translations
    print("Palavras destacadas e suas traduções:")
    for original, translated in zip(words, translated_words):
        print(f"{original}: {translated}")

