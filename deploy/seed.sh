#!/bin/bash
# Seed the cascade KB: register, index, export, render site cache
set -e

echo "=== Registering cascade-timeline KB ==="
python3 -c "
from pyrite.config import load_config
from pyrite.utils.yaml import dump_yaml_file
from pathlib import Path

config_path = Path('/data/config.yaml')
if not config_path.exists():
    dump_yaml_file({
        'knowledge_bases': [{
            'name': 'cascade-timeline',
            'path': '/data/cascade-timeline',
            'type': 'journalism-investigation',
            'description': 'The Capture Cascade Timeline — documenting the systematic erosion of democratic institutions. 4,400+ verified events with source citations.'
        }],
        'settings': {
            'index_path': '/data/index.db',
            'host': '0.0.0.0',
            'port': 8088,
        }
    }, config_path)
    print('Config written')
else:
    print('Config exists, skipping')
"

# Copy KB data if not already present
if [ ! -d /data/cascade-timeline/events ]; then
    echo "=== Copying KB data ==="
    cp -r /seed/cascade-timeline /data/cascade-timeline
fi

echo "=== Building index ==="
pyrite index build --no-embed || echo "Index build completed with warnings"

echo "=== Exporting viewer data ==="
mkdir -p /data/viewer-api
pyrite cascade export -k cascade-timeline -o /data/viewer-api

echo "=== Rendering site cache ==="
python3 -c "
from pyrite.config import load_config
from pyrite.storage.database import PyriteDB
from pyrite.services.site_cache import SiteCacheService
config = load_config()
db = PyriteDB(config.settings.index_path)
svc = SiteCacheService(config, db)
stats = svc.render_all()
print(f'Site rendered: {stats}')
db.close()
"

echo "=== Copying viewer dist ==="
if [ -d /app/viewer-dist ]; then
    mkdir -p /data/viewer
    cp -r /app/viewer-dist/* /data/viewer/
    # Copy export data as viewer API
    mkdir -p /data/viewer/api
    cp /data/viewer-api/* /data/viewer/api/
fi

echo "=== Seed complete ==="
