import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class ChatLogger:
    """Logger for storing chat conversations with timestamps."""
    
    def __init__(self, log_dir: str = "conversations"):
        """Initialize the chat logger.
        
        Args:
            log_dir: Directory where conversation logs will be stored
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_conversation = []
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_file = None
    
    def _get_conversation_file(self) -> Path:
        """Get the current conversation file path."""
        return self.log_dir / f"conversation_{self.current_date}.json"
    
    def load_conversations(self, date: str = None) -> List[Dict]:
        """Load conversations for a specific date or current date."""
        if date:
            file_path = self.log_dir / f"conversation_{date}.json"
        else:
            file_path = self._get_conversation_file()
            
        if not file_path.exists():
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def save_conversations(self):
        """Save the current conversation to file."""
        file_path = self._get_conversation_file()
        existing_conversations = self.load_conversations()
        
        # Merge existing conversations with current one
        all_conversations = existing_conversations + self.current_conversation
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_conversations, f, indent=2)
    
    def log_message(self, role: str, message: str):
        """Log a message in the current conversation.
        
        Args:
            role: The role of the message sender (user/assistant)
            message: The content of the message
        """
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "role": role,
            "message": message
        }
        self.current_conversation.append(entry)
        self.save_conversations()
    
    def start_new_conversation(self):
        """Start a new conversation."""
        self.current_conversation = []
        self.current_date = datetime.now().strftime("%Y-%m-%d")
    
    def get_recent_conversations(self, days: int = 7) -> Dict[str, List[Dict]]:
        """Get conversations from the last n days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary with dates as keys and conversations as values
        """
        conversations = {}
        log_files = self.log_dir.glob("conversation_*.json")
        
        for file in sorted(log_files, reverse=True)[:days]:
            date = file.stem.replace("conversation_", "")
            conversations[date] = self.load_conversations(date)
            
        return conversations
    
    def search_conversations(self, query: str) -> List[Dict]:
        """Search through all conversations for specific terms.
        
        Args:
            query: Search term
            
        Returns:
            List of matching conversation entries
        """
        results = []
        log_files = self.log_dir.glob("conversation_*.json")
        
        for file in log_files:
            conversations = self.load_conversations(file.stem.replace("conversation_", ""))
            for entry in conversations:
                if query.lower() in entry["message"].lower():
                    results.append(entry)
                    
        return results

def main():
    """Test the chat logger functionality."""
    logger = ChatLogger()
    
    # Test logging some messages
    logger.log_message("user", "Hello AI!")
    logger.log_message("assistant", "Hello! How can I help you today?")
    logger.log_message("user", "Can you help me with Python?")
    
    # Test loading conversations
    conversations = logger.load_conversations()
    print("\nToday's conversations:")
    for conv in conversations:
        print(f"{conv['timestamp']}: {conv['role']} - {conv['message']}")
    
    # Test searching
    results = logger.search_conversations("python")
    print("\nSearch results for 'python':")
    for result in results:
        print(f"{result['timestamp']}: {result['role']} - {result['message']}")

if __name__ == "__main__":
    main()