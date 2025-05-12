"""
AutoGen service module for working with Microsoft AutoGen.
"""
import logging
import os
from typing import Any, Dict, List, Optional, Union, Callable
import autogen
from config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class AutoGenService:
    """Service for Microsoft AutoGen operations."""
    
    def __init__(self):
        """Initialize the AutoGen service."""
        self._config = self._load_config()
        self._agents = {}
        logger.info("AutoGen service initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load and return AutoGen configuration."""
        try:
            config = {
                "llm_config": {
                    "config_list": [
                        {
                            "model": "gpt-4",  # Can be configured from settings
                            "api_key": settings.OPENAI_API_KEY,
                        }
                    ],
                    "temperature": 0.2,
                    "cache_seed": 42,  # For reproducibility in development
                }
            }
            return config
        except Exception as e:
            logger.error(f"Failed to load AutoGen configuration: {str(e)}")
            raise
    
    def create_assistant_agent(
        self,
        name: str,
        system_message: str,
        llm_config: Optional[Dict[str, Any]] = None,
        human_input_mode: str = "NEVER"
    ) -> autogen.AssistantAgent:
        """
        Create an AssistantAgent.
        
        Args:
            name: Name of the agent
            system_message: System message for the agent
            llm_config: LLM configuration (uses default if None)
            human_input_mode: When to ask for human input
            
        Returns:
            AssistantAgent instance
        """
        try:
            agent_config = llm_config or self._config["llm_config"]
            
            agent = autogen.AssistantAgent(
                name=name,
                system_message=system_message,
                llm_config=agent_config,
                human_input_mode=human_input_mode
            )
            
            self._agents[name] = agent
            logger.info(f"Created AssistantAgent: {name}")
            return agent
        
        except Exception as e:
            logger.error(f"Error creating AssistantAgent {name}: {str(e)}")
            raise
    
    def create_user_proxy_agent(
        self,
        name: str,
        human_input_mode: str = "NEVER",
        max_consecutive_auto_reply: int = 10,
        code_execution_config: Optional[Dict[str, Any]] = None
    ) -> autogen.UserProxyAgent:
        """
        Create a UserProxyAgent.
        
        Args:
            name: Name of the agent
            human_input_mode: When to ask for human input
            max_consecutive_auto_reply: Maximum number of consecutive auto replies
            code_execution_config: Configuration for code execution
            
        Returns:
            UserProxyAgent instance
        """
        try:
            # Default code execution config
            default_execution_config = {
                "work_dir": "workspace",
                "use_docker": False  # Set to true to use Docker for code execution
            }
            
            execution_config = code_execution_config or default_execution_config
            
            agent = autogen.UserProxyAgent(
                name=name,
                human_input_mode=human_input_mode,
                max_consecutive_auto_reply=max_consecutive_auto_reply,
                code_execution_config=execution_config
            )
            
            self._agents[name] = agent
            logger.info(f"Created UserProxyAgent: {name}")
            return agent
        
        except Exception as e:
            logger.error(f"Error creating UserProxyAgent {name}: {str(e)}")
            raise
    
    def create_group_chat(
        self,
        agents: List[Union[autogen.ConversableAgent]],
        messages: Optional[List[Dict[str, Any]]] = None,
        max_round: int = 10
    ) -> autogen.GroupChat:
        """
        Create a GroupChat for multiple agents.
        
        Args:
            agents: List of agents to include in the chat
            messages: Initial messages
            max_round: Maximum number of conversation rounds
            
        Returns:
            GroupChat instance
        """
        try:
            messages = messages or []
            
            group_chat = autogen.GroupChat(
                agents=agents,
                messages=messages,
                max_round=max_round
            )
            
            logger.info(f"Created GroupChat with {len(agents)} agents")
            return group_chat
        
        except Exception as e:
            logger.error(f"Error creating GroupChat: {str(e)}")
            raise
    
    def create_group_chat_manager(
        self,
        groupchat: autogen.GroupChat,
        llm_config: Optional[Dict[str, Any]] = None,
        system_message: Optional[str] = None
    ) -> autogen.GroupChatManager:
        """
        Create a GroupChatManager to manage a GroupChat.
        
        Args:
            groupchat: The GroupChat to manage
            llm_config: LLM configuration (uses default if None)
            system_message: System message for the manager
            
        Returns:
            GroupChatManager instance
        """
        try:
            agent_config = llm_config or self._config["llm_config"]
            
            default_system_message = (
                "You are a helpful AI assistant. "
                "You manage a group chat between multiple agents, choosing which agent speaks next. "
                "Always select the most appropriate agent based on their expertise and the task at hand."
            )
            
            manager = autogen.GroupChatManager(
                groupchat=groupchat,
                llm_config=agent_config,
                system_message=system_message or default_system_message
            )
            
            logger.info("Created GroupChatManager")
            return manager
        
        except Exception as e:
            logger.error(f"Error creating GroupChatManager: {str(e)}")
            raise
    
    def get_agent(self, name: str) -> Optional[autogen.ConversableAgent]:
        """
        Get an agent by name.
        
        Args:
            name: Name of the agent
            
        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """
        List all available agent names.
        
        Returns:
            List of agent names
        """
        return list(self._agents.keys())
    
    def clear_agents(self) -> None:
        """Clear all agents."""
        self._agents = {}
        logger.info("All agents cleared")

# Create a singleton instance
autogen_service = AutoGenService() 