# Grafana Management Tool

A powerful CLI tool for managing Grafana dashboards and datasources across instances with patch-based transformations.

## Features

### Dashboard Management
- **Retrieve dashboards** by UID from any Grafana instance
- **Update dashboards** with JSON patch operations (RFC 6902)
- **Transfer dashboards** between Grafana instances
- **Apply transformations** using powerful path selectors:
  - Wildcard matching (`*`)
  - Conditional selection (`[?type=='graph']`)
  - Nested path operations

### Datasource Management
- **List all datasources** from an instance
- **Get datasource details** by UID, ID, or name
- **Create/update/delete** datasources
- **Test datasource connections**
- **Manage permissions** for datasources

### Advanced Operations
- **JSON Patch support** for precise modifications
- **Environment variable** support for credentials
- **Multi-instance sync** between Grafana servers
- **Dry-run capability** for testing changes
- **Comprehensive error handling**

## Installation

```bash
pip install grafana-management-tool
```

Or install from source:

```bash
git clone https://github.com/yourrepo/grafana-management-tool.git
cd grafana-management-tool
pip install -e .
```

## Configuration

Configure via environment variables or command-line arguments:

| Environment Variable       | CLI Option       | Description                     |
|----------------------------|------------------|---------------------------------|
| `SRC_GRAFANA_USER`         | `--src-user`     | Source instance username        |
| `SRC_GRAFANA_PASS`         | `--src-pass`     | Source instance password        |
| `DEST_GRAFANA_USER`        | `--dest-user`    | Destination instance username   |
| `DEST_GRAFANA_PASS`        | `--dest-pass`    | Destination instance password   |

## Usage Examples

### 1. Update Dashboard Title

```bash
grafana-tool dashboard \
  --src http://grafana:3000 \
  --uid ABC123 \
  --patch-file title_update.json
```

Where `title_update.json` contains:
```json
[
  {
    "op": "replace",
    "path": "/dashboard/title",
    "value": "New Dashboard Title"
  }
]
```

### 2. Transfer Dashboard Between Instances

```bash
grafana-tool dashboard \
  --src http://grafana1:3000 \
  --dest http://grafana2:3000 \
  --uid ABC123
```

### 3. Bulk Update Panel Titles

```bash
grafana-tool dashboard \
  --src http://grafana:3000 \
  --uid ABC123 \
  --patch-file panel_updates.json
```

Where `panel_updates.json` contains:
```json
[
  {
    "op": "replace",
    "path": "/dashboard/panels/[?type=='graph']/title",
    "value": "Metrics"
  }
]
```

### 4. List All Datasources

```bash
grafana-tool datasources \
  --src http://grafana:3000
```

### 5. Update Datasource URL

```bash
grafana-tool datasource \
  --src http://grafana:3000 \
  --uid prometheus-main \
  --patch-file datasource_update.json
```

Where `datasource_update.json` contains:
```json
[
  {
    "op": "replace",
    "path": "/url",
    "value": "http://new-prometheus:9090"
  }
]
```

## JSON Patch Syntax

The tool supports full RFC 6902 JSON Patch syntax with extensions:

### Supported Operations
- `add` - Add new element
- `remove` - Delete element
- `replace` - Update element
- `copy` - Copy value
- `move` - Move value
- `test` - Verify value

### Path Selectors
- `*` - Wildcard (matches all elements)
- `[?condition]` - Conditional selection
  - Supports `==`, `!=`, `=~` (regex), `in`
  - Multiple conditions with `&&` and `||`

Example selectors:
- `/*/title` - All titles at first level
- `/panels/[?type=='graph']` - All graph panels
- `/panels/[?title=~'CPU.*']` - Panels with titles starting with "CPU"

## Development

### Setup

1. Clone repository
2. Create virtual environment
3. Install dependencies:

```bash
pip install -e .[dev]
```

### Running Tests

```bash
pytest tests/
```

### Building Documentation

```bash
pip install pdoc
pdoc --html -o docs src
```

## License

MIT License

## Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Support

For issues and feature requests, please open an issue on GitHub.