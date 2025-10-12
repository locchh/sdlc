# Agentic System

## Characteristic

- Tool use

- Planning

- Reflection

- Collaboration

## Patterns

### 1. Input -> [ LLM ] -> Output

A single LLM 

### 2. Input -> [ LLM + Thinking/Reasoning ] -> Output

A LLM with planning, reasoning, 

### 3. Input -> [ LLM + Tool Use ] -> Output

A LLM with tool use capability 

### 4. Input -> [ LLM + Planning/Observe/Reflect + Tool Use ] -> Output

An Agent with planning, observation, reflection, and tool use capability

### 5. Input -> [ Agent ... Agent ] -> Output

A system with multiple agents collaborating to generate output. They can connect to each other in sequential, parallel, looping,  hierarchical, network, etc.


## Evaluation

- LLM as a judge: Simple, scalable, but expensive.

- Runtime as a judge: Scalable, Cheap, but complex to implement.

- Testing as a judge: Scalable, Cheap, but need effort to build test cases.

- Human as a judge: High quality, but expensive and time-consuming.