<script lang="ts">
	import { timeline } from '$lib/stores/timeline.svelte';
	import EventPanel from './EventPanel.svelte';
	import type { TimelineEvent } from '$lib/types';

	const SITE_BASE = '/site/cascade-timeline';

	let selectedEvent = $state<TimelineEvent | null>(null);

	function openEvent(event: TimelineEvent, e: MouseEvent) {
		e.preventDefault();
		selectedEvent = event;
	}

	function closePanel() {
		selectedEvent = null;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape' && selectedEvent) {
			closePanel();
			return;
		}
		if (e.key === 'Enter' || e.key === ' ') {
			const target = e.currentTarget as HTMLElement;
			target.click();
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="table-container">
	<div class="table-controls">
		<div class="controls-left">
			<h2>Timeline Explorer</h2>
			<span class="stats-bar">
				{timeline.events.length.toLocaleString()} events &middot;
				{timeline.topActors.length.toLocaleString()} actors &middot;
				{timeline.topTags.length.toLocaleString()} tags
			</span>
			<span class="result-count">{timeline.filtered.length.toLocaleString()} events</span>
		</div>
		<div class="search-box">
			<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<circle cx="11" cy="11" r="8" />
				<path d="m21 21-4.3-4.3" />
			</svg>
			<input
				type="text"
				placeholder="Search events, tags..."
				value={timeline.search}
				oninput={(e) => timeline.setSearch(e.currentTarget.value)}
			/>
			{#if timeline.search}
				<button class="clear-btn" onclick={() => timeline.setSearch('')} aria-label="Clear search">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M18 6 6 18"/><path d="m6 6 12 12"/>
					</svg>
				</button>
			{/if}
		</div>
	</div>

	<div class="date-filter">
		<label class="date-label">
			From
			<input
				type="date"
				class="date-input"
				value={timeline.dateFrom}
				onchange={(e) => timeline.setDateRange(e.currentTarget.value, timeline.dateTo)}
			/>
		</label>
		<label class="date-label">
			To
			<input
				type="date"
				class="date-input"
				value={timeline.dateTo}
				onchange={(e) => timeline.setDateRange(timeline.dateFrom, e.currentTarget.value)}
			/>
		</label>
		{#if timeline.dateFrom || timeline.dateTo}
			<button class="date-clear-btn" onclick={() => timeline.setDateRange('', '')}>Clear</button>
		{/if}
	</div>

	{#if timeline.search || timeline.dateFrom || timeline.dateTo}
		<div class="filter-bar">
			{#if timeline.search}
				<span class="filter-chip">
					Search: {timeline.search}
					<button class="chip-dismiss" onclick={() => timeline.setSearch('')}>&times;</button>
				</span>
			{/if}
			{#if timeline.dateFrom || timeline.dateTo}
				<span class="filter-chip">
					Dates: {timeline.dateFrom || '...'} &ndash; {timeline.dateTo || '...'}
					<button class="chip-dismiss" onclick={() => timeline.setDateRange('', '')}>&times;</button>
				</span>
			{/if}
			<button class="clear-all" onclick={() => { timeline.setSearch(''); timeline.setDateRange('', ''); }}>
				Clear all
			</button>
		</div>
	{/if}

	<div class="table-wrapper">
		<table>
			<thead>
				<tr>
					<th
						class="sortable col-date-head"
						onclick={() => timeline.setSort('date')}
						onkeydown={handleKeydown}
						tabindex="0"
						role="columnheader"
						aria-sort={timeline.sortField === 'date' ? (timeline.sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}
					>
						Date
						{#if timeline.sortField === 'date'}
							<span class="sort-indicator">{timeline.sortDir === 'asc' ? '↑' : '↓'}</span>
						{/if}
					</th>
					<th
						class="sortable"
						onclick={() => timeline.setSort('title')}
						onkeydown={handleKeydown}
						tabindex="0"
						role="columnheader"
						aria-sort={timeline.sortField === 'title' ? (timeline.sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}
					>
						Title
						{#if timeline.sortField === 'title'}
							<span class="sort-indicator">{timeline.sortDir === 'asc' ? '↑' : '↓'}</span>
						{/if}
					</th>
					<th>Tags</th>
				</tr>
			</thead>
			<tbody>
				{#each timeline.paginated as event (event.id)}
					<tr class="event-row" style="border-left: 3px solid {event.importance >= 8 ? '#ef4444' : event.importance >= 6 ? '#f59e0b' : 'transparent'}">
						<td class="col-date">
							<span class="date-text">{event.date}</span>
						</td>
						<td class="col-title">
							<a href="{SITE_BASE}/{encodeURIComponent(event.id)}" class="event-title" onclick={(e) => openEvent(event, e)}>
								{event.title}
							</a>
							{#if event.summary}
								<div class="event-summary">{event.summary.substring(0, 120)}{event.summary.length > 120 ? '...' : ''}</div>
							{/if}
							{#if event.body}
								<div class="event-preview">{event.body.substring(0, 120)}{event.body.length > 120 ? '...' : ''}</div>
							{/if}
						</td>
						<td class="col-tags">
							<div class="tags-list">
								{#each (event.tags || []).slice(0, 3) as tag}
									<button class="tag tag-clickable" onclick={(e) => { e.stopPropagation(); timeline.setSearch(tag); }} title="Filter by {tag}">{tag}</button>
								{/each}
								{#if (event.tags || []).length > 3}
									<span class="tag tag-overflow" title={(event.tags || []).slice(3).join(', ')}>+{(event.tags || []).length - 3}</span>
								{/if}
							</div>
						</td>
					</tr>
				{:else}
					<tr>
						<td colspan="3" class="empty-state">
							{#if timeline.search || timeline.dateFrom || timeline.dateTo}
								No events matching current filters
							{:else}
								No events found.
							{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	{#if timeline.totalPages > 1}
		<div class="pagination">
			<button
				class="page-btn"
				disabled={timeline.page === 1}
				onclick={() => timeline.setPage(timeline.page - 1)}
			>
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="m15 18-6-6 6-6"/>
				</svg>
				Previous
			</button>

			<div class="page-info">
				<span class="page-current">{timeline.page}</span>
				<span class="page-sep">of</span>
				<span>{timeline.totalPages}</span>
			</div>

			<button
				class="page-btn"
				disabled={timeline.page >= timeline.totalPages}
				onclick={() => timeline.setPage(timeline.page + 1)}
			>
				Next
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="m9 18 6-6-6-6"/>
				</svg>
			</button>
		</div>
	{/if}
</div>

{#if selectedEvent}
	<EventPanel event={selectedEvent} onclose={closePanel} />
{/if}

<style>
	.table-container {
		padding: 1.5rem;
		max-width: 100%;
	}

	/* ── Controls ────────────────────────────────────────── */
	.table-controls {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.25rem;
		gap: 1rem;
		flex-wrap: wrap;
	}
	.controls-left {
		display: flex;
		align-items: baseline;
		gap: 0.75rem;
	}
	.controls-left h2 {
		font-size: 1.25rem;
		font-weight: 600;
	}
	.stats-bar {
		font-size: 0.75rem;
		color: var(--ink-faint);
	}
	.result-count {
		font-size: 0.8125rem;
		color: var(--ink-muted);
	}

	.search-box {
		display: flex;
		align-items: center;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		padding: 0.5rem 0.75rem;
		gap: 0.5rem;
		width: 320px;
		transition: border-color 0.15s;
	}
	.search-box:focus-within {
		border-color: var(--gold-border);
	}
	.search-box svg {
		color: var(--ink-faint);
		flex-shrink: 0;
	}
	.search-box input {
		flex: 1;
		border: none;
		background: transparent;
		color: var(--ink);
		font-size: 0.875rem;
		outline: none;
		padding: 0;
		font-family: inherit;
	}
	.search-box input::placeholder {
		color: var(--ink-faint);
	}
	.clear-btn {
		background: none;
		border: none;
		color: var(--ink-muted);
		cursor: pointer;
		padding: 2px;
		display: flex;
		border-radius: 2px;
	}
	.clear-btn:hover {
		color: var(--ink);
	}

	/* ── Date filter ────────────────────────────────────────── */
	.date-filter {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 1rem;
		flex-wrap: wrap;
	}
	.date-label {
		display: flex;
		align-items: center;
		gap: 0.375rem;
		font-size: 0.8125rem;
		color: var(--ink-muted);
	}
	.date-input {
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.375rem;
		padding: 0.375rem 0.5rem;
		color: var(--ink);
		font-size: 0.8125rem;
		font-family: inherit;
		outline: none;
		transition: border-color 0.15s;
		color-scheme: dark;
	}
	.date-input:focus {
		border-color: var(--gold-border);
	}
	.date-clear-btn {
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.375rem;
		padding: 0.375rem 0.75rem;
		color: var(--ink-muted);
		font-size: 0.8125rem;
		font-family: inherit;
		cursor: pointer;
		transition: all 0.15s;
	}
	.date-clear-btn:hover {
		border-color: var(--border-light);
		color: var(--ink);
		background: var(--surface-raised);
	}

	/* ── Filter bar ─────────────────────────────────────────── */
	.filter-bar {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
		flex-wrap: wrap;
	}
	.filter-chip {
		display: inline-flex;
		align-items: center;
		gap: 0.375rem;
		background: var(--gold-glow);
		border: 1px solid var(--gold-border);
		border-radius: 999px;
		padding: 0.25rem 0.625rem;
		font-size: 0.8125rem;
		color: var(--ink-soft);
		font-family: inherit;
		line-height: 1.4;
	}
	.chip-dismiss {
		background: none;
		border: none;
		color: var(--ink-muted);
		cursor: pointer;
		padding: 0;
		font-size: 1rem;
		line-height: 1;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		width: 1.125rem;
		height: 1.125rem;
		transition: all 0.15s;
	}
	.chip-dismiss:hover {
		color: var(--ink);
		background: var(--surface-overlay);
	}
	.clear-all {
		background: none;
		border: none;
		color: var(--ink-faint);
		cursor: pointer;
		font-size: 0.75rem;
		font-family: inherit;
		padding: 0.25rem 0.5rem;
		transition: color 0.15s;
	}
	.clear-all:hover {
		color: var(--ink);
	}

	/* ── Table ───────────────────────────────────────────── */
	.table-wrapper {
		overflow-x: auto;
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		background: var(--surface-raised);
	}
	table {
		width: 100%;
		border-collapse: collapse;
	}

	thead {
		background: var(--surface-overlay);
	}
	th {
		text-align: left;
		padding: 0.75rem 1rem;
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--ink-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		border-bottom: 1px solid var(--border);
		white-space: nowrap;
		user-select: none;
	}
	th.sortable {
		cursor: pointer;
	}
	th.sortable:hover {
		color: var(--ink-soft);
	}
	.sort-indicator {
		margin-left: 0.25rem;
		color: var(--gold);
	}

	.col-date-head { width: 110px; }
	/* ── Rows ────────────────────────────────────────────── */
	.event-row {
		transition: background 0.1s;
	}
	.event-row:hover {
		background: var(--surface-overlay);
	}

	td {
		padding: 0.75rem 1rem;
		border-bottom: 1px solid var(--border);
		vertical-align: top;
		font-size: 0.875rem;
	}

	.col-date {
		white-space: nowrap;
	}
	.date-text {
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.8125rem;
		color: var(--ink-muted);
	}

	.col-title {
		max-width: 500px;
	}

	.event-title {
		font-weight: 500;
		color: var(--ink);
		transition: color 0.15s;
	}
	.event-title:hover {
		color: var(--gold);
		text-decoration: none;
	}

	.event-summary {
		font-size: 0.8125rem;
		color: var(--ink-muted);
		margin-top: 0.25rem;
		line-height: 1.4;
	}

	.event-preview {
		display: none;
		font-size: 0.8125rem;
		color: var(--ink-muted);
		margin-top: 0.25rem;
		line-height: 1.4;
	}
	.event-row:hover .event-preview {
		display: block;
	}

	.col-tags {
		min-width: 150px;
	}
	.tags-list {
		display: flex;
		gap: 0.25rem;
		flex-wrap: wrap;
	}

	.empty-state {
		text-align: center;
		padding: 3rem 1rem !important;
		color: var(--ink-muted);
		font-style: italic;
	}

	/* ── Pagination ──────────────────────────────────────── */
	.pagination {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1.5rem;
		margin-top: 1rem;
		padding: 0.75rem 0;
	}

	.page-btn {
		display: flex;
		align-items: center;
		gap: 0.375rem;
		padding: 0.5rem 0.875rem;
		background: var(--surface-raised);
		border: 1px solid var(--border);
		border-radius: 0.375rem;
		color: var(--ink-soft);
		font-size: 0.8125rem;
		font-weight: 500;
		font-family: inherit;
		cursor: pointer;
		transition: all 0.15s;
	}
	.page-btn:not(:disabled):hover {
		border-color: var(--border-light);
		color: var(--ink);
		background: var(--surface-overlay);
	}
	.page-btn:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	.page-info {
		font-size: 0.8125rem;
		color: var(--ink-muted);
		display: flex;
		align-items: center;
		gap: 0.375rem;
	}
	.page-current {
		color: var(--ink);
		font-weight: 600;
	}
	.page-sep {
		color: var(--ink-faint);
	}

	.tag-clickable {
		cursor: pointer;
		border: none;
		font-family: inherit;
	}
	.tag-clickable:hover {
		background: var(--gold-glow);
		border-color: var(--gold-border);
		color: var(--gold);
	}

	/* ── Responsive ──────────────────────────────────────── */
	@media (max-width: 768px) {
		.table-container {
			padding: 1rem;
		}
		.table-controls {
			flex-direction: column;
			align-items: stretch;
		}
		.search-box {
			width: 100%;
		}
		.date-filter {
			flex-direction: column;
			align-items: stretch;
		}
		.date-label {
			justify-content: space-between;
		}
		.date-input {
			flex: 1;
		}
		.col-tags {
			display: none;
		}
		.controls-left h2 {
			font-size: 1.1rem;
		}
	}
</style>
