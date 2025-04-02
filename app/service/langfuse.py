import os
import ssl
from typing import Any, Dict, List, Optional, Union, Protocol

import httpx
from langfuse import Langfuse
from langfuse.client import StatefulClient, PromptClient


class LangfuseParent(Protocol):
    """Protocol for objects that can be used as parents in LangfuseService methods."""
    
    def span(self, **kwargs) -> StatefulClient: ...
    def generation(self, **kwargs) -> StatefulClient: ...
    def event(self, **kwargs) -> StatefulClient: ...
    def score(self, **kwargs) -> StatefulClient: ...


class LangfuseService:
    """Service class for Langfuse integration.
    
    This class provides a wrapper around the Langfuse client to simplify the creation
    of traces, spans, events, generations, and scores for observability in AI applications.
    
    It supports hierarchical structures through parent objects and implements caching
    for prompts to improve performance.
    
    Usage:
        service = LangfuseService()
        
        # Create a trace
        trace = service.create_trace(name="user-request")
        
        # Create a span under the trace
        span = service.create_span(parent=trace, name="process-input")
        
        # Create a generation under the span
        generation = service.create_generation(parent=span, name="llm-response")
        
        # Score the generation
        service.create_score(
            name="relevance",
            value=0.95,
            observation_id=generation.id
        )
    """

    __prompt_cache = {}
    
    def __init__(self):
        """Initialize the Langfuse service with credentials from environment variables.
        
        The service reads the following environment variables:
        - LANGFUSE_PUBLIC_KEY: Your Langfuse public API key
        - LANGFUSE_SECRET_KEY: Your Langfuse secret API key
        - LANGFUSE_HOST: The Langfuse API host (defaults to https://cloud.langfuse.com)
        """

        if os.getenv("REQUEST_CA_CERTIFICATE"):
            ssl_context = ssl.create_default_context(cafile=os.getenv("REQUEST_CA_CERTIFICATE"))
            http_client = httpx.Client(verify=ssl_context, timeout=20.0)
        else:
            http_client = None

        self.client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            httpx_client=http_client
        )
    
    def create_trace(self, **kwargs) -> StatefulClient:
        """Create a new trace to track a complete user request or operation.
        
        A trace is the top-level object in the Langfuse hierarchy and can contain
        spans, generations, and events.
        
        Args:
            **kwargs: Arguments to pass to the Langfuse client, including:
                - name: Name of the trace
                - id: Optional custom ID
                - user_id: Optional user identifier
                - metadata: Optional dictionary with additional data
                - tags: Optional list of tags
                - session_id: Optional session identifier
                - release: Optional release version
        
        Returns:
            StatefulClient: The created trace object that can be used as a parent
                           for subsequent spans, generations, or events.
        """
        return self.client.trace(**kwargs)
    
    def create_span(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new span to track a specific operation or step in a process.
        
        Spans are used to measure the duration and details of operations within a trace.
        They can be nested to represent hierarchical relationships.
        
        Args:
            parent: Optional parent object (trace or span) to create the span under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client, including:
                - name: Name of the span
                - id: Optional custom ID
                - input: Optional input data
                - output: Optional output data
                - metadata: Optional dictionary with additional data
                - start_time: Optional custom start time
                - end_time: Optional custom end time
                - level: Optional logging level
        
        Returns:
            StatefulClient: The created span object that can be used as a parent
                           for subsequent spans, generations, or events.
        """
        if parent:
            return parent.span(**kwargs)
        return self.client.span(**kwargs)
    
    def create_generation(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new generation to track an AI model's response.
        
        Generations are specialized spans for tracking LLM or other AI model outputs,
        with specific fields for model information, prompts, and completions.
        
        Args:
            parent: Optional parent object (trace or span) to create the generation under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client, including:
                - name: Name of the generation
                - id: Optional custom ID
                - model: Model name or identifier
                - model_parameters: Optional dictionary of model parameters
                - prompt: Optional prompt text or structured prompt
                - completion: The model's response
                - usage: Optional usage statistics (tokens, etc.)
                - metadata: Optional dictionary with additional data
                - start_time: Optional custom start time
                - end_time: Optional custom end time
                - level: Optional logging level
        
        Returns:
            StatefulClient: The created generation object that can be used as a parent
                           for subsequent observations.
        """
        if parent:
            return parent.generation(**kwargs)
        return self.client.generation(**kwargs)
    
    def create_event(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new event to track a point-in-time occurrence.
        
        Events represent instantaneous occurrences within a trace or span,
        such as user interactions or system events.
        
        Args:
            parent: Optional parent object (trace or span) to create the event under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client, including:
                - name: Name of the event
                - id: Optional custom ID
                - input: Optional input data
                - output: Optional output data
                - metadata: Optional dictionary with additional data
                - timestamp: Optional custom timestamp
                - level: Optional logging level
        
        Returns:
            StatefulClient: The created event object.
        """
        if parent:
            return parent.event(**kwargs)
        return self.client.event(**kwargs)
    
    def create_score(self, parent: Optional[LangfuseParent] = None, **kwargs) -> StatefulClient:
        """Create a new score to evaluate the quality of an observation.
        
        Scores are used to track metrics and evaluations of traces, spans, or generations,
        such as accuracy, relevance, or user feedback.
        
        Args:
            parent: Optional parent object to create the score under.
                   Must implement the LangfuseParent protocol.
            **kwargs: Arguments to pass to the Langfuse client, including:
                - name: Name of the score metric
                - value: Numeric value of the score (typically 0-1)
                - observation_id: ID of the observation to score (if not using parent)
                - trace_id: ID of the trace to score (if not using parent)
                - comment: Optional explanation of the score
                - metadata: Optional dictionary with additional data
        
        Returns:
            StatefulClient: The created score object.
        """
        if parent:
            return parent.score(**kwargs)
        return self.client.score(**kwargs)
    
    def get_prompt(self, name: str, label: str = 'production', **kwargs) -> PromptClient:
        """Retrieve a prompt by name with caching support.
        
        This method fetches prompts from Langfuse and caches them by name and label
        to reduce API calls for frequently used prompts.
        
        Args:
            name: The name of the prompt to retrieve.
            label: The version label of the prompt (default: 'production').
            **kwargs: Additional arguments to pass to the Langfuse client.
            
        Returns:
            PromptClient: The prompt object that can be rendered with variables.
        """

        if name in self.__prompt_cache:
            for cached_prompt in self.__prompt_cache[name]:
                if cached_prompt['label'] == label:
                    return cached_prompt['prompt']

        prompt = self.client.get_prompt(name, label=label, **kwargs)

        if name not in self.__prompt_cache:
            self.__prompt_cache[name] = []

        self.__prompt_cache[name].append({'label': label, 'prompt': prompt})

        return prompt
    
    def flush(self) -> Any:
        """Flush all queued observations to the Langfuse API.
        
        This method forces any queued observations to be immediately sent to the
        Langfuse API instead of waiting for the automatic flush.
        
        Returns:
            Any: The result of the flush operation.
        """
        return self.client.flush()
