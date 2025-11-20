import boto3
from nlp_processor import nlp_extract
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

textract = boto3.client("textract")

def process_textract(file_key: str, bucket_name: str):
    fields = {
        "nome_emissor": None,
        "CNPJ_emissor": None,
        "endereco_emissor": None,
        "CNPJ_CPF_consumidor": None,
        "data_emissao": None,
        "numero_nota_fiscal": None,
        "serie_nota_fiscal": None,
        "valor_total": None,
        "forma_pgto": None
    }

    try:
        logger.info(f"Processando arquivo: {file_key}")
        
        # 1. Detecção de texto bruto
        ocr_response = textract.detect_document_text(
            Document={"S3Object": {"Bucket": bucket_name, "Name": file_key}}
        )
        texto_ocr = extract_text_from_blocks(ocr_response.get('Blocks', []))
        
        # 2. Campos estruturados
        expense_response = textract.analyze_expense(
            Document={"S3Object": {"Bucket": bucket_name, "Name": file_key}}
        )
        fields = extract_expense_fields(expense_response, fields)
        
        # 3. NLP para complementação
        fields = nlp_extract(texto_ocr, fields)
        
        # Log
        preenchidos = sum(1 for value in fields.values() if value)
        logger.info(f"Campos preenchidos: {preenchidos}/{len(fields)}")
        
        return {
            "statusCode": 200,
            "texto": texto_ocr,
            "fields": fields
        }

    except Exception as error:
        logger.error(f"Erro ao processar {file_key}: {str(error)}")
        return {
            "statusCode": 500,
            "texto": "",
            "fields": fields,
            "error": str(error)
        }

def extract_text_from_blocks(blocks):
    lines = [line_block.get('Text', '') for line_block in blocks 
             if line_block.get('BlockType') == 'LINE' and line_block.get('Text')]
    return "\n".join(lines)

def extract_expense_fields(expense_response, fields):
    for expense_doc in expense_response.get('ExpenseDocuments', []):
        for summary_field in expense_doc.get('SummaryFields', []):
            type_text = (summary_field.get('Type') or {}).get('Text', '').upper()
            value_text = (summary_field.get('ValueDetection') or {}).get('Text', '')
            if not value_text:
                continue
            
            field_mappings = {
                'VENDOR_NAME': 'nome_emissor',
                'VENDOR_ADDRESS': 'endereco_emissor',
                'INVOICE_RECEIPT_DATE': 'data_emissao',
                'INVOICE_RECEIPT_ID': 'numero_nota_fiscal',
                'TOTAL': 'valor_total',
                'TAX_ID': 'CNPJ_emissor'
            }
            
            for textract_field, our_field in field_mappings.items():
                if textract_field in type_text and not fields.get(our_field):
                    fields[our_field] = value_text
                    break
    return fields