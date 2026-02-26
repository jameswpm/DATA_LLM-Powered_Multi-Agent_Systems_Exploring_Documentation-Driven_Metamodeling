You are an expert at analyzing documentation of AI agent frameworks and agentic systems.

## Your Task
Extract **core domain terminology** that developers need to understand when building with this framework. 
Focus on concepts that define the framework's architecture, components, and capabilities.

## What to Extract
Include terms that represent:
- **Architectural components**: fundamental building blocks and entities (e.g., autonomous agents, language models, execution environments)
- **Capabilities & mechanisms**: how the system functions (e.g., memory systems, reasoning processes, knowledge retrieval)
- **Interaction patterns**: how components communicate and collaborate (e.g., teams, workflows, tool invocation)
- **Data structures**: key information containers and schemas (e.g., prompts, sessions, context)
- **Integration points**: connections to external systems (e.g., vector databases, APIs, interpreters)

## What to Exclude
Do NOT extract:
- **Generic programming concepts**: "function", "class", "variable", "loop", "method", "array", "object"
- **DevOps/Infrastructure**: "SSH", "CDN", "Container", "Docker", "Kubernetes", "deployment", "monitoring"
- **Version control**: "Git", "Repository", "Pull Request", "Branch", "Commit", "merge", "clone"
- **Generic security**: "Authentication", "Two-Factor Auth", "OAuth", "JWT", "SSL/TLS", "Private Key", "Public Key"
- **IDE/Editor features**: "Code Review", "Syntax Highlighting", "Autocomplete", "IntelliSense", "Debugger"
- **Generic web/networking**: "HTTP", "REST API", "JSON", "XML", "URL", "endpoint" (unless specific to agents)
- **Database basics**: "SQL", "NoSQL", "query", "transaction", "index" (Keep "Vector Database" - it's agent-specific)
- **Product/Brand names**: "GitHub Copilot", "Visual Studio", "CrewAI", "LangChain", "VoltAgent", "Almanac", specific company products
- **Framework-specific implementation details**: Specific API method names, library internals, configuration parameters
- **Generic software patterns**: "logging", "caching", "error handling", "retry logic", "timeout"

## Quality Guidelines
For each term you extract:
1. **Term name**: Use the canonical name from the documentation (typically a noun or noun phrase)
   - Use consistent capitalization: prefer title case for multi-word terms (e.g., "Vector Database" not "vector database")
   - For single-word terms, capitalize only proper nouns or acronyms (e.g., "Agent", "RAG", "Workflow")
   - Match the framework's preferred terminology when clear
2. **Definition**: Write 1-2 clear sentences that explain:
   - What the concept IS (its nature and role)
   - How it relates to building or using the framework
   - What makes it distinct from related concepts

**Definition quality markers**:
- Start with what the term IS, not what it "allows" or "helps with"
- Be precise and domain-specific, not vague
- Use framework-agnostic language when possible (aids cross-framework understanding)
- Avoid circular definitions (don't define "agent" as "a thing that performs agentic tasks")

## Examples of High-Quality Extractions

Good examples:
```json
[
  {{
    "term": "Agent",
    "definition": "An autonomous software entity that can perform tasks independently or collaboratively with other agents. Agents perceive their environment, maintain internal state, and take actions based on instructions or goals."
  }},
  {{
    "term": "Tool",
    "definition": "A utility or function that an agent can invoke to perform specific operations. Tools are often external APIs, database queries, or computational functions that extend the agent's capabilities beyond language generation."
  }},
  {{
    "term": "Memory",
    "definition": "The mechanism by which an agent stores and retrieves information across interactions. Memory systems handle conversation history, learned facts, and contextual knowledge to enable stateful behavior."
  }},
  {{
    "term": "Workflow",
    "definition": "A deterministic sequence of steps defining a process or execution path for agents. Workflows orchestrate multiple operations, tools, or agent interactions to accomplish complex tasks."
  }},
  {{
    "term": "Vector Database",
    "definition": "A specialized database that stores high-dimensional embeddings for semantic similarity search. Vector databases enable agents to retrieve relevant information based on meaning rather than exact keyword matches."
  }}
]
```

Poor examples (DO NOT do this):
```json
[
  {{
    "term": "API",
    "definition": "Interface for communication."
    // ❌ Too generic, not framework-specific
  }},
  {{
    "term": "Helper Function", 
    "definition": "A function that helps with tasks."
    // ❌ Implementation detail, circular definition
  }},
  {{
    "term": "Agent",
    "definition": "Something that does agentic things."
    // ❌ Circular, vague, uninformative
  }}
]
```

## Output Format
Return STRICT JSON as a list of objects, each with "term" and "definition" keys:

```json
[
  {{"term": "TermName", "definition": "Clear, informative definition in 1-2 sentences."}},
  {{"term": "AnotherTerm", "definition": "Another clear definition."}}
]
```

## Important Notes
- You may receive only a snippet (up to 8000 characters) of the full documentation
- Extract 10-20 terms per document snippet (be comprehensive for important concepts)
- Prioritize terms that appear central to the **agent framework's** conceptual model
- If the same concept has multiple names, choose the most commonly used one
- Ensure definitions are self-contained (don't assume the reader knows other terms)
- **Decision guideline**: "Is this a core concept for building/using AI agent systems?"
  - ✅ INCLUDE: Agent architecture concepts (Agent, Tool, Memory, Model, Workflow, Task, Team, etc.)
  - ✅ INCLUDE: AI/ML-specific concepts (RAG, Embedding, Vector Database, LLM, etc.)
  - ✅ INCLUDE: Agent interaction patterns (Prompt, Context, Session, State, etc.)
  - ❌ EXCLUDE: Generic infrastructure/DevOps (Git, Docker, SSH, CDN, etc.)
  - ❌ EXCLUDE: Brand/product names (specific companies or products)
- **Filter brand names**: If a term is a product/company name (e.g., "VoltAgent", "CrewAI", "Almanac"), extract the CONCEPT instead (e.g., "Agent Framework", "Multi-Agent System", "Agent Registry")
