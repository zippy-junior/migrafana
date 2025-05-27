from copy import deepcopy
import pytest  # type: ignore
import sys
sys.path.append("..")

from migrafana.src.core.json_parser.parser import (
    JSONPathProcessor,
    JSONPathNormalizer,
    JSONPathResolver,
    JSONPathSelector,
    JSONPathConditionParser,
    JSONPathConditionEvaluator,
    JSONPathTraverser,
    JSONPathOperator,
    apply_patch
)


class TestJSONPathNormalizer:
    """Tests for path normalization and validation"""

    def test_normalize_path(self):
        assert JSONPathNormalizer.normalize("foo") == "/foo"
        assert JSONPathNormalizer.normalize("/foo") == "/foo"
        assert JSONPathNormalizer.normalize("") == "/"

    def test_get_components(self):
        assert JSONPathNormalizer.get_components("/foo/bar") == ["foo", "bar"]
        assert JSONPathNormalizer.get_components("/foo/~0bar") == ["foo", "~bar"]
        assert JSONPathNormalizer.get_components("/foo/~1bar") == ["foo", "/bar"]

    def test_get_components_invalid(self):
        with pytest.raises(ValueError):
            JSONPathNormalizer.get_components("foo/bar")


class TestJSONPathTraverser:
    """Tests for data structure traversal"""

    @pytest.fixture
    def sample_data(self):
        return {
            "foo": {
                "bar": [1, 2, 3],
                "baz": "value"
            },
            "arr": [{"id": 1}, {"id": 2}]
        }

    def test_get_value(self, sample_data):
        assert JSONPathTraverser.get(sample_data, "/foo/bar/0") == 1
        assert JSONPathTraverser.get(sample_data, "/foo/baz") == "value"
        assert JSONPathTraverser.get(sample_data, "/arr/1/id") == 2

    def test_get_invalid_path(self, sample_data):
        with pytest.raises(ValueError):
            JSONPathTraverser.get(sample_data, "/foo/nonexistent")

        with pytest.raises(ValueError):
            JSONPathTraverser.get(sample_data, "/foo/bar/10")

    def test_resolve_path(self, sample_data):
        parent, key = JSONPathTraverser.resolve_path(sample_data, ["foo", "bar", "0"])
        assert parent == [1, 2, 3]
        assert key == "0"


class TestJSONPathSelector:
    """Tests for selector expressions"""

    def test_is_selector(self):
        assert JSONPathSelector.is_selector("[?type=='row']") is True
        assert JSONPathSelector.is_selector("*") is True
        assert JSONPathSelector.is_selector("regular") is False

    def test_extract_selector(self):
        assert JSONPathSelector.extract("[?type=='row']") == "type=='row'"

    def test_evaluate_selector(self):
        data = [
            {"type": "row", "title": "Row 1"},
            {"type": "panel", "title": "Panel 1"},
            {"type": "row", "title": "Row 2"}
        ]

        matches = JSONPathSelector.evaluate(data, "type=='row'")
        assert matches == [0, 2]

        # Test with dict
        data = {
            "a": {"type": "row"},
            "b": {"type": "panel"},
            "c": {"type": "row"}
        }
        matches = JSONPathSelector.evaluate(data, "type=='row'")
        assert set(matches) == {"a", "c"}


class TestJSONPathConditionParser:
    """Tests for condition parsing"""

    def test_parse_condition(self):
        conditions = JSONPathConditionParser.parse("type=='row' && title=~'Row.*'")
        assert conditions == [("type", "==", "row"), "&&", ("title", "=~", "Row.*")]

    def test_parse_complex_condition(self):
        conditions = JSONPathConditionParser.parse("a==1 && b!=2 || c in 3")
        assert conditions == [
            ("a", "==", "1"), "&&", ("b", "!=", "2"), "||", ("c", "in", "3")
        ]

    def test_invalid_condition(self):
        with pytest.raises(ValueError):
            JSONPathConditionParser.parse("invalid condition")


class TestJSONPathConditionEvaluator:
    """Tests for condition evaluation"""

    def test_evaluate_single(self):
        item = {"type": "row", "title": "Row 1"}

        assert JSONPathConditionEvaluator._evaluate_single(item, ("type", "==", "row")) is True
        assert JSONPathConditionEvaluator._evaluate_single(item, ("type", "!=", "panel")) is True
        assert JSONPathConditionEvaluator._evaluate_single(item, ("title", "=~", "Row.*")) is True
        assert JSONPathConditionEvaluator._evaluate_single(item, ("title", "in", "1")) is True

    def test_matches_combined_conditions(self):
        item = {"type": "row", "title": "Row 1", "id": 5}
        conditions = [
            ("type", "==", "row"), "&&",
            ("title", "=~", "Row.*"), "||",
            ("id", "==", "10")
        ]
        assert JSONPathConditionEvaluator.matches(item, conditions) is True

        conditions = [
            ("type", "==", "row"), "&&",
            ("title", "=~", "Panel.*")
        ]
        assert JSONPathConditionEvaluator.matches(item, conditions) is False


