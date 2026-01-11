# Anki-COT 
A hand-written tool to capture *your* chain-of-thoughts in response to complex Anki prompts. 


## Motivation
Anki decks can contain complex and broad questions. I prefer them over cloze deletions as they are easy to add, and are more realistic to questions which I encounter frequently. 

Reasoning models have demonstrated the effectiveness of chain-of-thoughts to solve complex problems. It would be interesting to record the raw thoughts in a private ledger that pop up in the mind while going through a problem. Perhaps for down-stream exploration of mental maps or just capture the sheer velocity of thoughts. 

This will allow to compare the accuracy of the final answer, and also capture if you just recalled the answer or arrived at it step-by-step. It may useful to have a one-side conversation and arrive at the final answer, without external influence or hints.  

Hopefully, it would be more fun to power through your decks. 

## Technical specification
It will read the TSV exported Anki deck. This will be populated to a local database.
The backend will be in FastAPI. 
The tool will be a CLI and eventually also offer a simple web interface.

For each card, you start a session recording the thoughts`<think></think>` and then give the final answer in `<answer></answer>`. 

The session(s) will be linked to the card id, and individual thoughts will be timestamped. 

The tool would also allow to run async evaluation of answers by LLM judges, supporting configuration for observability.  



## Example 
```html
<question> tell me step by step how to publish a git repo on github via cli</question>
<think>
1. git init
2. gh auth
3.  gh repo create my-cot --private
4. 
<answer>
```