import Dexie, { type Table } from 'dexie';
import type { TimelineEvent } from '../schemas/events';

export class TimelineDatabase extends Dexie {
    events!: Table<TimelineEvent, string>;

    constructor() {
        super('TimelineUTC');
        this.version(3).stores({
            events: 'id, date, *tags',
        });
    }
}

export const db = new TimelineDatabase();
