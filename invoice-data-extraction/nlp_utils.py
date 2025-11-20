import re

# Captura todos os matches do SpaCy Matcher e organiza em dicionário.
def get_matches(doc, matcher, nlp):
    matches_dict = {}
    for match_id, start, end in matcher(doc):
        match_label = nlp.vocab.strings[match_id]
        matches_dict.setdefault(match_label, []).append(doc[start:end])
    return matches_dict

# Busca valores (CPF, CNPJ, VALOR_NUMERICO) após uma keyword usando o matcher.
# Se não encontrar nada, usa fallback via regex na janela após a keyword.
def extract_after_keyword(matches, keyword, target_labels=None, max_tokens=12, doc=None, ocr_text=None):
 
    if keyword not in matches:
        return None

    for keyword_span in matches[keyword]:
        start_idx = keyword_span.end
        end_idx = min(start_idx + max_tokens, len(doc))
        search_span = doc[start_idx:end_idx]

        if target_labels:
            for label in target_labels:
                if label in matches:
                    for span in matches[label]:
                        if span.start >= start_idx and span.end <= end_idx:
                            return span.text

        # fallback via regex na janela após a keyword
        search_text = search_span.text.replace(" ", "") if target_labels and ("CPF" in target_labels or "CNPJ" in target_labels) else search_span.text

        # CPF
        if target_labels and "CPF" in target_labels:
            cpf_match = re.search(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', search_text)
            if cpf_match:
                return cpf_match.group()

        # CNPJ
        if target_labels and "CNPJ" in target_labels:
            cnpj_match = re.search(r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}', search_text)
            if cnpj_match:
                return cnpj_match.group()

    return None