<script lang="ts">
	import { timeline } from '$lib/stores/timeline.svelte';

	let { count }: { count: number } = $props();

	let actorFilter = $state('');

	const navItems = [
		{ view: 'table' as const, label: 'Timeline', icon: 'table' },
		{ view: 'd3' as const, label: 'Visual Timeline', icon: 'chart' }
	];

	const filteredActors = $derived.by(() => {
		const actors = timeline.topActors;
		if (!actorFilter) return actors.slice(0, 20);
		const q = actorFilter.toLowerCase();
		return actors.filter((a) => a.name.toLowerCase().includes(q)).slice(0, 20);
	});
</script>

<aside class="sidebar">
	<div class="sidebar-header">
		<a href="/site/cascade-timeline" class="sidebar-brand">
			<span class="brand-mark">CC</span>
			<div>
				<div class="brand-name">Capture Cascade</div>
				<div class="brand-sub">{count.toLocaleString()} events</div>
			</div>
		</a>
	</div>

	<nav class="sidebar-nav">
		{#each navItems as item}
			<button
				class="nav-item"
				class:active={timeline.view === item.view}
				onclick={() => timeline.setView(item.view)}
			>
				{#if item.icon === 'table'}
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
						<line x1="3" y1="9" x2="21" y2="9"/>
						<line x1="3" y1="15" x2="21" y2="15"/>
						<line x1="9" y1="3" x2="9" y2="21"/>
					</svg>
				{:else}
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<circle cx="12" cy="12" r="10"/>
						<polyline points="12 6 12 12 16 14"/>
					</svg>
				{/if}
				{item.label}
			</button>
		{/each}
	</nav>

	<div class="sidebar-tags">
		<div class="tags-header">Top Tags</div>
		<div class="tags-chips">
			{#each timeline.topTags.slice(0, 12) as tag}
				<button
					class="tag-chip"
					class:active={timeline.search === tag.name}
					onclick={() => timeline.setSearch(timeline.search === tag.name ? '' : tag.name)}
					title="{tag.name} ({tag.count})"
				>
					{tag.name}
					<span class="tag-count">{tag.count}</span>
				</button>
			{/each}
		</div>
	</div>

	<div class="sidebar-actors">
		<div class="actors-header">Actors</div>
		<input
			type="text"
			class="actor-search"
			placeholder="Search actors..."
			bind:value={actorFilter}
		/>
		<div class="actor-list">
			{#each filteredActors as actor}
				<button
					class="actor-item"
					class:active={timeline.search === actor.name}
					onclick={() => timeline.setSearch(timeline.search === actor.name ? '' : actor.name)}
					title="{actor.name} ({actor.count} events)"
				>
					<span class="actor-name">{actor.name}</span>
					<span class="actor-count">{actor.count}</span>
				</button>
			{/each}
			{#if filteredActors.length === 0}
				<div class="actor-empty">No actors found</div>
			{/if}
		</div>
	</div>

	<div class="sidebar-footer">
		<a href="/site/cascade-timeline" class="nav-item">
			<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
				<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
			</svg>
			Browse KB
		</a>
	</div>
</aside>

<style>
	.sidebar {
		width: 14rem;
		background: var(--surface-raised);
		border-right: 1px solid var(--border);
		display: flex;
		flex-direction: column;
		flex-shrink: 0;
	}

	.sidebar-header {
		padding: 1.25rem;
		border-bottom: 1px solid var(--border);
	}

	.sidebar-brand {
		display: flex;
		align-items: center;
		gap: 0.625rem;
		text-decoration: none;
		color: var(--ink);
	}
	.sidebar-brand:hover {
		text-decoration: none;
		color: var(--ink);
	}

	.brand-mark {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 2rem;
		height: 2rem;
		border-radius: 0.375rem;
		background: linear-gradient(135deg, var(--gold), var(--gold-dim));
		color: var(--surface);
		font-size: 0.75rem;
		font-weight: 700;
		flex-shrink: 0;
	}

	.brand-name {
		font-weight: 600;
		font-size: 0.875rem;
	}
	.brand-sub {
		font-size: 0.6875rem;
		color: var(--ink-muted);
	}

	.sidebar-nav {
		flex-shrink: 0;
		padding: 0.75rem 0;
	}

	.nav-item {
		display: flex;
		align-items: center;
		gap: 0.625rem;
		width: 100%;
		padding: 0.5rem 1.25rem;
		color: var(--ink-soft);
		text-decoration: none;
		font-size: 0.8125rem;
		font-weight: 500;
		background: none;
		border: none;
		cursor: pointer;
		font-family: inherit;
		transition: all 0.15s;
		text-align: left;
	}
	.nav-item:hover {
		color: var(--ink);
		background: var(--surface-overlay);
		text-decoration: none;
	}
	.nav-item.active {
		color: var(--gold);
		background: var(--gold-glow);
		border-right: 2px solid var(--gold);
	}

	.sidebar-footer {
		padding: 0.75rem 0;
		border-top: 1px solid var(--border);
	}
	.sidebar-footer .nav-item {
		color: var(--ink-soft);
	}

	.sidebar-tags {
		padding: 0.75rem 1.25rem;
		flex-shrink: 0;
	}
	.tags-header {
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--ink-faint);
		margin-bottom: 0.5rem;
	}
	.tags-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
	}
	.tag-chip {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.2rem 0.5rem;
		font-size: 0.6875rem;
		font-family: inherit;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		color: var(--ink-soft);
		cursor: pointer;
		transition: all 0.15s;
		white-space: nowrap;
	}
	.tag-chip:hover {
		border-color: var(--gold-border);
		color: var(--gold);
	}
	.tag-chip.active {
		background: var(--gold-glow);
		border-color: var(--gold-border);
		color: var(--gold);
	}
	.tag-count {
		font-size: 0.625rem;
		color: var(--ink-faint);
	}

	.sidebar-actors {
		padding: 0.75rem 1.25rem;
		flex: 1;
		overflow-y: auto;
		min-height: 0;
		border-top: 1px solid var(--border);
	}
	.actors-header {
		font-size: 0.6875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--ink-faint);
		margin-bottom: 0.5rem;
	}
	.actor-search {
		width: 100%;
		padding: 0.3rem 0.5rem;
		font-size: 0.75rem;
		font-family: inherit;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		color: var(--ink);
		margin-bottom: 0.5rem;
		outline: none;
		box-sizing: border-box;
	}
	.actor-search::placeholder {
		color: var(--ink-faint);
	}
	.actor-search:focus {
		border-color: var(--gold-border);
	}
	.actor-list {
		display: flex;
		flex-direction: column;
		gap: 1px;
	}
	.actor-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		padding: 0.3rem 0.5rem;
		font-size: 0.75rem;
		font-family: inherit;
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		color: var(--ink-soft);
		cursor: pointer;
		transition: all 0.15s;
		text-align: left;
	}
	.actor-item:hover {
		background: var(--surface-overlay);
		border-color: var(--gold-border);
		color: var(--gold);
	}
	.actor-item.active {
		background: var(--gold-glow);
		border-color: var(--gold-border);
		color: var(--gold);
	}
	.actor-name {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		flex: 1;
		min-width: 0;
	}
	.actor-count {
		font-size: 0.625rem;
		color: var(--ink-faint);
		flex-shrink: 0;
		margin-left: 0.5rem;
	}
	.actor-empty {
		font-size: 0.6875rem;
		color: var(--ink-faint);
		padding: 0.5rem;
		text-align: center;
	}

	@media (max-width: 768px) {
		.sidebar {
			position: fixed;
			left: 0;
			top: 0;
			bottom: 0;
			width: 3.5rem;
			z-index: 10;
		}
		.brand-name,
		.brand-sub,
		.sidebar-footer .nav-item :global(svg ~ *) {
			display: none;
		}
		.sidebar-tags {
			display: none;
		}
		.sidebar-actors {
			display: none;
		}
		.nav-item {
			justify-content: center;
			padding: 0.75rem;
		}
		/* Hide text labels on mobile, keep icons */
		.nav-item :global(svg ~ *) {
			display: none;
		}
	}
</style>
