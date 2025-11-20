import spacy
from spacy.matcher import Matcher
from nlp_utils import get_matches, extract_after_keyword
import re

# Inicialização do SpaCy e Matcher
nlp = spacy.load("/opt/pt_core_news_sm")
SPACY_AVAILABLE = True
matcher = Matcher(nlp.vocab)

# Palavras-chave 
matcher.add("CONSUMIDOR_KEYWORD", [[{"LOWER": "consumidor"}], [{"LOWER": "cpf"}]])
matcher.add("CONSUMIDOR_NAO_IDENTIFICADO", [
    [{"LOWER": {"IN": ["consumidor","cliente"]}},
     {"LOWER": {"IN": ["não","nao"]}},
     {"LOWER": {"IN": ["identificado","informado"]}}]
])
matcher.add("CNPJ_KEYWORD", [[{"LOWER": "cnpj"}]])
matcher.add("NUMERO_NOTA_KEYWORD", [[{"LOWER": {"IN":["extrato","nota","nf","nfc","nfc-e","nfe","numero","número"]}}]])
matcher.add("SERIE_KEYWORD", [
    [{"LOWER": "série"}],
    [{"LOWER": "serie"}],
    [{"LOWER": "coo"}],
    [{"LOWER": "ccf"}],
    [{"LOWER": "sat"}, {"LOWER": {"IN": ["n°","no","n","nro"]}}] 
])
matcher.add("DATA_FORMATADA", [[{"TEXT": {"REGEX": r"\d{1,2}/\d{1,2}/\d{4}"}}]])

# Padrões de documentos
matcher.add("CPF", [[{"TEXT": {"REGEX": r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}"}}]])
matcher.add("CNPJ", [[{"TEXT": {"REGEX": r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}"}}]])
matcher.add("VALOR_NUMERICO", [[{"TEXT": {"REGEX": r"\d+"}}]])

# Função principal que extrai dados estruturados de OCR usando SpaCy + regex.
def nlp_extract(ocr_text, fields_dict):
    fields = fields_dict.copy()
    if not ocr_text.strip() or not SPACY_AVAILABLE:
        return fields

    doc = nlp(ocr_text)
    matches = get_matches(doc, matcher, nlp)

    # CPF/CNPJ do consumidor 
    if not fields.get("CNPJ_CPF_consumidor"):
        if "CONSUMIDOR_NAO_IDENTIFICADO" in matches:
            fields["CNPJ_CPF_consumidor"] = "CONSUMIDOR NÃO IDENTIFICADO"
        else:
            cpf_cnpj = extract_after_keyword(matches, "CONSUMIDOR_KEYWORD", ["CPF","CNPJ"], max_tokens=4, doc=doc)
            if cpf_cnpj:
                fields["CNPJ_CPF_consumidor"] = cpf_cnpj

    # CNPJ do emissor 
    if not fields.get("CNPJ_emissor"):
        cnpj = extract_after_keyword(matches, "CNPJ_KEYWORD", ["CNPJ"], max_tokens=4, doc=doc)
        if cnpj:
            fields["CNPJ_emissor"] = cnpj

    # Número da nota fiscal
    if not fields.get("numero_nota_fiscal"):
        numero = extract_after_keyword(matches, "NUMERO_NOTA_KEYWORD", ["VALOR_NUMERICO"], max_tokens=4, doc=doc)
        if numero:
            fields["numero_nota_fiscal"] = numero
        else:
            nf_patterns = [
                r'Extrato\s*(?:No|N[ºo°]|Número)?\s*[:\.]?\s*([0-9]+)',
                r'NFC[-]?e?\s*(?:No|N[ºo°]|Número)?\s*[:\.]?\s*([0-9.]+)',
                r'Nota\s*Fiscal\s*[:\.]?\s*([0-9]+)',
                r'Cupom\s*Fiscal\s*[:\.]?\s*([0-9]+)',
                r'N[ºo°]?\s*[:\.]?\s*([0-9]+)',
                r'Número\s*[:\.]?\s*([0-9]+)'
            ]
            for pattern in nf_patterns:
                match = re.search(pattern, ocr_text, re.IGNORECASE)
                if match:
                    fields["numero_nota_fiscal"] = match.group(1)
                    break

    # Série da nota fiscal 
    if not fields.get("serie_nota_fiscal"):
        serie = extract_after_keyword(matches, "SERIE_KEYWORD", ["VALOR_NUMERICO"], max_tokens=3, doc=doc)
        if serie:
            fields["serie_nota_fiscal"] = serie
        else:
            series_patterns = [
                r'S[eé]rie[:\s]*([0-9]+)',
                r'SAT\s*(N[ºo]?|n|nro)\s*[:\s]*([0-9]+)',
                r'COO[:\s]*([0-9]+)',
                r'CCF[:\s]*([0-9]+)'
            ]
            for pattern in series_patterns:
                match = re.search(pattern, ocr_text, re.IGNORECASE)
                if match:
                    for group_index in range(1, len(match.groups()) + 1):
                        if match.group(group_index) and match.group(group_index).isdigit():
                            fields["serie_nota_fiscal"] = match.group(group_index)
                            break
                    if fields.get("serie_nota_fiscal"):
                        break

    # Data de emissão 
    if not fields.get("data_emissao"):
        if "DATA_FORMATADA" in matches:
            fields["data_emissao"] = matches["DATA_FORMATADA"][0].text
        else:
            match = re.search(r"\d{1,2}/\d{1,2}/\d{4}", ocr_text)
            if match:
                fields["data_emissao"] = match.group()

    # Forma de pagamento 
    if not fields.get("forma_pgto"):
        sent_lower = ocr_text.lower()
        if 'pix' in sent_lower:
            fields["forma_pgto"] = "pix"
        elif 'dinheiro' in sent_lower:
            fields["forma_pgto"] = "dinheiro"
        elif any(pgto in sent_lower for pgto in ['cartão crédito','cartao credito','crédito','credito']):
            fields["forma_pgto"] = "cartao de credito"
        elif any(pgto in sent_lower for pgto in ['cartão débito','cartao debito','débito','debito']):
            fields["forma_pgto"] = "cartao de debito"
        elif any(pgto in sent_lower for pgto in ['alimentação','alimentacao','refeição','vale alimentação','ali']):
            fields["forma_pgto"] = "cartao de alimentação"
        else:
            fields["forma_pgto"] = "outros"

    return fields