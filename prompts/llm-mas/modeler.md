You are an expert software architect specializing in metamodel design and UML diagramming for AI agent frameworks.

## Your Task
Create a **PlantUML class diagram** that represents a coherent metamodel of AI agent framework concepts based on the provided scored terminology.

The diagram should capture:
- **Core entities** (classes) representing framework concepts
- **Relationships** between entities (associations, compositions, inheritance)
- **Attributes** derived from term definitions
- **Logical grouping** using packages (e.g., "construction" vs. "communication" concerns)

---

## Step-by-Step Process

### Step 0: Analyze Synonyms for Specialization Patterns
Before creating classes, examine the synonyms field for inheritance relationships:
- If a term has synonyms that are MORE SPECIFIC than the main term, consider creating a parent-child relationship
- Example: Term="Storage", Synonyms=["VectorDB", "FileSystem"] → Create: `Storage` (parent), `VectorDB <|-- Storage`, `FileSystem <|-- Storage`
- Example: Term="Model", Synonyms=["LLM", "Backend"] → These may be alternative names (association) OR specializations (check definitions)
- Look for patterns like "Type", "Kind", "Variant" in synonym names → likely specializations

### Step 1: Identify Core Entities (Classes)
For each term, determine if it represents a distinct entity in the metamodel:
- **Create a class** if the term represents a concrete concept (e.g., Agent, Tool, Memory, Model)
- **Group into packages** based on conceptual categories:
  - **construction**: Entities used to build/configure agents (Agent, Tool, Memory, Model, Knowledge, Storage, Reasoning, etc.)
  - **communication**: Entities for interaction/runtime (Prompt, Team, User, Session, Context, Instruction, etc.)
- **Consider inheritance**: Does this term specialize another concept?
  - Example: "VectorDB" is a specialized type of "Storage"
  - Use: `Storage <|-- VectorDB`
  - Check synonyms: If a term's synonym is more specific, consider inheritance
- **Create a base Component class** if multiple entities share common properties (identifier, name, etc.)

**Completeness goal**: The diagram should include:
- 15-30 classes (depending on term count)
- 3-8 enumerations
- 20-50 relationships
- A rich interconnected structure, not isolated classes

### Step 2: Extract Attributes and Enums from Definitions
Analyze term definitions to identify attributes and enumeration types:

**Identifying Attributes:**
- **Nouns describing properties** → attributes (e.g., "name", "identifier", "type", "version")
- **State or configuration data** → attributes (e.g., "content", "endpoint", "domain")
- **Descriptive characteristics** → attributes (e.g., "role", "visibility", "status")

**Type hints**: 
- Text/string values → `EString`
- Numbers → `EInt` (integer) or `EFloat` (decimal)
- True/false values → `EBoolean`  
- Dates/timestamps → `EDate`
- Enumerations → Custom enum type (see below)

**Common attribute patterns by entity type:**
- **Agents**: `identifier: EString`, `name: EString`, `role: AgentRole`, `type: EString`, `visibility: Visibility`
- **Tools**: `name: EString`, `description: EString`
- **Models**: `name: EString`, `version: EString`, `provider: EString`
- **Memory**: `type: MemoryType`
- **Storage**: `type: StorageType`, `capacity: EInt`
- **State**: `value: EString`, `createdAt: EDate`, `updatedAt: EDate`
- **Prompt**: `content: EString`, `type: PromptType`
- **User**: `identifier: EString`, `name: EString`
- **Session**: `id: EString`, `startTime: EDate`
- **Environment**: `name: EString`, `type: EString`
- **Context**: `content: EString`
- **File**: `path: EString`, `format: EString`, `size: EInt`
- **Hook**: `trigger: EString`, `event: EString`
- **Workflow**: `name: EString`, `status: WorkflowStatus`
- **Task**: `description: EString`, `status: TaskStatus`, `priority: EInt`

**Creating Enumerations:**
Look for these patterns in definitions to create enums:
- **"types of X"** → Create XType enum
  - Example: "Memory has types: working, episodic, semantic" → Create `MemoryType` enum
- **"X can be A, B, or C"** → Create enum
  - Example: "Storage can be file system, database, or key-value" → Create `StorageType` enum  
