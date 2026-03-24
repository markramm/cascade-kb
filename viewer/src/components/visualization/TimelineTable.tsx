import { useState, useMemo } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../../db';
import { ChevronLeft, ChevronRight, Search, ExternalLink } from 'lucide-react';
import type { TimelineEvent } from '../../schemas/events';
import './TimelineTable.css';

const EMPTY_ARRAY: TimelineEvent[] = [];

const GITHUB_BASE = 'https://github.com/markramm/cascade-kb/blob/main/cascade-timeline/events';
const SITE_BASE = '/site/cascade-timeline';

export function TimelineTable() {
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState('');
    const [sortField, setSortField] = useState<keyof TimelineEvent>('date');
    const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');
    const ITEMS_PER_PAGE = 20;

    // Reactive query from Dexie
    const allEvents = useLiveQuery(() => db.events.toArray()) || EMPTY_ARRAY;

    // Filter & Sort
    const filteredEvents = useMemo(() => {
        let result = [...allEvents];

        if (search) {
            const lower = search.toLowerCase();
            result = result.filter(e =>
                e.title.toLowerCase().includes(lower) ||
                e.summary.toLowerCase().includes(lower) ||
                (e.tags || []).some(t => t.toLowerCase().includes(lower))
            );
        }

        result.sort((a, b) => {
            const valA = a[sortField] || '';
            const valB = b[sortField] || '';

            if (sortDir === 'asc') return valA > valB ? 1 : -1;
            return valA < valB ? 1 : -1;
        });

        return result;
    }, [allEvents, search, sortField, sortDir]);

    // Pagination
    const totalPages = Math.ceil(filteredEvents.length / ITEMS_PER_PAGE);
    const paginatedEvents = useMemo(() => {
        const start = (page - 1) * ITEMS_PER_PAGE;
        return filteredEvents.slice(start, start + ITEMS_PER_PAGE);
    }, [filteredEvents, page, ITEMS_PER_PAGE]);

    const handleSort = (field: keyof TimelineEvent) => {
        if (sortField === field) {
            setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortDir('asc');
        }
    };

    return (
        <div className="timeline-table-container">
            <div className="table-header-controls">
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <h2>Timeline Explorer</h2>
                </div>
                <div className="search-box">
                    <Search size={18} />
                    <input
                        type="text"
                        placeholder="Search events..."
                        value={search}
                        onChange={e => { setSearch(e.target.value); setPage(1); }}
                    />
                </div>
            </div>

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th onClick={() => handleSort('date')} className="sortable">Date {sortField === 'date' && (sortDir === 'asc' ? '↑' : '↓')}</th>
                            <th onClick={() => handleSort('title')} className="sortable">Title {sortField === 'title' && (sortDir === 'asc' ? '↑' : '↓')}</th>
                            <th>Tags</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {paginatedEvents.map(event => (
                            <tr key={event.id}>
                                <td className="col-date">{event.date}</td>
                                <td className="col-title">
                                    <a href={`${SITE_BASE}/${encodeURIComponent(event.id)}`} className="event-title">{event.title}</a>
                                    <div className="event-summary">{(event.summary || '').substring(0, 100)}</div>
                                </td>
                                <td>
                                    <div className="tags-list">
                                        {(event.tags || []).slice(0, 3).map(tag => (
                                            <span key={tag} className="badge badge-tag">{tag}</span>
                                        ))}
                                        {(event.tags || []).length > 3 && <span className="badge badge-more">+{(event.tags || []).length - 3}</span>}
                                    </div>
                                </td>
                                <td className="col-actions">
                                    <a href={`${SITE_BASE}/${encodeURIComponent(event.id)}`} className="icon-btn" title="View entry">
                                        <ExternalLink size={16} />
                                    </a>
                                </td>
                            </tr>
                        ))}
                        {paginatedEvents.length === 0 && (
                            <tr>
                                <td colSpan={4} style={{ textAlign: 'center', padding: '2rem' }}>
                                    No events found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <div className="pagination-controls">
                <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>
                    <ChevronLeft size={16} /> Previous
                </button>
                <span>Page {page} of {totalPages || 1}</span>
                <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>
                    Next <ChevronRight size={16} />
                </button>
            </div>
        </div>
    );
}
