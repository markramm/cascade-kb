<script lang="ts">
	import { timeline } from '$lib/stores/timeline.svelte';

	let { count }: { count: number } = $props();

	const navItems = [
		{ view: 'table' as const, label: 'Timeline', icon: 'table' },
		{ view: 'd3' as const, label: 'Visual Timeline', icon: 'chart' }
	];
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
		flex: 1;
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

	@media (max-width: 768px) {
		.sidebar {
			width: 3.5rem;
		}
		.brand-name,
		.brand-sub,
		.sidebar-footer .nav-item :global(svg ~ *) {
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
