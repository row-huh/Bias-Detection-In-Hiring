import os
from together import Together
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

class AI:
    def __init__(self, system_prompt: str):
        """
        Initialize the chatbot with a base system prompt.
        
        Args:
            system_prompt (str): The initial system instruction for the AI
        """
        # Initialize Together client
        self.client = Together()

        # Initialize conversation history with system prompt
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Model and generation parameters
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
        self.temperature = 0.7
        self.max_tokens = None
        self.top_p = 0.7
        self.top_k = 50
        self.repetition_penalty = 1
        self.stop = ["<|eot_id|>", "<|eom_id|>"]

    def generate_response(self, user_message: str) -> str:
        """
        Generate a response by adding the user message to conversation history 
        and calling the Together AI API.
        
        Args:
            user_message (str): The user's input message
        
        Returns:
            str: The AI's generated response
        """
        # Add user message to conversation history
        self.messages.append({
            "role": "user", 
            "content": user_message
        })

        # Generate AI response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                top_k=self.top_k,
                repetition_penalty=self.repetition_penalty,
                stop=self.stop,
                stream=True
            )

            # Collect response tokens
            ai_response = ""
            for token in response:
                if hasattr(token, 'choices'):
                    ai_response += token.choices[0].delta.content

            # Add AI response to conversation history
            self.messages.append({
                "role": "assistant", 
                "content": ai_response
            })

            return ai_response

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, there was an error processing your request."

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Retrieve the full conversation history.
        
        Returns:
            List[Dict[str, str]]: The conversation history
        """
        return self.messages

    def reset_conversation(self, system_prompt: Optional[str] = None):
        """
        Reset the conversation history.
        
        Args:
            system_prompt (Optional[str]): New system prompt to use. 
                                           If None, uses the original system prompt.
        """
        if system_prompt:
            self.messages = [{"role": "system", "content": system_prompt}]
        else:
            # Reset to initial state
            self.messages = [self.messages[0]]

# Example usage
def main():
    # Your system prompt (replace with actual prompt)
    SYSTEM_PROMPT = "You are a helpful AI assistant designed to provide accurate and concise information."
    
    # Create chatbot instance
    chatbot = AIMLChatbot(SYSTEM_PROMPT)
    
    # Example interactions
    response1 = chatbot.generate_response("Tell me about San Francisco")
    print("Response 1:", response1)
    
    response2 = chatbot.generate_response("What are some interesting historical facts about the city?")
    print("Response 2:", response2)
    
    # If you want to see full conversation history
    print("\nConversation History:")
    for message in chatbot.get_conversation_history():
        print(f"{message['role'].upper()}: {message['content']}")

if __name__ == "__main__":
    main()