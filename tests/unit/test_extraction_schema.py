"""Contrato entre o esquema enviado ao Bedrock e o modelo `ExtractedFields`."""

from typing import Any

from liberty_find.extraction.prompt import MAX_DESCRIPTION_CHARS, build_user_message
from liberty_find.extraction.schema import INPUT_SCHEMA, TOOL_CONFIG, TOOL_NAME
from liberty_find.models import ExtractedFields


def _walk(schema: Any) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    if isinstance(schema, dict):
        nodes.append(schema)
        for value in schema.values():
            nodes.extend(_walk(value))
    elif isinstance(schema, list):
        for value in schema:
            nodes.extend(_walk(value))
    return nodes


def test_top_level_uses_only_fields_accepted_by_nova() -> None:
    assert set(INPUT_SCHEMA) == {"type", "properties", "required"}
    assert INPUT_SCHEMA["type"] == "object"


def test_no_type_lists_or_combinators() -> None:
    for node in _walk(INPUT_SCHEMA):
        assert not isinstance(node.get("type"), list)
        assert not {"anyOf", "oneOf", "allOf", "$ref"} & set(node)


def test_schema_matches_pydantic_model() -> None:
    fields = set(ExtractedFields.model_fields)
    assert set(INPUT_SCHEMA["properties"]) == fields
    assert set(INPUT_SCHEMA["required"]) == fields


def test_enums_match_model_enums() -> None:
    model_schema = ExtractedFields.model_json_schema()
    defs = model_schema["$defs"]
    for name, prop in INPUT_SCHEMA["properties"].items():
        if "enum" not in prop:
            continue
        ref = model_schema["properties"][name]
        options = ref.get("anyOf", [ref])
        enum_ref = next(o["$ref"] for o in options if "$ref" in o).split("/")[-1]
        assert prop["enum"] == defs[enum_ref]["enum"], name


def test_tool_choice_forces_the_tool() -> None:
    assert TOOL_CONFIG["toolChoice"] == {"tool": {"name": TOOL_NAME}}


def test_user_message_truncates_description() -> None:
    message = build_user_message("Título", "Empresa", None, "x" * (MAX_DESCRIPTION_CHARS + 500))
    assert message.count("x") == MAX_DESCRIPTION_CHARS
    assert "Location: not stated" in message
