<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { timeline } from '$lib/stores/timeline.svelte';
	import { browser } from '$app/environment';

	let { children } = $props();

	if (browser) {
		timeline.load();
	}
</script>

{#if timeline.loading}
	<div class="loading-screen">
		<div class="loading-spinner"></div>
		<div class="loading-text">Loading Capture Cascade Timeline...</div>
	</div>
{:else if timeline.error}
	<div class="error-screen">
		<h2>Failed to load</h2>
		<p>{timeline.error}</p>
		<button onclick={() => timeline.load()}>Retry</button>
	</div>
{:else}
	<div class="app-shell">
		<Sidebar count={timeline.events.length} />
		<main class="app-main">
			{@render children()}
		</main>
	</div>
{/if}
