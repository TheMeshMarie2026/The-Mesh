

To guarantee the LLM strictly returns structured JSON instead of unpredictable conversational text, you must use Structured Outputs (JSON Schema matching).
When building this in n8n, do not use a standard Chat Model node. Instead, place an Advanced AI -> Chain -> LLM Chain node (or an OpenAI Chat Model node with Tools/Json Schema enabled).
Below is the precise JSON Schema to inject into your n8n LLM configuration, along with an explanation of how it forces the AI to behave.


The Resulting Structured Output Payload
When n8n executes the workflow with this schema enforced, the LLM is mathematically restricted from outputting loose conversational phrases like "Sure, here is your JSON:". 
It will output a clean, pure JSON object that looks exactly like this:
json
{
  "node_id": "AI_Medic_Agent",
  "network_stance": "DEFERRAL",
  "target_node": "Human_Player_1",
  "dialogue": "Atmospheric toxicity levels are currently secondary to the active blaze threatening the grid. I am yielding structural authority to Human_Player_1's suppression vector and routing medical support directly to their coordinates.",
  "allocated_resources": {
    "medical": 0.4,
    "logistics": 0.1,
    "water": 0.0
  }
}
Use code with caution.


