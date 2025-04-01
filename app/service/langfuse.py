import os
from typing import Any, Dict, List, Optional, Union, Protocol
from langfuse import Langfuse
from langfuse.api.resources.commons.types import (
    CreateGeneration,
    CreateObservation,
    CreateScore,
    CreateSpan,
    CreateTrace,
    UpdateObservation,
)
from langfuse.client import StatefulClient


class LangfuseParent(Protocol):
    """Protocol for objects that can be used as parents in LangfuseService methods."""
    
    def span(self, **kwargs) -> StatefulClient: ...
    def generation(self, **kwargs) -> StatefulClient: ...
    def event(self, **kwargs) -> StatefulClient: ...


class LangfuseService:
    """Service class for Langfuse integration.
    
    This class delegates to the Langfuse client methods to create traces, spans,
    events, generations, and scores.
    """
    
    def __init__(self):
        """Initialize the Langfuse service with credentials from environment variables."""
        self.client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        )
    
    def create_trace(self, **kwargs) -> StatefulClient:
        """Create a new trace.
        
        Args:
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            StatefulClient: The created trace object.
        """
        return self.client.trace(**kwargs)
    
    def create_span(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new span.
        
        Args:
            parent: Optional parent object to create the span under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            StatefulClient: The created span object.
        """
        if parent:
            return parent.span(**kwargs)
        return self.client.span(**kwargs)
    
    def create_generation(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new generation.
        
        Args:
            parent: Optional parent object to create the generation under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            StatefulClient: The created generation object.
        """
        if parent:
            return parent.generation(**kwargs)
        return self.client.generation(**kwargs)
    
    def create_event(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new event.
        
        Args:
            parent: Optional parent object to create the event under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            StatefulClient: The created event object.
        """
        if parent:
            return parent.event(**kwargs)
        return self.client.event(**kwargs)
    
    def create_score(self, **kwargs) -> Any:
        """Create a new score.
        
        Args:
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            Any: The result of the score creation.
        """
        return self.client.score(**kwargs)
    
    def get_prompt(self, name: str) -> Dict[str, Any]:
        """Retrieve a prompt by name.
        
        Args:
            name: The name of the prompt to retrieve.
            
        Returns:
            Dict[str, Any]: The prompt data.
        """
        return self.client.get_prompt(name)
    
    def update_observation(self, observation_id: str, **kwargs) -> Any:
        """Update an existing observation.
        
        Args:
            observation_id: The ID of the observation to update.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            Any: The result of the observation update.
        """
        return self.client.update_observation(observation_id, **kwargs)
    
    def flush(self) -> Any:
        """Flush all queued observations to the Langfuse API.
        
        Returns:
            Any: The result of the flush operation.
        """
        return self.client.flush()
