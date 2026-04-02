<script lang="ts">
	import { timeline } from '$lib/stores/timeline.svelte';
	import type { TimelineEvent } from '$lib/types';
	import { onMount } from 'svelte';

	const SITE_BASE = '/site/cascade-timeline';

	let { event, onclose }: { event: TimelineEvent; onclose: () => void } = $props();
	let fullEvent = $state<TimelineEvent>(event);
	let loadingDetail = $state(!event.body);

	// Lazy-load body/sources if not present (lightweight index mode)
	onMount(async () => {
		if (!event.body) {
			const detail = await timeline.loadEventDetail(event.id);
			if (detail) fullEvent = detail;
			loadingDetail = false;
		}
	});

	function escapeHtml(text: string): string {
		return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
	}

	function renderBody(body: string): string {
		// Basic markdown-like rendering: paragraphs + bold
		return body
			.split('\n\n')
			.map(p => p.trim())
			.filter(Boolean)
			.map(p => `<p>${escapeHtml(p).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')}</p>`)
			.join('');
	}
</script>

<div class="panel-overlay" onclick={onclose} onkeydown={(e) => e.key === 'Escape' && onclose()} role="button" tabindex="-1">
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<aside class="panel" onclick={(e) => e.stopPropagation()} role="complementary">
		<header class="panel-header">
			<div class="panel-date">{event.date}</div>
			<button class="panel-close" onclick={onclose} aria-label="Close panel">
				<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M18 6 6 18"/><path d="m6 6 12 12"/>
				</svg>
			</button>
		</header>

		<h2 class="panel-title">{event.title}</h2>

		{#if event.status && event.status !== 'confirmed'}
			<span class="panel-status status-{event.status}">{event.status}</span>
		{/if}

		{#if event.actors && event.actors.length > 0}
			<div class="panel-actors">
				{#each event.actors as actor}
					<button class="actor-chip" onclick={() => { onclose(); timeline.setSearch(actor); }}>
						{actor}
					</button>
				{/each}
			</div>
		{/if}

		{#if event.capture_lanes && event.capture_lanes.length > 0}
			<div class="panel-lanes">
				{#each event.capture_lanes as lane}
					<button class="lane-badge" onclick={() => { onclose(); timeline.setSearch(lane); }}>{lane}</button>
				{/each}
			</div>
		{/if}

		{#if event.tags && event.tags.length > 0}
			<div class="panel-tags">
				{#each event.tags as tag}
					<button class="tag tag-clickable" onclick={() => { onclose(); timeline.setSearch(tag); }}>
						{tag}
					</button>
				{/each}
			</div>
		{/if}

		<div class="panel-body">
			{#if loadingDetail}
				<div class="loading-body">Loading details...</div>
			{:else}
				{@html renderBody(fullEvent.body || '')}
			{/if}
		</div>

		{#if fullEvent.sources && fullEvent.sources.length > 0}
			<div class="panel-sources">
				<h3>Sources ({fullEvent.sources.length})</h3>
				<ol>
					{#each fullEvent.sources as source}
						<li>
							{#if source.url}
								<a href={source.url} target="_blank" rel="noopener noreferrer">
									{source.title || source.url}
								</a>
							{:else}
								{source.title || 'Untitled source'}
							{/if}
							{#if source.outlet}
								<span class="source-outlet">— {source.outlet}</span>
							{/if}
							{#if source.date}
								<span class="source-date">({source.date})</span>
							{/if}
						</li>
					{/each}
				</ol>
			</div>
		{/if}

		<div class="panel-footer">
			<a href="{SITE_BASE}/{encodeURIComponent(event.id)}" class="full-page-link">
				View full page
				<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
					<polyline points="15 3 21 3 21 9" />
					<line x1="10" y1="14" x2="21" y2="3" />
				</svg>
			</a>
		</div>
	</aside>
</div>

<style>
	.panel-overlay {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(2px);
		z-index: 50;
		display: flex;
		justify-content: flex-end;
	}

	.panel {
		width: min(40rem, 90vw);
		height: 100vh;
		background: var(--surface-raised);
		border-left: 1px solid var(--border);
		overflow-y: auto;
		padding: 1.5rem;
		animation: slideIn 0.2s ease-out;
	}

	@keyframes slideIn {
		from { transform: translateX(100%); }
		to { transform: translateX(0); }
	}

	.panel-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}

	.panel-date {
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.875rem;
		color: var(--ink-muted);
	}

	.panel-close {
		background: none;
		border: none;
		color: var(--ink-muted);
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 0.25rem;
	}
	.panel-close:hover {
		color: var(--ink);
		background: var(--surface-overlay);
	}

	.panel-title {
		font-size: 1.5rem;
		font-weight: 700;
		line-height: 1.3;
		margin: 0 0 0.75rem 0;
		color: var(--ink);
	}

	.panel-status {
		display: inline-block;
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		padding: 0.15rem 0.5rem;
		border-radius: 0.25rem;
		margin-bottom: 0.75rem;
	}
	.status-reported, .status-alleged, .status-rumored {
		background: rgba(245, 158, 11, 0.15);
		color: #f59e0b;
	}
	.status-disputed {
		background: rgba(239, 68, 68, 0.15);
		color: #ef4444;
	}
	.status-draft {
		background: rgba(107, 114, 128, 0.15);
		color: #9ca3af;
	}

	.panel-actors {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		margin-bottom: 0.75rem;
	}
	.actor-chip {
		font-size: 0.75rem;
		font-family: inherit;
		padding: 0.15rem 0.5rem;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		color: var(--ink-soft);
		cursor: pointer;
		transition: all 0.15s;
	}
	.actor-chip:hover {
		border-color: var(--gold-border);
		color: var(--gold);
	}

	.panel-lanes {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		margin-bottom: 0.75rem;
	}
	.lane-badge {
		font-family: inherit;
		font-size: 0.6875rem;
		padding: 0.1rem 0.4rem;
		background: var(--gold-glow);
		border: 1px solid var(--gold-border);
		border-radius: 0.25rem;
		color: var(--gold);
		cursor: pointer;
		transition: all 0.15s;
	}
	.lane-badge:hover {
		background: var(--gold-border);
	}

	.panel-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		margin-bottom: 1rem;
	}

	.panel-body {
		color: var(--ink-soft);
		font-size: 0.9375rem;
		line-height: 1.7;
		margin-bottom: 1.5rem;
	}
	.panel-body :global(p) {
		margin: 0 0 0.75rem 0;
	}
	.loading-body {
		color: var(--ink-faint);
		font-style: italic;
		padding: 1rem 0;
	}

	.panel-sources {
		border-top: 1px solid var(--border);
		padding-top: 1rem;
		margin-bottom: 1rem;
	}
	.panel-sources h3 {
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--ink-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin: 0 0 0.5rem 0;
	}
	.panel-sources ol {
		padding-left: 1.25rem;
		font-size: 0.8125rem;
		color: var(--ink-soft);
	}
	.panel-sources li {
		margin-bottom: 0.375rem;
	}
	.panel-sources a {
		color: var(--gold);
	}
	.source-outlet, .source-date {
		color: var(--ink-faint);
		font-size: 0.75rem;
	}

	.panel-footer {
		border-top: 1px solid var(--border);
		padding-top: 1rem;
	}
	.full-page-link {
		display: inline-flex;
		align-items: center;
		gap: 0.375rem;
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--gold);
	}
	.full-page-link:hover {
		text-decoration: underline;
	}
</style>
