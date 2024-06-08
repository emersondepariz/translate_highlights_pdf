import fitz  # PyMuPDF
from translate import Translator

def extract_all_words(pdf_path):
    document = fitz.open(pdf_path)
    all_words = []

    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        words_in_page = page.get_text("words")
        all_words.extend(word[4] for word in words_in_page)

    return all_words

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
    pdf_path = "english-text-plans.pdf"  # Certifique-se de que o PDF está na mesma pasta que este script

    # Extraia todas as palavras do documento
    all_words = extract_all_words(pdf_path)

    # Extraia palavras realçadas do documento
    highlighted_words = extract_highlighted_words(pdf_path)

    # Perguntar ao usuário qual é a língua original do texto
    src_lang = input("Qual é a língua original do texto? (ex: en para inglês, fr para francês): ").strip()
    dest_lang = 'pt'  # Definir a língua de destino para português

    # Traduzir as palavras destacadas
    translated_words = translate_words(highlighted_words, src_lang=src_lang, dest_lang=dest_lang)

    # Imprimir as palavras destacadas com traduções
    print("Palavras destacadas e suas traduções:")
    for original, translated in zip(highlighted_words, translated_words):
        print(f"{original}: {translated}")

    # Imprimir o total de palavras analisadas e palavras realçadas
    print(f"\nForam analisadas {len(all_words)} palavras ao todo.")
    print(f"Foram encontradas {len(highlighted_words)} palavras realçadas.")
