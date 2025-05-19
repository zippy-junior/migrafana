JSONPathProcessor
│
├── JSONPathNormalizer (handles path formatting)
│
├── JSONPathResolver (now handles *, [?], and regular paths)
│   ├── _get_all_children_keys (wildcard implementation)
│   └── _build_new_path (path construction)
│
├── JSONPathSelector (handles condition evaluation)
│
├── JSONPathTraverser (data navigation)
│
└── JSONPathOperator (patch operations)