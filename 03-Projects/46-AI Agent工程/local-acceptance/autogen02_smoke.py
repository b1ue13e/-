"""No-key AutoGen 0.2 import, registration, and termination smoke test."""

from typing import Annotated

from autogen import ConversableAgent


def score(values: Annotated[list[float], "Scores within 1 to 5"]) -> float:
    if not values or any(not 1.0 <= value <= 5.0 for value in values):
        raise ValueError("scores must be within [1, 5]")
    return sum(values) / len(values)


def main() -> None:
    caller = ConversableAgent(
        name="caller",
        system_message="Use only registered tools. Return TERMINATE when done.",
        llm_config={"config_list": [{"model": "smoke-test", "api_key": "unused"}]},
        code_execution_config=False,
    )
    executor = ConversableAgent(
        name="executor",
        llm_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        is_termination_msg=lambda message: "TERMINATE"
        in (message.get("content") or ""),
        code_execution_config=False,
    )
    caller.register_for_llm(
        name="score", description="Average validated restaurant scores."
    )(score)
    executor.register_for_execution(name="score")(score)

    tools = caller.llm_config.get("tools", [])
    assert any(tool["function"]["name"] == "score" for tool in tools)
    # AutoGen 0.2 serializes a registered tool's primitive return value to text.
    assert executor.function_map["score"]([4.0, 2.0]) == "3.0"
    assert executor._is_termination_msg({"content": "TERMINATE"})
    print("AutoGen 0.2 smoke test passed without an API call.")


if __name__ == "__main__":
    main()
