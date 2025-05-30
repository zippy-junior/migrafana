from typing import Dict, List, Union, Any, Tuple
from copy import deepcopy
import re

from core.models import Patch


class JSONPathProcessor:
    """Main class for processing JSON paths with selector support"""

    @staticmethod
    def apply_patch(
        data: Union[Dict, List],
        patch: Patch
    ) -> Union[Dict, List]:
        """
        Applies RFC 6902 JSON Patch operations with selector support
        """
        result = deepcopy(data)

        for operation in patch.root:
            op = operation.op
            path = operation.path
            value = operation.value

            try:
                normalized_path = JSONPathNormalizer.normalize(path)
                resolved_paths = JSONPathResolver.resolve(result, normalized_path)

                for resolved_path in resolved_paths:
                    JSONPathOperator.apply_operation(
                        result,
                        op,
                        resolved_path,
                        value
                    )
            except ValueError as e:
                raise ValueError(f"Failed to process operation {operation}: {str(e)}")

        return result


class JSONPathNormalizer:
    """Handles path normalization and validation"""

    @staticmethod
    def normalize(path: str) -> str:
        """Ensures path follows JSON Pointer spec"""
        if not path.startswith('/'):
            return f'/{path}'
        return path

    @staticmethod
    def get_components(path: str) -> List[str]:
        """Converts path to components with proper escaping"""
        if not path.startswith('/'):
            raise ValueError("Path must start with '/'")
        return [p.replace('~1', '/').replace('~0', '~') for p in path[1:].split('/')]


class JSONPathResolver:
    """Resolves paths including selector expressions"""

    @staticmethod
    def resolve(
        data: Any,
        path: str
    ) -> List[str]:
        """
        Resolves paths to concrete locations in data
        Handles:
        - Regular paths: "/panels/0/title"
        - Selector paths: "/panels/[?type=='row']/title"
        - Wildcard paths: "/panels/*/title"
        - Mixed paths: "/panels/[?type=='row']/*/options"
        """
        if not path.startswith('/'):
            raise ValueError("Path must start with '/'")

        components = path.split('/')[1:]
        current_paths = ['']

        for comp in components:
            new_paths = []

            if comp == '*':
                # Handle wildcard - match all immediate children
                for base_path in current_paths:
                    base_data = JSONPathTraverser.get(data, base_path) if base_path else data
                    matches = JSONPathResolver._get_all_children_keys(base_data)
                    new_paths.extend(
                        JSONPathResolver._build_new_path(base_path, match)
                        for match in matches
                    )
            elif JSONPathSelector.is_selector(comp):
                # Handle selector expression
                selector = JSONPathSelector.extract(comp)
                for base_path in current_paths:
                    base_data = JSONPathTraverser.get(data, base_path) if base_path else data
                    matches = JSONPathSelector.evaluate(base_data, selector)
                    new_paths.extend(
                        JSONPathResolver._build_new_path(base_path, match)
                        for match in matches
                    )
            else:
                # Regular path component
                for base_path in current_paths:
                    new_paths.append(f"{base_path}/{comp}" if base_path else f"/{comp}")

            current_paths = new_paths

        return [p if p.startswith('/') else f'/{p}' for p in current_paths]

    @staticmethod
    def _get_all_children_keys(data: Any) -> List[Union[int, str]]:
        """
        Gets all valid child keys/indices for wildcard expansion
        Returns list of strings for dict keys or integers for list indices
        """
        if isinstance(data, dict):
            return list(data.keys())
        elif isinstance(data, list):
            return list(range(len(data)))
        return []

    @staticmethod
    def _build_new_path(base_path: str, match: Union[int, str]) -> str:
        """Constructs new path from base and match"""
        return f"{base_path}/{match}" if base_path else f"/{match}"


class JSONPathSelector:
    """Handles selector expressions like [?type=='row']"""

    @staticmethod
    def is_selector(component: str) -> bool:
        """Checks if component is a selector expression or wildcard"""
        return (component.startswith('[?') and component.endswith(']')) or component == '*'

    @staticmethod
    def extract(selector_component: str) -> str:
        """Extracts selector content from component"""
        return selector_component[2:-1]

    @staticmethod
    def evaluate(
        data: Any,
        selector: str
    ) -> List[Union[int, str]]:
        """
        Evaluates selector against data and returns matching indices/keys
        """
        if not isinstance(data, (list, dict)):
            return []

        conditions = JSONPathConditionParser.parse(selector)

        if isinstance(data, list):
            return [
                i for i, item in enumerate(data)
                if JSONPathConditionEvaluator.matches(item, conditions)
            ]
        else:
            return [
                key for key, value in data.items()
                if JSONPathConditionEvaluator.matches(value, conditions)
            ]


class JSONPathConditionParser:
    """Parses selector conditions into executable form"""

    @staticmethod
    def parse(selector: str) -> List[Union[str, Tuple[str, str, str]]]:
        """
        Parses selector into list of conditions and operators
        Returns list of either:
        - condition tuples: (key, operator, value)
        - logical operators: '&&' or '||'
        """
        tokens = re.split(r'\s*(&&|\|\|)\s*', selector)
        parsed = []

        for token in tokens:
            if token in ('&&', '||'):
                parsed.append(token)
            else:
                parsed.append(JSONPathConditionParser._parse_condition(token))

        return parsed

    @staticmethod
    def _parse_condition(condition: str) -> Tuple[str, str, str]:
        """Parses a single condition into (key, op, value)"""
        ops = ['==', '!=', '=~', ' in ']
        for op in ops:
            if op in condition:
                key, value = condition.split(op, 1)
                return (key.strip(), op.strip(), value.strip().strip("'\""))
        raise ValueError(f"Invalid condition format: {condition}")


