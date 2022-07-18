# Abstract Syntax Tree

Enhancements and corrections beased on minilang2 AST

## Problems in minilang2

- Definition nodes are good adds unnecessary complexity during translation
- Type nodes still aren't good enough
- Parameter and Variable offsets got completely forgotten with definition nodes
- Class Declaration nodes must distinguish static from instance members in a more simple manner
- Composer needs to be refactored


## Enhancements

- Member lookup node chains is now well-structured and easy to undestand and translate (in minilang2)
- keywordless syntax was insteresting, but it won't be added yet


## Solutions

- Lexer will generate some code (tokenizer constants) to be used in parsing
- ExprOperands used during translation will be moved to parsing
- No more definition nodes, scope and decls suffice
- Include openvm in this project
