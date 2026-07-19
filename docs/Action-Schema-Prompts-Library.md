# Mesh Action Schemas

This file defines all approved action schemas used by the Mesh Narrator and validated by the Mesh Engine.

Each action contains:
- action_type  
- description  
- required fields  
- impact object

Impact object:
```json
{
  "node_id": "",
  "resource_change": 0,
  "trust_change": 0,
  "edge_weight_change": 0
}