class JSONPathConditionEvaluator:
    """Evaluates conditions against data items"""

    @staticmethod
    def matches(
        item: Any,
        conditions: List[Union[str, Tuple[str, str, str]]]
    ) -> bool:
        """Evaluates all conditions against an item"""
        if not conditions:
            return True

        result = True
        i = 0

        while i < len(conditions):
            condition = conditions[i]

            if isinstance(condition, str):  # Logical operator
                next_cond = conditions[i+1]
                next_result = JSONPathConditionEvaluator._evaluate_single(item, next_cond)

                if condition == '&&':
                    result = result and next_result
                else:  # '||'
                    result = result or next_result
                i += 2
            else:
                result = JSONPathConditionEvaluator._evaluate_single(item, condition)
                i += 1

        return result

    @staticmethod
    def _evaluate_single(
        item: Any,
        condition: Tuple[str, str, str]
    ) -> bool:
        """Evaluates a single condition against an item"""
        if not isinstance(item, dict):
            return False

        key, op, value = condition

        if key not in item:
            return False

        item_value = str(item[key])

        if op == '==':
            return item_value == value
        elif op == '!=':
            return item_value != value
        elif op == '=~':
            return bool(re.match(value, item_value))
        elif op == 'in':
            return value in item_value
        else:
            raise ValueError(f"Unknown operator: {op}")


class JSONPathTraverser:
    """Handles traversal of data structures"""

    @staticmethod
    def get(
        data: Union[Dict, List],
        path: str
    ) -> Any:
        """Gets value at path in data structure"""
        if not path:
            return data

        components = path.split('/')
        current = data

        for comp in components:
            if comp == '':
                continue

            if isinstance(current, dict):
                if comp not in current:
                    raise ValueError(f"Key not found: {comp}")
                current = current[comp]
            elif isinstance(current, list):
                try:
                    idx = int(comp)
                    if idx >= len(current):
                        raise ValueError(f"Index out of range: {idx}")
                    current = current[idx]
                except ValueError:
                    raise ValueError(f"Invalid array index: {comp}")
            else:
                raise ValueError(f"Cannot traverse into {type(current)} at {comp}")

        return current

    @staticmethod
    def resolve_path(
        data: Union[Dict, List],
        components: List[str]
    ) -> Tuple[Any, str]:
        """Resolves path components to parent and target"""
        current = data
        for comp in components[:-1]:
            if isinstance(current, dict):
                if comp not in current:
                    raise ValueError(f"Key not found: {comp}")
                current = current[comp]
            elif isinstance(current, list):
                current = current[int(comp)]
            else:
                raise ValueError(f"Cannot traverse into {type(current)}")
        return current, components[-1]


class JSONPathOperator:
    """Applies operations at resolved paths"""

    @staticmethod
    def apply_operation(
        data: Union[Dict, List],
        op: str,
        path: str,
        value: Any = None
    ) -> None:
        """Applies the specified operation at the given path"""
        components = JSONPathNormalizer.get_components(path)
        parent, last_component = JSONPathTraverser.resolve_path(data, components)

        if op == 'add':
            JSONPathOperator._add(parent, last_component, value)
        elif op == 'remove':
            JSONPathOperator._remove(parent, last_component)
        elif op == 'replace':
            JSONPathOperator._replace(parent, last_component, value)
        elif op == 'move':
            raise NotImplementedError("Move operation requires from_path")
        elif op == 'copy':
            raise NotImplementedError("Copy operation requires from_path")
        elif op == 'test':
            if not JSONPathOperator._test(parent, last_component, value):
                raise ValueError(f"Test failed at {path}")
        else:
            raise ValueError(f"Unsupported operation: {op}")

    @staticmethod
    def _resolve_path(
        data: Union[Dict, List],
        components: List[str]
    ) -> Tuple[Any, str]:
        """Resolves path components to parent and target"""
        current = data
        for comp in components[:-1]:
            if isinstance(current, dict):
                if comp not in current:
                    raise ValueError(f"Key not found: {comp}")
                current = current[comp]
            elif isinstance(current, list):
                current = current[int(comp)]
            else:
                raise ValueError(f"Cannot traverse into {type(current)}")
        return current, components[-1]

    @staticmethod
    def _add(
        parent: Union[Dict, List],
        key: str,
        value: Any
    ) -> None:
        """Adds value at specified location"""
        if isinstance(parent, dict):
            parent[key] = value
        elif isinstance(parent, list):
            if key == '-':
                parent.append(value)
            else:
                parent.insert(int(key), value)
        else:
            raise ValueError("Cannot add to non-container")

    @staticmethod
    def _remove(
        parent: Union[Dict, List],
        key: str
    ) -> None:
        """Removes value at specified location"""
        if isinstance(parent, dict):
            del parent[key]
        elif isinstance(parent, list):
            del parent[int(key)]
        else:
            raise ValueError("Cannot remove from non-container")

    @staticmethod
    def _replace(
        parent: Union[Dict, List],
        key: str,
        value: Any
    ) -> None:
        """Replaces value at specified location"""
        if isinstance(parent, dict):
            parent[key] = value
        elif isinstance(parent, list):
            parent[int(key)] = value
        else:
            raise ValueError("Cannot replace in non-container")

    @staticmethod
    def _test(
        parent: Union[Dict, List],
        key: str,
        value: Any
    ) -> bool:
        """Tests value at specified location"""
        if isinstance(parent, dict):
            return parent.get(key) == value
        elif isinstance(parent, list):
            return parent[int(key)] == value
        return False


# Public API
def apply_patch(
    data: Union[Dict, List],
    patch: Patch
) -> Union[Dict, List]:
    """Public interface for applying JSON patches"""
    return JSONPathProcessor.apply_patch(data, patch)