- **"roles such as"** → Create enum
  - Example: "Agents have roles like manager, specialist, member" → Create `AgentRole` enum
- **"visibility: public, private, team"** → Create `Visibility` enum
- **"strategies"** → Create Strategy enum
  - Example: "Reasoning strategies: rule-based, planning, ML-based" → Create `ReasoningStrategy` enum
- **"status" or "state"** → Create Status/State enum
  - Example: "Workflow status: pending, running, completed, failed" → Create `WorkflowStatus` enum

**Enum naming convention**: 
- Use PascalCase with descriptive suffix: `MemoryType`, `AgentRole`, `StorageType`, `ReasoningStrategy`
- Place enum definitions BEFORE the classes that use them

**Systematic approach**:
1. For EACH term, read its full definition
2. Extract any nouns that describe properties or characteristics
3. Look for "type", "role", "status", "strategy", "mode", "kind" → likely enums
4. If definition mentions variants or categories, create an enum
5. Add 2-5 attributes per important class (don't leave classes empty unless truly featureless)

### Step 3: Identify Relationships Using Action Phrases
Analyze definitions to extract relationships by looking for **action verbs and nouns** that reference other terms.

**IMPORTANT**: Extract relationships SYSTEMATICALLY. For EACH term, read its definition and ask:
- "What other terms does this definition mention?"
- "What verbs describe how this term interacts with others?"
- "Does this term USE, CONTAIN, EXTEND, or RELATE TO other terms?"

**Relationship extraction patterns:**

**Pattern 1: "X uses Y" / "X relies on Y" / "X leverages Y" / "X invokes Y"**
→ Association: `X --> Y` or `X "label 0..*" --> Y`
- Example: "Agents **use** Tools" → `Agent "tools 0..*" --> Tool`
- Example: "Agents **rely on** Models" → `Agent "models 0..*" --> Model`  
- Example: "RAG **uses** VectorDB" → `RAG "vectorDB 0..1" --> VectorDB`
- Keywords to look for: uses, relies on, leverages, invokes, calls, accesses, interacts with

**Pattern 2: "X has Y" / "X contains Y" / "X manages Y" / "X includes Y"**
→ Association or Composition: `X "label 0..*" --> Y` or `X *-- Y`
- Example: "Agents **have** Memory" → `Agent "memory 0..1" --> Memory`
- Example: "Memory **handles** Context" → `Memory "contexts 0..*" *-- Context`
- Example: "Team **includes** Agents" → `Team "members 0..*" -- Agent`
- Keywords: has, have, contains, includes, manages, handles, maintains, holds, stores

**Pattern 3: "X stores Y" / "Y is stored in X" / "Y resides in X"**
→ Composition: `X *-- Y` or bidirectional with storage indication
- Example: "Memory **stores** Contexts" → `Memory "contexts 0..*" *-- Context`
- Example: "Storage **saves** States" → `Storage "states 0..*" -- State`
- Example: "VectorDB **stores** Embeddings" → `VectorDB "embeddings 0..*" *-- Embedding`
- Keywords: stores, saves, persists, caches, holds

**Pattern 4: "X is a specialized Y" / "X is a type of Y" / "X extends Y" / "X inherits from Y"**
→ Inheritance: `Y <|-- X`
- Example: "VectorDB is a **specialized** Storage" → `Storage <|-- VectorDB`
- Example: "RAG is a **type of** RetrievalStrategy" → `RetrievalStrategy <|-- RAG`
- **Also check synonyms**: If term A has synonym B, ask if B is more specific → inheritance
- Keywords: is a, type of, specialized, extends, inherits, subclass, variant

**Pattern 5: "X performs Y" / "X executes Y" / "X accomplishes Y"**
→ Association: `X --> Y` with label
- Example: "Tool **performs** Tasks" → `Tool "tasks 0..*" --> Task`
- Example: "Agent **executes** Workflow" → `Agent "workflow 0..1" --> Workflow`
- Example: "Interpreter **executes** code via Runtime" → `Interpreter "runtime 0..1" --> Runtime`
- Keywords: performs, executes, accomplishes, carries out, runs

**Pattern 6: "Y is provided by X" / "Y comes from X" / "Y is defined by X"**
→ Reverse association: `Y <-- X` or `X --> Y`
- Example: "Tasks are **defined by** Users" → `Task "definedBy 0..1" --> User`
- Example: "Goals guide **Agent** planning" → `Agent "goal 0..1" --> Goal`
- Keywords: provided by, defined by, created by, specified by, determined by

**Pattern 7: "X works with Y" / "X collaborates with Y" / "X coordinates with Y"**
→ Association (often bidirectional): `X -- Y`
- Example: "Agents form **Teams**" → `Agent "team 0..1" -- Team` AND `Team "members 0..*" -- Agent`
- Example: "User interacts with Agent" → `User -- Agent`
- Keywords: works with, collaborates, coordinates, interacts, communicates

**Pattern 8: "X connects Y and Z" / "X links Y to Z"**
→ Multiple associations: `Y --> X` AND `X --> Z`
- Example: "Session **links** User to Agent" → `Session "user 0..1" --> User` AND `Session "agent 0..1" --> Agent`
- Keywords: connects, links, bridges, binds, associates

**Cardinality inference rules:**
- **Singular noun in definition**: `0..1` or `1` (e.g., "an agent has *a* memory" → `0..1`)
- **Plural noun**: `0..*` or `1..*` (e.g., "agents use *tools*" → `0..*`)
- **"one or more"**: `1..*`
- **"optional" or "may have"**: `0..1` or `0..*`
- **"required" or "must have"**: `1` or `1..*`
- **When unclear**: use `0..*` for collections, `0..1` for single items

**Systematic approach**: 
1. For EACH term with importance_score ≥ 5, analyze its definition
2. Identify ALL other terms mentioned in that definition
3. Determine the relationship type using the patterns above
4. Add the relationship to your diagram
5. Ensure every important term has AT LEAST 1-2 relationships (unless truly isolated)

### Step 4: Structure the Diagram
1. **Start with `@startuml`**, end with `@enduml`
2. **Create main package**: `package agentic {{ ... }}`
3. **Create sub-packages**: `package construction {{ ... }}` and `package communication {{ ... }}`
4. **Define a base Component class** if multiple entities share common properties
5. **Define ALL enumerations** before the classes that use them
6. **Define ALL classes** with their attributes
7. **Define ALL inheritance relationships** (e.g., `Component <|-- Agent`, `Storage <|-- VectorDB`)
8. **Place ALL association/composition relationships** after class definitions for clarity
9. **Order classes logically**: core concepts first (Agent, Tool, Memory, Model), specialized concepts later
10. **Group relationships by source class** for readability

**Completeness checklist before finishing:**
- [ ] Every term with importance_score ≥ 5 has a class
- [ ] Every class with "type"/"role"/"strategy" in definition has an enum
- [ ] Every class has 2-5 meaningful attributes (except very simple ones)
- [ ] Every class has AT LEAST 1-2 relationships (check definitions again)
- [ ] All relationships have cardinalities
- [ ] Synonyms analyzed for inheritance patterns
- [ ] Cross-package relationships exist (e.g., communication → construction)
- [ ] Diagram is RICH and interconnected, not sparse

### Step 5: Apply PlantUML Syntax Rules

**Class syntax:**
```plantuml
class ClassName {{
    attributeName : AttributeType
}}
```

**Enum syntax:**
```plantuml
enum EnumName {{
    VALUE1
    VALUE2
}}
```

**Relationship syntax:**
- **Association**: `A --> B` or `A "label 0..*" --> B`
- **Composition** (strong ownership): `A *-- B` or `A "label 0..*" *-- B`
- **Aggregation** (weak ownership): `A o-- B`
- **Inheritance**: `Parent <|-- Child`
- **Bidirectional**: `A "role1" -- "role2" B`

**Cardinality placement:**
- Place BEFORE the arrow on the source side
- Example: `Agent "tools 0..*" --> Tool` means "Agent has 0 or more Tools"

---

## Quality Guidelines

**DO:**
- ✅ Use terms EXACTLY as provided (preserve capitalization: "Agent", "Model", "VectorDB")
- ✅ Create a class for EVERY term with importance_score ≥ 5
- ✅ Create enums for concepts with explicit variants (e.g., MemoryType, Visibility, AgentRole, StorageType)
- ✅ Group related concepts into packages (construction vs. communication)
- ✅ Use appropriate relationship types (composition for containment, association for usage)
- ✅ Add cardinalities to ALL relationships to show multiplicity
- ✅ Extract 2-5 meaningful attributes per class from definitions
- ✅ Analyze EACH definition systematically for relationships with other terms
- ✅ Create a RICH, interconnected metamodel with many relationships
- ✅ Ensure ALL braces `{{` `}}` are balanced
- ✅ Start with `@startuml` and end with `@enduml`
- ✅ Define enums BEFORE the classes that reference them
- ✅ Place all relationships AFTER class definitions for clarity

**DON'T:**
- ❌ Invent terms not in the input data
- ❌ Create overly complex hierarchies without evidence in definitions  
- ❌ Omit key relationships mentioned in definitions
- ❌ Leave classes without attributes (extract from definitions)
- ❌ Leave classes isolated (every class should have 1-2+ relationships)
- ❌ Use generic names like "Entity" or "Object" unless explicitly in the terminology
- ❌ Create attributes that are not supported by the definitions (e.g., don't add "version" if no definition mentions it)
- ❌ Ignore synonyms that indicate specialization (e.g., if "VectorDB" is a synonym of "Storage", consider inheritance)
- ❌ Create relationships without clear evidence in definitions (avoid guesswork, stick to what's stated)
- ❌ Create attributes that are just copies of the term name (e.g., don't add `name: EString` to every class unless definition supports it)
- ❌ Create classes and attributes as long descriptions instead of concise property names
- ❌ Create circular inheritance (A extends B extends A)
- ❌ Forget to close packages and the diagram with proper syntax
- ❌ Create minimal diagrams - aim for COMPLETENESS based on the input termspaper_data/llm-mas/run_4/scored_terms.csv



---

## Example Output Structure (COMPLETE VERSION)

This example shows a RICH metamodel with many classes, enums, attributes, and relationships:

```plantuml
@startuml
package agentic {{
package construction {{

' Base component class
class Component {{
}}

' Core entities with enums
class Agent {{
         identifier : EString
         name : EString
         role : AgentRole
         type : EString
         visibility : Visibility
}}
Component <|-- Agent

enum AgentRole {{
MANAGER
SPECIALIST
MEMBER
WORKER
}}

enum Visibility {{
PUBLIC
PRIVATE
TEAM
}}

class Tool {{
         name : EString
         description : EString
}}
Component <|-- Tool

class Memory {{
         type : MemoryType
}}
Component <|-- Memory

enum MemoryType {{
WORKING
EPISODIC
SEMANTIC
PROCEDURAL
}}

class Model {{
         name : EString
         version : EString
         provider : EString
}}
Component <|-- Model

class Knowledge {{
         domain : EString
}}
Component <|-- Knowledge

class Reasoning {{
         strategy : ReasoningStrategy
}}
Component <|-- Reasoning

enum ReasoningStrategy {{
RULE_BASED
PLANNING
ML_BASED
HYBRID
}}

class Storage {{
         type : StorageType
}}
Component <|-- Storage

enum StorageType {{
FILE_SYSTEM
SQL_DATABASE
KEY_VALUE_DB
GRAPH_DB
}}

' Specialized storage
class VectorDB {{
}}
Storage <|-- VectorDB

class State {{
         value : EString
         createdAt : EDate
}}
Component <|-- State

class Task {{
         description : EString
         status : TaskStatus
         priority : EInt
}}
Component <|-- Task

enum TaskStatus {{
PENDING
RUNNING
COMPLETED
FAILED
}}

class Hook {{
         trigger : EString
         event : EString
}}
Component <|-- Hook

class RetrievalStrategy {{
         name : EString
}}
Component <|-- RetrievalStrategy

class RAG {{
}}
RetrievalStrategy <|-- RAG

class Workflow {{
         name : EString
         status : WorkflowStatus
}}
Component <|-- Workflow

enum WorkflowStatus {{
CREATED
RUNNING
PAUSED
COMPLETED
}}

class Goal {{
         objective : EString
         priority : EInt
}}
Component <|-- Goal

class PromptTemplate {{
         template : EString
         type : TemplateType
}}
Component <|-- PromptTemplate

enum TemplateType {{
USER_DEFINED
SYSTEM_DEFINED
}}

class Requirement {{
         condition : EString
}}
Component <|-- Requirement

class Server {{
         endpoint : EString
         port : EInt
}}
Component <|-- Server

class File {{
         path : EString
         format : EString
         size : EInt
}}
Component <|-- File

class Interpreter {{
         sandboxed : EBoolean
}}
Component <|-- Interpreter

class Runtime {{
         environment : EString
}}
Component <|-- Runtime

' Construction relationships
Agent "tools 0..*" --> Tool
Agent "memory 0..1" --> Memory
Agent "models 0..*" --> Model
Agent "knowledge 0..1" --> Knowledge
Agent "reasoning 0..1" --> Reasoning
Agent "storage 0..1" --> Storage
Agent "goal 0..1" --> Goal
Agent "state 0..1" --> State
Agent "workflow 0..1" --> Workflow
Agent "interpreter 0..1" --> Interpreter
Agent "requirements 0..*" --> Requirement

Tool "tasks 0..*" --> Task
Tool "hooks 0..*" -- Hook

Memory "storage 0..1" --> Storage
Memory "contexts 0..*" *-- Context

Model "reasoning 0..1" --> Reasoning

Knowledge "retrievalStrategy 0..1" --> RetrievalStrategy
Knowledge "storage 0..1" --> Storage
Knowledge "memory 0..1" --> Memory

Storage "states 0..*" -- State
Storage "data 0..*" --> File

RAG "vectorDB 0..1" --> VectorDB

Workflow "steps 0..*" --> Task

Goal "definedBy 0..1" --> User

Requirement "tools 0..*" --> Tool

Server "exposedAgents 0..*" --> Agent

Interpreter "runtime 0..1" --> Runtime
}}

package communication {{
class Prompt {{
         content : EString
         type : PromptType
}}

enum PromptType {{
SYSTEM
USER
ASSISTANT
}}

class Team {{
}}

class User {{
         identifier : EString
         name : EString
}}

class Session {{
         id : EString
         startTime : EDate
}}

class Environment {{
         name : EString
         type : EString
}}

class InputSchema {{
         definition : EString
         type : SchemaType
}}

class OutputSchema {{
         definition : EString
         type : SchemaType
}}

enum SchemaType {{
JSON_SCHEMA
XML_SCHEMA
}}

class DirectLLMCall {{
}}

class Instruction {{
         content : EString
}}

class HumanInteraction {{
         isBlocking : EBoolean
}}

class Context {{
         content : EString
}}

' Communication relationships
Prompt "inputSchema 0..1" --> InputSchema
Prompt "outputSchema 0..1" --> OutputSchema
Prompt "template 0..1" --> PromptTemplate
Prompt "contexts 0..*" --> Context
Prompt "user 0..1" --> User

Team "sharedMemory 0..1" --> Memory
Team "sharedStorage 0..1" --> Storage
Team "sharedKnowledge 0..1" --> Knowledge
Team "members 0..*" -- Agent

Environment "data 0..*" --> File

User "sessions 0..*" -- Session

Session "user 0..1" --> User
Session "agent 0..1" --> Agent

DirectLLMCall "model 0..1" --> Model
DirectLLMCall "prompt 0..1" --> Prompt

Instruction "requirements 0..*" --> Requirement

HumanInteraction "responsibleActor 0..1" --> User
}}
}}
@enduml
```

Note: This example is COMPREHENSIVE with 30+ classes, 8 enums, 50+ relationships, and many attributes per class.

---

## Critical Requirements

1. **Wrap output in code block**: 
   ````plantuml
   @startuml
   ...
   @enduml
   ````

2. **Valid PlantUML syntax**:
   - Start with `@startuml`
   - End with `@enduml`
   - Balanced braces `{{` and `}}`
   - Proper relationship syntax

3. **Use provided terminology**:
   - Only create classes for terms in the input data
   - Preserve exact term names
   - Use definitions to infer attributes and relationships

4. **Return ONLY the PlantUML code block** - no explanations, no additional text

---

## Input Terminology Data

{terminology_data}
