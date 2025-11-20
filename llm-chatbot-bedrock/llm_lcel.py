import logging
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import BedrockLLM
from config import bedrock_client, BEDROCK_LLM_MODEL_ID
from retriever_module import get_retriever


# BEDROCK_LLM_MODEL_ID = 'amazon.titan-text-express-v1'
logger = logging.getLogger(__name__)

history_aware_prompt = ChatPromptTemplate.from_messages([
    ("system", "Dado o histórico da conversa e a última pergunta, reformule a pergunta para ser uma pergunta independente que possa ser entendida sem o histórico. Não responda à pergunta, apenas a reformule."),
    ("user", "{chat_history}\n\nPergunta: {input}"),
])

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente jurídico. Responda à pergunta do usuário baseando-se SOMENTE no contexto de documentos fornecido abaixo. Seja objetivo e, se a resposta não estiver no contexto, diga 'A informação não foi encontrada nos documentos disponíveis.'"),
    ("human", """
Contexto:
{context}

Pergunta: {input}
""")
])

def _get_llm():
    if not bedrock_client:
        raise ConnectionError("O cliente Bedrock não foi inicializado.")
    
    model_kwargs = {
        'max_tokens': 1024,
        'temperature': 0.1,
    }
    
    logger.info(f"Inicializando LLM: {BEDROCK_LLM_MODEL_ID} com parâmetros: {model_kwargs}")
    
    try:
        return BedrockLLM(
            client=bedrock_client, 
            model_id=BEDROCK_LLM_MODEL_ID,
            model_kwargs=model_kwargs
        )
    except Exception as error:
        logger.critical(f"Falha ao inicializar o modelo BedrockLLM: {error}")
        raise

def create_llm_conversational_chain():
    try:
        logger.info("Montando a cadeia conversacional...")
        llm = _get_llm()
        
        retriever = get_retriever()
        if not retriever:
            raise ValueError("O retriever não pôde ser inicializado.")

        history_aware_retriever_chain = create_history_aware_retriever(
            llm=llm,
            retriever=retriever,
            prompt=history_aware_prompt
        )
        
        question_answer_chain = create_stuff_documents_chain(llm, answer_prompt)
        
        conversational_rag_chain = create_retrieval_chain(
            retriever=history_aware_retriever_chain,
            combine_docs_chain=question_answer_chain
        )
        
        logger.info("Cadeia conversacional (simplificada) montada com sucesso.")
        return conversational_rag_chain

    except Exception as error:
        logger.critical(f"Falha crítica ao montar a cadeia conversacional: {error}")
        raise RuntimeError(f"Não foi possível criar a cadeia de IA: {error}")