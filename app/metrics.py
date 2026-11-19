from prometheus_client import Counter, Histogram

request_seconds = Histogram("cloudops_request_seconds", "HTTP request duration", ["method", "route"])
retrieval_seconds = Histogram("cloudops_retrieval_seconds", "Database retrieval duration")
llm_seconds = Histogram("cloudops_llm_seconds", "LLM response duration")
llm_tokens = Counter("cloudops_llm_tokens", "LLM tokens reported by provider", ["kind"])
llm_estimated_cost = Counter("cloudops_llm_estimated_cost_dollars", "Estimated LLM cost in USD")