class TestJSONPathResolver:
    """Tests for path resolution"""

    @pytest.fixture
    def sample_data(self):
        return {
            "panels": [
                {"type": "row", "title": "Row 1"},
                {"type": "graph", "title": "Graph 1"},
                {"type": "row", "title": "Row 2"}
            ],
            "nested": {
                "items": [
                    {"id": 1, "value": "A"},
                    {"id": 2, "value": "B"}
                ]
            }
        }

    def test_resolve_simple_path(self, sample_data):
        paths = JSONPathResolver.resolve(sample_data, "/panels/0/title")
        assert paths == ["/panels/0/title"]

    def test_resolve_wildcard(self, sample_data):
        paths = JSONPathResolver.resolve(sample_data, "/panels/*/title")
        assert set(paths) == {
            "/panels/0/title",
            "/panels/1/title",
            "/panels/2/title"
        }

    def test_resolve_selector(self, sample_data):
        paths = JSONPathResolver.resolve(sample_data, "/panels/[?type=='row']/title")
        assert set(paths) == {"/panels/0/title", "/panels/2/title"}

    def test_resolve_mixed_path(self, sample_data):
        paths = JSONPathResolver.resolve(sample_data, "/nested/items/[?id==1]/value")
        assert paths == ["/nested/items/0/value"]


class TestJSONPathOperator:
    """Tests for JSON patch operations"""

    @pytest.fixture
    def sample_data(self):
        return {
            "foo": {"bar": [1, 2, 3]},
            "items": [{"id": 1}, {"id": 2}],
            "config": {"enabled": False}
        }

    def test_add_operation(self, sample_data):
        # Add to dict
        JSONPathOperator.apply_operation(sample_data, "add", "/foo/new", "value")
        assert sample_data["foo"]["new"] == "value"

        # Add to array
        JSONPathOperator.apply_operation(sample_data, "add", "/foo/bar/-", 4)
        assert sample_data["foo"]["bar"] == [1, 2, 3, 4]

    def test_remove_operation(self, sample_data):
        JSONPathOperator.apply_operation(sample_data, "remove", "/foo/bar/0")
        assert sample_data["foo"]["bar"] == [2, 3]

    def test_replace_operation(self, sample_data):
        JSONPathOperator.apply_operation(sample_data, "replace", "/config/enabled", True)
        assert sample_data["config"]["enabled"] is True

    def test_test_operation(self, sample_data):
        # Should not raise
        JSONPathOperator.apply_operation(sample_data, "test", "/items/0/id", 1)

        with pytest.raises(ValueError):
            JSONPathOperator.apply_operation(sample_data, "test", "/items/0/id", 2)


class TestJSONPathProcessorIntegration:
    """Integration tests for full JSON patch processing"""

    @pytest.fixture
    def sample_data(self):
        return deepcopy({
            "dashboard": {
                "panels": [
                    {"id": 1, "type": "row", "title": "Row 1"},
                    {"id": 2, "type": "graph", "title": "Graph 1"},
                    {"id": 3, "type": "row", "title": "Row 2"}
                ],
                "settings": {
                    "refresh": "30s",
                    "enabled": False
                }
            }
        })

    def test_apply_patch_simple_operations(self, sample_data):
        patch = [
            {"op": "replace", "path": "/dashboard/settings/refresh", "value": "60s"},
            {"op": "add", "path": "/dashboard/settings/maxItems", "value": 10},
            {"op": "remove", "path": "/dashboard/panels/0"}
        ]

        result = JSONPathProcessor.apply_patch(sample_data, patch)

        assert result["dashboard"]["settings"]["refresh"] == "60s"
        assert result["dashboard"]["settings"]["maxItems"] == 10
        assert len(result["dashboard"]["panels"]) == 2
        assert result["dashboard"]["panels"][0]["id"] == 2

    def test_apply_patch_with_selectors(self, sample_data):
        patch = [
            {
                "op": "replace",
                "path": "/dashboard/panels/[?type=='row']/title",
                "value": "Updated Row"
            },
            {
                "op": "remove",
                "path": "/dashboard/panels/[?type=='graph']"
            }
        ]
        print(sample_data)
        result = JSONPathProcessor.apply_patch(sample_data, patch)

        # Both rows should be updated
        assert result["dashboard"]["panels"][0]["title"] == "Updated Row"
        assert result["dashboard"]["panels"][1]["title"] == "Updated Row"

        # Graph panel should be removed
        assert len(result["dashboard"]["panels"]) == 2
        assert all(p["type"] == "row" for p in result["dashboard"]["panels"])

    def test_apply_patch_with_wildcards(self, sample_data):
        patch = [
            {
                "op": "replace",
                "path": "/dashboard/panels/*/title",
                "value": "Generic Title"
            }
        ]

        result = JSONPathProcessor.apply_patch(sample_data, patch)

        assert all(p["title"] == "Generic Title" for p in result["dashboard"]["panels"])

    def test_invalid_patch_operations(self, sample_data):
        # Invalid path
        with pytest.raises(ValueError):
            JSONPathProcessor.apply_patch(sample_data, [
                {"op": "replace", "path": "invalid/path", "value": "new"}
            ])

        # Test operation failure
        with pytest.raises(ValueError):
            JSONPathProcessor.apply_patch(sample_data, [
                {"op": "test", "path": "/dashboard/settings/enabled", "value": True}
            ])


class TestPublicAPI:
    """Tests for the public apply_patch function"""

    def test_public_api(self):
        data = {"a": 1}
        patch = [{"op": "replace", "path": "/a", "value": 2}]
        result = apply_patch(data, patch)
        assert result["a"] == 2
        assert data["a"] == 1  # Original shouldn't be modified
