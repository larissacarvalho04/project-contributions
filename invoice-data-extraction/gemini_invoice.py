import os
import json
import google.generativeai as genai
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    gemini_api_key = os.environ['GEMINI_API_KEY']
    genai.configure(api_key=gemini_api_key)

except KeyError:
    error_message = "ERRO: A variável de ambiente 'GEMINI_API_KEY' não foi definida."
    logger.error(error_message)
    raise RuntimeError(error_message)

def extract_invoice_gemini(invoice_text: str) -> dict:

    prompt_for_gemini = f"""
    Por favor, atue como um especialista em analisar notas fiscais brasileiras.
    Sua tarefa é ler o texto abaixo e extrair as informações solicitadas,
    retornando-as em um formato JSON.

    Regras:
    1. Os campos a serem extraídos são: "nome_emissor", "CNPJ_emissor", "endereco_emissor",
       "CNPJ_CPF_consumidor", "data_emissao", "numero_nota_fiscal", "serie_nota_fiscal",
       "valor_total" e "forma_pgto".
    2. Para "forma_pgto", extraia o método de pagamento exato mencionado no texto (Ex: "Dinheiro", "Cartão de Crédito", "Pix").
    3. Se algum campo, incluindo "forma_pgto", não for encontrado, use o valor `null` no JSON.
    4. Formate a data como "DD/MM/AAAA" e o valor total como string com ponto (ex: "150.75").
    5. Sua resposta deve conter APENAS o JSON, sem nenhuma outra palavra ou explicação.

    Texto para análise:
    ---
    {invoice_text}
    ---
    """
    
    try:
        # Prepara o modelo e envia o prompt
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        gemini_response = model.generate_content(prompt_for_gemini)

        # Limpa formatações extras (como ```json) 
        response_text = gemini_response.text
        cleaned_text = response_text.strip().replace("```json", "").replace("```", "")
        
        # Converte o texto JSON em um dicionário Python e o retorna
        extracted_data = json.loads(cleaned_text)
        return extracted_data

    except Exception as error:
        # Captura qualquer erro (de rede, formatação, etc.) 
        error_message = "Falha ao analisar a nota fiscal com o serviço de IA."
        logger.error(f"{error_message} Detalhe: {error}")
        return {"erro": error_message}

