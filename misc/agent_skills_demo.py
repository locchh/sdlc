import anthropic
import os
import json
from pathlib import Path

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Initialize messages
messages = [
    {
        "role": "user",
        "content": "Create a presentation about renewable energy with 5 slides",
    }
]

print("Starting Agent Skills presentation creation...\n")

# Agentic loop - continue until we get a final response
while True:
    response = client.beta.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={
            "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
        },
        messages=messages,
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )

    # Check if we have tool use that needs to be processed
    has_tool_use = False
    tool_results = []

    for block in response.content:
        if hasattr(block, "type") and block.type == "tool_use":
            has_tool_use = True
            print(f"Claude is using tool: {block.name}")
            # In a real scenario, we would execute the tool here
            # For now, we just note that a tool was used
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": "Tool executed",
                }
            )

    # If no tool use, we're done
    if not has_tool_use:
        print("Claude has finished processing")
        break

    # Add assistant response to messages
    messages.append({"role": "assistant", "content": response.content})

    # Add tool results to messages
    if tool_results:
        messages.append({"role": "user", "content": tool_results})

# Extract file ID from response
file_id = None
print("\n=== Looking for file ID ===")

for block in response.content:
    print(f"Block type: {type(block).__name__}")

    # Look for tool_use blocks with code_execution results
    if hasattr(block, "type") and block.type == "tool_use":
        if hasattr(block, "name") and block.name == "code_execution":
            print(f"Found code_execution tool")
            if hasattr(block, "content") and block.content:
                for result_block in block.content:
                    print(f"  Result: {type(result_block).__name__}")
                    # Check all attributes for file_id
                    if hasattr(result_block, "__dict__"):
                        for key, value in result_block.__dict__.items():
                            if "file" in key.lower():
                                print(f"    Found: {key} = {value}")
                                if key == "file_id" or "file_id" in str(value):
                                    file_id = value if key == "file_id" else str(value)

    # Check text blocks for file references
    if hasattr(block, "text") and block.text:
        text_lower = str(block.text).lower()
        if "file" in text_lower or "saved" in text_lower:
            print(f"Text block: {str(block.text)[:100]}...")

if file_id:
    print(f"\n✓ Found file_id: {file_id}")
    print(f"Downloading file...")

    try:
        file_content = client.beta.files.download(
            file_id=file_id, betas=["files-api-2025-04-14"]
        )

        # Create output directory
        output_dir = Path("/Users/locch/Works/snx/misc/agent_skills_output")
        output_dir.mkdir(exist_ok=True)

        # Save to disk
        output_path = output_dir / "renewable_energy.pptx"
        with open(output_path, "wb") as f:
            f.write(file_content.read())

        print(f"✓ Presentation saved to {output_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")
else:
    print("\n⚠️  No file ID found in response")
    print("\nResponse content:")
    for i, block in enumerate(response.content):
        print(f"  [{i}] {type(block).__name__}")
        if hasattr(block, "text"):
            print(f"      Text: {str(block.text)[:100]}...")
