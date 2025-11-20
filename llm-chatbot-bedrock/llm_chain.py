import boto3
from langchain_aws import BedrockLLM
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMChain:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.llm = BedrockLLM(
            client=self.bedrock_client,
            model_id='amazon.titan-text-express-v1',
            model_kwargs={
                "maxTokenCount": 1000,
                "temperature": 0.1,
            }
        )

        self.prompt = PromptTemplate.from_template("""
        Você é um assistente jurídico especializado. Sua função é responder perguntas com base EXCLUSIVAMENTE no contexto fornecido.

        CONTEXTO DISPONÍVEL:
        {context}

        PERGUNTA DO USUÁRIO:
        {input}

        INSTRUÇÕES:
        1. Baseie sua resposta estritamente nas informações do contexto
        2. Seja preciso e técnico, usando terminologia jurídica adequada
        3. Se a informação necessária não estiver presente no contexto, responda claramente:
        "Não encontrei informações suficientes sobre este tópico nos documentos disponíveis."

        RESPOSTA:""")
        
        self.chain = None
        logger.info("LLMChain configurado com Amazon Titan G1 Express")
    
    def create_chain(self, retriever):
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.chain = create_retrieval_chain(retriever, document_chain)
        logger.info("Chain de RAG criada com sucesso")
        return self.chain
    
    def query(self, question: str) -> str:
        if not self.chain:
            return "Erro: Chain não foi criada. Execute create_chain primeiro."
        if not question or len(question.strip()) < 3:
            return "Por favor, faça uma pergunta mais específica."
        
        try:
            result = self.chain.invoke({"input": question.strip()})
            response = result["answer"]
            logger.info(f"Pergunta: '{question[:50]}...'")
            return response
            
        except Exception as error:
            logger.error(f"Erro: {error}")
            return "Erro ao processar. Tente novamente."