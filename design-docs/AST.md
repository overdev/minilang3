# Abstract Syntax Tree

Enhancements and corrections beased on minilang2 AST

## Problems

- Definition nodes are good adds unnecessary complexity during translation
- Type nodes still aren't good enough
- Parameter and Variable offsets got completely forgotten with definition nodes

## Enhancements

- Member lookup node chains is now well-structured and easy to undestand and translate


## Solutions

- ExprOperands used during translation will be moved to parsing
- No more definition nodes
- Class Declaration nodes must distinguish static from instance members
