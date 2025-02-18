# ... [אותו קוד כמו קודם, אבל נשנה את בדיקת המודולים]
    def check_main_imports(self):
        try:
            sys.path.append(str(self.root / 'backend'))
            from app.services.chat_service import AdvancedChatService  # שינוי השם
            from app.services.rag_service import RAGService
            logger.info("✓ Main service imports successful")
        except Exception as e:
            self.issues.append(f"Import error: {str(e)}")
