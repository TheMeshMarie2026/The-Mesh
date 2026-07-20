import json

class NarratorJSONValidationError(Exception):
    """Custom exception for narrator JSON validation errors."""
    pass


def validate_narrator_json(json_obj):
    """
    Validate narrator JSON according to the required schema:
    
    {
      "narrative": "",
      "choices": [
        {
          "text": "",
          "impact": {
            "node_id": "",
            "resource_change": 0,
            "trust_change": 0,
            "edge_weight_change": 0
          }
        }
      ]
    }
    """

    # --- Top-level structure ---
    if not isinstance(json_obj, dict):
        raise NarratorJSONValidationError("Top-level JSON must be an object.")

    # Required top-level keys
    required_top_keys = {"narrative", "choices"}
    missing = required_top_keys - json_obj.keys()
    if missing:
        raise NarratorJSONValidationError(f"Missing required keys: {missing}")

    # --- Narrative field ---
    if not isinstance(json_obj["narrative"], str):
        raise NarratorJSONValidationError("Field 'narrative' must be a string.")

    # --- Choices array ---
    choices = json_obj["choices"]
    if not isinstance(choices, list):
        raise NarratorJSONValidationError("'choices' must be a list.")

    if len(choices) != 3:
        raise NarratorJSONValidationError("There must be exactly 3 choices.")

    # --- Validate each choice ---
    for idx, choice in enumerate(choices):
        if not isinstance(choice, dict):
            raise NarratorJSONValidationError(f"Choice {idx} must be an object.")

        # Required keys in each choice
        if "text" not in choice or "impact" not in choice:
            raise NarratorJSONValidationError(f"Choice {idx} missing 'text' or 'impact'.")

        # Validate text
        if not isinstance(choice["text"], str):
            raise NarratorJSONValidationError(f"Choice {idx} 'text' must be a string.")

        # Validate impact object
        impact = choice["impact"]
        if not isinstance(impact, dict):
            raise NarratorJSONValidationError(f"Choice {idx} 'impact' must be an object.")

        required_impact_keys = {
            "node_id",
            "resource_change",
            "trust_change",
            "edge_weight_change"
        }

        missing_impact = required_impact_keys - impact.keys()
        if missing_impact:
            raise NarratorJSONValidationError(
                f"Choice {idx} impact missing keys: {missing_impact}"
            )

        # Validate node_id
        if not isinstance(impact["node_id"], str):
            raise NarratorJSONValidationError(
                f"Choice {idx} 'node_id' must be a string."
            )

        # Validate numerical fields
        for field in ["resource_change", "trust_change", "edge_weight_change"]:
            if not isinstance(impact[field], (int, float)):
                raise NarratorJSONValidationError(
                    f"Choice {idx} '{field}' must be a number."
                )

    return True  # Passed all checks


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    # Example JSON string (replace with narrator output)
    example_json = """
    {
      "narrative": "Test crisis.",
      "choices": [
        {
          "text": "Option 1",
          "impact": {
            "node_id": "Node_A",
            "resource_change": -1,
            "trust_change": 0.2,
            "edge_weight_change": 0.1
          }
        },
        {
          "text": "Option 2",
          "impact": {
            "node_id": "Node_B",
            "resource_change": -2,
            "trust_change": 0.3,
            "edge_weight_change": 0.05
          }
        },
        {
          "text": "Option 3",
          "impact": {
            "node_id": "Node_C",
            "resource_change": -3,
            "trust_change": 0.4,
            "edge_weight_change": 0.2
          }
        }
      ]
    }
    """

    data = json.loads(example_json)

    try:
        print("Validating JSON...")
        validate_narrator_json(data)
        print("JSON is valid.")
    except NarratorJSONValidationError as e:
        print("Validation failed:", e)
