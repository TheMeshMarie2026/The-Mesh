



// Get the input data from the error branch
const inputData = item; 
// Retrieve the agent profile and rankings passed into the workflow originally
// Note: n8n allows you to pull data from earlier nodes using $( 'Node Name' )
const agentId = $('Set Node').item.json.agent_profile.node_id;
const topRankedNode = $('Set Node').item.json.network_rankings[0].node_id;
let fallbackDialogue = "";
if (agentId === topRankedNode) {
  // Fallback text if this agent was supposed to take the lead
  fallbackDialogue = `[NETWORK NOTICE: LLM SYNC DELAYED] Local subroutines active. My node holds the highest priority coefficient for this vector. Commencing automated deployment of local assets now.`;
} else {
  // Fallback text if this agent was supposed to defer
  fallbackDialogue = `[NETWORK NOTICE: LLM SYNC DELAYED] Local subroutines active. I am yielding primary priority to ${topRankedNode}. Routing secondary background data to support their deployment grid.`;
}
// Return the structured object back to your game front-end
return {
  json: {
    dialogue: fallbackDialogue,
    status: "fallback_mode_active",
    error_details: inputData.error?.message || "Timeout"
  }
};
