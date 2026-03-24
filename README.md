# Capture Cascade Knowledge Base

A Pyrite-managed knowledge base documenting the systematic erosion of democratic institutions through the Capture Cascade framework.

## Knowledge Bases

- **cascade-timeline** — 4,400+ verified events spanning 1142 to present, with source citations, actor tracking, and institutional impact analysis.

## Structure

```
cascade-timeline/     Pyrite KB (events, actors, sources)
viewer/               React SPA for timeline visualization
export/               Generated static API (rebuilt by pyrite)
config.yaml           Pyrite multi-KB configuration
```

## Usage

```bash
# Index the KB
pyrite index build

# Search events
pyrite search "executive order" -k cascade-timeline

# Export static API for the viewer
pyrite cascade export -k cascade-timeline -o export/
```

## Viewer

The React viewer provides interactive timeline browsing, D3 network visualization, and full-text search.

```bash
cd viewer && npm install && npm run dev
```

## License

- Data: CC BY-SA 4.0
- Code: MIT
