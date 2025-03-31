import os
from typing import Any, Dict, List, Optional, Union
from langfuse import Langfuse
from langfuse.api.resources.commons.types import (
    CreateGeneration,
    CreateObservation,
    CreateScore,
    CreateSpan,
    CreateTrace,
    UpdateObservation,
)


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
    
    def create_trace(self, **kwargs) -> str:
        """Create a new trace.
        
        Args:
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            str: The ID of the created trace.
        """
        trace = self.client.trace(**kwargs)
        return trace.id
    
    def create_span(self, trace_id: Optional[str] = None, **kwargs) -> str:
        """Create a new span.
        
        Args:
            trace_id: Optional trace ID to associate the span with.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            str: The ID of the created span.
        """
        if trace_id:
            trace = self.client.get_trace(trace_id)
            span = trace.span(**kwargs)
        else:
            span = self.client.span(**kwargs)
        return span.id
    
    def create_generation(self, trace_id: Optional[str] = None, **kwargs) -> str:
        """Create a new generation.
        
        Args:
            trace_id: Optional trace ID to associate the generation with.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            str: The ID of the created generation.
        """
        if trace_id:
            trace = self.client.get_trace(trace_id)
            generation = trace.generation(**kwargs)
        else:
            generation = self.client.generation(**kwargs)
        return generation.id
    
    def create_event(self, trace_id: Optional[str] = None, **kwargs) -> str:
        """Create a new event.
        
        Args:
            trace_id: Optional trace ID to associate the event with.
            **kwargs: Arguments to pass to the Langfuse client.
            
        Returns:
            str: The ID of the created event.
        """
        if trace_id:
            trace = self.client.get_trace(trace_id)
            event = trace.event(**kwargs)
        else:
            event = self.client.event(**kwargs)
        return event.id
    
    def create_score(self, **kwargs) -> None:
        """Create a new score.
        
        Args:
            **kwargs: Arguments to pass to the Langfuse client.
        """
        self.client.score(**kwargs)
    
    def get_prompt(self, name: str) -> Dict[str, Any]:
        """Retrieve a prompt by name.
        
        Args:
            name: The name of the prompt to retrieve.
            
        Returns:
            Dict[str, Any]: The prompt data.
        """
        return self.client.get_prompt(name)
    
    def update_observation(self, observation_id: str, **kwargs) -> None:
        """Update an existing observation.
        
        Args:
            observation_id: The ID of the observation to update.
            **kwargs: Arguments to pass to the Langfuse client.
        """
        self.client.update_observation(observation_id, **kwargs)
    
    def flush(self) -> None:
        """Flush all queued observations to the Langfuse API."""
        self.client.flush()
