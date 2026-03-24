<script lang="ts">
	import { timeline } from '$lib/stores/timeline.svelte';
	import TimelineTable from '$lib/components/TimelineTable.svelte';
	import TimelineView from '$lib/components/TimelineView.svelte';
</script>

<svelte:head>
	<title>Capture Cascade Timeline — {timeline.events.length.toLocaleString()} events</title>
</svelte:head>

{#if timeline.view === 'table'}
	<TimelineTable />
{:else}
	<TimelineView />
{/if}
