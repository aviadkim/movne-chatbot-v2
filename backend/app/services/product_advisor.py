from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.models import Client, StructuredProduct, Conversation, Message
from .rag_service import RAGService

class ProductAdvisor:
    def __init__(self, db: Session):
        self.db = db
        self.rag_service = RAGService(db)
    
    def get_suitable_products(self, client: Client) -> List[StructuredProduct]:
        """Find suitable products based on client's risk profile and investment goals"""
        return self.db.query(StructuredProduct).filter(
            StructuredProduct.risk_level == client.risk_profile,
            StructuredProduct.is_active == True
        ).all()
    
    def analyze_client_query(self, client_id: int, query: str) -> Dict[str, Any]:
        """Analyze client query and provide relevant context for response generation"""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        
        # Get relevant product information
        product_context = self.rag_service.get_product_information(query)
        
        # Get compliance requirements
        compliance_context = self.rag_service.get_compliance_context(
            product_type="structured_product",
            risk_level=client.risk_profile
        )
        
        # Get conversation history
        recent_conversation = self.get_recent_conversation_context(client_id)
        
        return {
            "client_profile": {
                "risk_profile": client.risk_profile,
                "investment_goals": client.investment_goals
            },
            "product_context": product_context,
            "compliance_context": compliance_context,
            "conversation_history": recent_conversation
        }
    
    def get_recent_conversation_context(self, client_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve recent conversation context for the client"""
        recent_messages = self.db.query(Message).join(Conversation).\
            filter(Conversation.client_id == client_id).\
            order_by(Message.timestamp.desc()).\
            limit(limit).all()
        
        return [{
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp
        } for msg in recent_messages]
    
    def validate_recommendation(self, product: StructuredProduct, client: Client) -> bool:
        """Validate if a product recommendation complies with regulations and client suitability"""
        if product.risk_level > client.risk_profile:
            return False
        
        # Get regulatory requirements
        compliance_rules = self.rag_service.get_compliance_context(
            product_type="structured_product",
            risk_level=product.risk_level
        )
        
        # Implement compliance validation logic here
        # This is a placeholder for actual regulatory compliance checks
        return True
    
    def generate_product_explanation(self, product: StructuredProduct, client: Client) -> str:
        """Generate a personalized explanation of the product for the client"""
        product_info = self.rag_service.get_product_information(
            product.name,
            language="he" if client.preferred_language == "he" else "en"
        )
        
        # Implement explanation generation logic here
        # This should combine product information with client's context
        explanation = f"Based on your {client.risk_profile} risk profile and investment goals, "
        explanation += f"this {product.name} offers {product.expected_return}% expected return "
        explanation += f"over {product.term_length} months with {product.risk_level} risk level."
        
        return explanation