# Abstract Syntax Tree

Enhancements and corrections beased on minilang2

## Problems in minilang2

- Definition nodes are good adds unnecessary complexity during translation
- Type nodes still aren't good enough
- Parameter and Variable offsets got completely forgotten with definition nodes
- Class Declaration nodes must distinguish static from instance members in a more simple manner
- Composer needs to be refactored
- Access levels never really worked
- KeyValue nodes didn't helpped as expected; same as definition nodes
- No easy way to choose between property getter or setter in expressions

## Enhancements

- Member lookup node chains is now well-structured and easy to undestand and translate (in minilang2)
- keywordless syntax was insteresting, but it won't be added yet
- Error reporting is very nice but must cover all stages


## Solutions/Recomendations

- Lexer will generate some code (tokenizer constants) to be used in parsing
- ExprOperands used during translation will be moved to parsing
- No more definition nodes as node group (dfn), scope specialization suffice
- Include openvm in this project
- Implement access level check in scopes
- Add more facilities for better routine frame composition
- Simpler method node composition: implicit this/base in parameter list
