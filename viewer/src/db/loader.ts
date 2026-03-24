/**
 * Database Loader
 *
 * Fetches timeline.json and loads into local IndexedDB.
 */

import { db } from './index';
import { getConfig } from '../config/timeline';

export interface SyncResult {
    count: number;
    source: 'local' | 'network';
    schemaWarning?: string;
}

/**
 * Sync events from configured data source to local IndexedDB
 */
export const syncEvents = async (force = false): Promise<SyncResult> => {
    const count = await db.events.count();
    if (count > 0 && !force) {
        return { count, source: 'local' };
    }

    const config = getConfig();
    console.log(`Fetching events from: ${config.dataUrl}`);

    const response = await fetch(config.dataUrl);
    if (!response.ok) {
        throw new Error(`Failed to fetch timeline data: ${response.status}`);
    }

    const events = await response.json();
    if (!Array.isArray(events) || events.length === 0) {
        throw new Error('No events found in timeline data');
    }

    console.log(`Loading ${events.length} events into IndexedDB...`);
    await db.events.bulkPut(events);

    return {
        count: events.length,
        source: 'network',
    };
};
