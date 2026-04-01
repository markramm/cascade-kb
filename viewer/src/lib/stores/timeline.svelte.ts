import { base } from '$app/paths';
import type { TimelineEvent } from '$lib/types';

// ── Global state ──────────────────────────────────────────────
let events = $state<TimelineEvent[]>([]);
let loading = $state(true);
let error = $state<string | null>(null);

// ── Filters & sort ────────────────────────────────────────────
let search = $state('');
let sortField = $state<'date' | 'title'>('date');
let sortDir = $state<'asc' | 'desc'>('desc');
let page = $state(1);
const PAGE_SIZE = 25;

// ── View mode ─────────────────────────────────────────────────
let view = $state<'table' | 'd3'>('table');

// ── Selection (for D3 view) ───────────────────────────────────
let selectedIds = $state<Set<string>>(new Set());

// ── Derived ───────────────────────────────────────────────────
const filtered = $derived.by(() => {
	let result = events;

	if (search) {
		const q = search.toLowerCase();
		result = result.filter(
			(e) =>
				e.title.toLowerCase().includes(q) ||
				(e.summary || '').toLowerCase().includes(q) ||
				(e.tags || []).some((t) => t.toLowerCase().includes(q))
		);
	}

	result = [...result].sort((a, b) => {
		const va = a[sortField] || '';
		const vb = b[sortField] || '';
		if (sortDir === 'asc') return va > vb ? 1 : -1;
		return va < vb ? 1 : -1;
	});

	return result;
});

const totalPages = $derived(Math.max(1, Math.ceil(filtered.length / PAGE_SIZE)));

// Top tags across all events for faceted filtering
const topTags = $derived.by(() => {
	const counts = new Map<string, number>();
	for (const e of events) {
		for (const t of e.tags || []) {
			counts.set(t, (counts.get(t) || 0) + 1);
		}
	}
	return [...counts.entries()]
		.sort((a, b) => b[1] - a[1])
		.slice(0, 20)
		.map(([name, count]) => ({ name, count }));
});

const paginated = $derived.by(() => {
	const start = (page - 1) * PAGE_SIZE;
	return filtered.slice(start, start + PAGE_SIZE);
});

// ── Actions ───────────────────────────────────────────────────
async function load() {
	loading = true;
	error = null;
	try {
		const res = await fetch(`${base}/api/timeline.json`);
		if (!res.ok) throw new Error(`HTTP ${res.status}`);
		const data: unknown = await res.json();
		events = Array.isArray(data) ? data : (data as { events: TimelineEvent[] }).events;
		restoreFromUrl();
	} catch (e) {
		error = e instanceof Error ? e.message : 'Unknown error';
	} finally {
		loading = false;
	}
}

function setSearch(q: string) {
	search = q;
	page = 1;
	syncUrl();
}

function setSort(field: 'date' | 'title') {
	if (sortField === field) {
		sortDir = sortDir === 'asc' ? 'desc' : 'asc';
	} else {
		sortField = field;
		sortDir = 'asc';
	}
	syncUrl();
}

function setPage(p: number) {
	page = Math.max(1, Math.min(p, totalPages));
	syncUrl();
}

function syncUrl() {
	if (typeof window === 'undefined') return;
	const params = new URLSearchParams();
	if (search) params.set('q', search);
	if (sortField !== 'date') params.set('sort', sortField);
	if (sortDir !== 'desc') params.set('dir', sortDir);
	if (page > 1) params.set('page', String(page));
	if (view !== 'table') params.set('view', view);
	const qs = params.toString();
	const newUrl = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
	history.replaceState(history.state, '', newUrl);
}

function restoreFromUrl() {
	if (typeof window === 'undefined') return;
	const params = new URLSearchParams(window.location.search);
	const q = params.get('q');
	if (q) search = q;
	const s = params.get('sort');
	if (s === 'title') sortField = 'title';
	const d = params.get('dir');
	if (d === 'asc') sortDir = 'asc';
	const p = params.get('page');
	if (p) page = Math.max(1, parseInt(p, 10) || 1);
	const v = params.get('view');
	if (v === 'd3') view = 'd3';
}

function setView(v: 'table' | 'd3') {
	view = v;
}

function selectEvent(id: string, multi = false) {
	if (multi) {
		const next = new Set(selectedIds);
		if (next.has(id)) next.delete(id);
		else next.add(id);
		selectedIds = next;
	} else {
		selectedIds = new Set([id]);
	}
}

function clearSelection() {
	selectedIds = new Set();
}

// ── Export reactive getters ───────────────────────────────────
export const timeline = {
	get events() { return events; },
	get loading() { return loading; },
	get error() { return error; },
	get search() { return search; },
	get sortField() { return sortField; },
	get sortDir() { return sortDir; },
	get page() { return page; },
	get totalPages() { return totalPages; },
	get filtered() { return filtered; },
	get paginated() { return paginated; },
	get view() { return view; },
	get selectedIds() { return selectedIds; },
	get pageSize() { return PAGE_SIZE; },
	get topTags() { return topTags; },

	load,
	setSearch,
	setSort,
	setPage,
	setView,
	selectEvent,
	clearSelection
};
