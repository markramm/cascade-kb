<script lang="ts">
	import { timeline } from '$lib/stores/timeline.svelte';
	import * as d3 from 'd3';
	import type { TimelineEvent } from '$lib/types';

	const MARGIN = { top: 20, right: 30, bottom: 30, left: 80 };
	const SITE_BASE = '/site/cascade-timeline';
	const GROUPS = ['legislative', 'judicial', 'financial', 'corporate', 'political', 'cultural', 'other'];
	const GROUP_COLORS: Record<string, string> = {
		legislative: 'var(--cat-legislative)',
		judicial: 'var(--cat-judicial)',
		financial: 'var(--cat-financial)',
		corporate: 'var(--cat-corporate)',
		political: 'var(--cat-political)',
		cultural: 'var(--cat-cultural)',
		other: 'var(--cat-other)'
	};

	let wrapper: HTMLDivElement;
	let svg: SVGSVGElement;
	let width = $state(0);
	let height = $state(0);
	let currentTransform = $state(d3.zoomIdentity);
	let tooltip = $state<{ x: number; y: number; event: TimelineEvent } | null>(null);

	// Keep a reference to the zoom behavior so controls can call it
	let zoomBehavior = $state<d3.ZoomBehavior<SVGSVGElement, unknown> | null>(null);

	// Resize observer
	function observeResize(node: HTMLDivElement) {
		const ro = new ResizeObserver((entries) => {
			const entry = entries[0];
			if (entry) {
				width = entry.contentRect.width;
				height = entry.contentRect.height;
			}
		});
		ro.observe(node);
		return {
			destroy() {
				ro.disconnect();
			}
		};
	}

	// Full time domain from sorted events
	const fullTimeDomain = $derived.by(() => {
		const events = timeline.events;
		if (!events.length) return [new Date(), new Date()] as [Date, Date];

		// Find min/max dates
		let min = events[0].date;
		let max = events[0].date;
		for (const e of events) {
			if (e.date < min) min = e.date;
			if (e.date > max) max = e.date;
		}
		const start = new Date(min);
		const end = new Date(max);
		const padding = (end.getTime() - start.getTime()) * 0.05;
		return [new Date(start.getTime() - padding), new Date(end.getTime() + padding)] as [Date, Date];
	});

	// ── Zoom control helpers ─────────────────────────────────────
	function zoomIn() {
		if (!svg || !zoomBehavior) return;
		d3.select(svg).transition().duration(300).call(zoomBehavior.scaleBy as any, 1.5);
	}

	function zoomOut() {
		if (!svg || !zoomBehavior) return;
		d3.select(svg).transition().duration(300).call(zoomBehavior.scaleBy as any, 1 / 1.5);
	}

	function fitAll() {
		if (!svg || !zoomBehavior) return;
		d3.select(svg).transition().duration(300).call(zoomBehavior.transform as any, d3.zoomIdentity);
	}

	function zoomToDateRange(startDate: Date, endDate: Date) {
		if (!svg || !zoomBehavior || !width) return;

		const xScale = d3.scaleTime()
			.domain(fullTimeDomain)
			.range([MARGIN.left, width - MARGIN.right]);

		const x1 = xScale(startDate);
		const x2 = xScale(endDate);
		const chartWidth = width - MARGIN.left - MARGIN.right;

		if (x2 - x1 <= 0) return;

		const k = chartWidth / (x2 - x1);
		const tx = MARGIN.left - x1 * k;

		d3.select(svg)
			.transition()
			.duration(400)
			.call(zoomBehavior.transform as any, d3.zoomIdentity.translate(tx, 0).scale(k));
	}

	function panBy(deltaX: number) {
		if (!svg || !zoomBehavior) return;
		d3.select(svg).transition().duration(150).call(zoomBehavior.translateBy as any, deltaX, 0);
	}

	// ── Keyboard shortcuts ───────────────────────────────────────
	function handleKeydown(e: KeyboardEvent) {
		// Only handle when timeline view is active and no input is focused
		const tag = (e.target as HTMLElement)?.tagName;
		if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

		switch (e.key) {
			case '+':
			case '=':
				e.preventDefault();
				zoomIn();
				break;
			case '-':
				e.preventDefault();
				zoomOut();
				break;
			case '0':
			case 'Home':
				e.preventDefault();
				fitAll();
				break;
			case 'ArrowLeft':
				e.preventDefault();
				panBy(80);
				break;
			case 'ArrowRight':
				e.preventDefault();
				panBy(-80);
				break;
		}
	}

	// ── Date range preset definitions ────────────────────────────
	const datePresets = [
		{ label: 'All', action: () => fitAll() },
		{ label: '2020s', action: () => zoomToDateRange(new Date('2020-01-01'), new Date('2029-12-31')) },
		{ label: '2025', action: () => zoomToDateRange(new Date('2025-01-01'), new Date('2025-12-31')) },
		{ label: '2026', action: () => zoomToDateRange(new Date('2026-01-01'), new Date('2026-12-31')) }
	];

	// D3 render effect
	$effect(() => {
		if (!svg || !width || !height || !timeline.events.length) return;

		const svgEl = d3.select(svg).attr('width', width).attr('height', height);
		svgEl.selectAll('*').remove();

		// Clipping rect
		svgEl.append('defs').append('clipPath').attr('id', 'chart-clip')
			.append('rect')
			.attr('x', MARGIN.left)
			.attr('y', MARGIN.top)
			.attr('width', width - MARGIN.left - MARGIN.right)
			.attr('height', height - MARGIN.top - MARGIN.bottom);

		// Scales
		const xScale = d3.scaleTime()
			.domain(fullTimeDomain)
			.range([MARGIN.left, width - MARGIN.right]);

		const k = currentTransform.k;
		const newXScale = currentTransform.rescaleX(xScale);

		const yScale = d3.scalePoint()
			.domain(GROUPS)
			.range([MARGIN.top + 20, height - MARGIN.bottom - 10])
			.padding(0.5);

		// Zoom behavior
		const zoom = d3.zoom<SVGSVGElement, unknown>()
			.scaleExtent([1, 1000])
			.extent([[MARGIN.left, MARGIN.top], [width - MARGIN.right, height - MARGIN.bottom]])
			.translateExtent([[MARGIN.left, -Infinity], [width - MARGIN.right, Infinity]])
			.on('zoom', (event) => {
				currentTransform = event.transform;
			});

		// Store zoom behavior for controls
		zoomBehavior = zoom;

		svgEl.call(zoom as any).on('dblclick.zoom', null);

		// Restore transform
		if (currentTransform !== d3.zoomIdentity) {
			svgEl.call(zoom.transform as any, currentTransform);
		}

		// Grid & lane labels
		const gridG = svgEl.append('g').attr('class', 'grid');
		for (const group of GROUPS) {
			const y = yScale(group);
			if (y === undefined) continue;

			gridG.append('line')
				.attr('x1', MARGIN.left)
				.attr('x2', width - MARGIN.right)
				.attr('y1', y)
				.attr('y2', y)
				.attr('stroke', 'var(--border)')
				.attr('stroke-width', 1)
				.attr('stroke-dasharray', '4,4');

			gridG.append('text')
				.attr('x', MARGIN.left - 8)
				.attr('y', y + 5)
				.attr('text-anchor', 'end')
				.style('fill', 'var(--ink-soft)')
				.style('font-size', '12px')
				.style('font-weight', '500')
				.style('font-family', "'DM Sans', sans-serif")
				.text(group.charAt(0).toUpperCase() + group.slice(1));
		}

		// X-axis
		svgEl.append('g')
			.attr('transform', `translate(0, ${height - MARGIN.bottom})`)
			.call(d3.axisBottom(newXScale).ticks(Math.max(2, Math.floor(width / 120))))
			.call((g) => {
				g.selectAll('text').style('fill', 'var(--ink-muted)').style('font-size', '11px');
				g.selectAll('line').style('stroke', 'var(--border-light)');
				g.select('.domain').style('stroke', 'var(--border-light)');
			});

		// Visible events
		const [viewStart, viewEnd] = newXScale.domain();
		const visibleEvents = timeline.events.filter((e) => {
			const d = new Date(e.date);
			return d >= viewStart && d <= viewEnd;
		});

		const FORCE_AGGREGATION = visibleEvents.length > 800 || k < 1.5;

		const chartG = svgEl.append('g').attr('clip-path', 'url(#chart-clip)');

		if (FORCE_AGGREGATION) {
			// Histogram mode
			const tickCount = Math.min(width / 10, 100);
			const bucketGenerator = d3.bin<TimelineEvent, Date>()
				.value((d) => new Date(d.date))
				.domain(newXScale.domain() as [Date, Date])
				.thresholds(newXScale.ticks(tickCount));

			const buckets = bucketGenerator(visibleEvents);
			const maxCount = d3.max(buckets, (b) => b.length) || 1;

			const barHeightScale = d3.scaleLinear()
				.domain([0, maxCount])
				.range([0, height - MARGIN.bottom - MARGIN.top]);

			chartG.selectAll('rect.bar')
				.data(buckets)
				.enter()
				.append('rect')
				.attr('class', 'bar')
				.attr('x', (d) => newXScale(d.x0 || new Date()))
				.attr('y', (d) => height - MARGIN.bottom - barHeightScale(d.length))
				.attr('width', (d) => Math.max(1, newXScale(d.x1 || new Date()) - newXScale(d.x0 || new Date()) - 1))
				.attr('height', (d) => barHeightScale(d.length))
				.attr('fill', 'var(--info)')
				.attr('opacity', 0.5)
				.attr('rx', 1);

			// Dim grid in dense mode
			gridG.style('opacity', 0.15);

			// Zoom hint
			if (visibleEvents.length > 800) {
				svgEl.append('text')
					.attr('x', width / 2)
					.attr('y', MARGIN.top + 20)
					.attr('text-anchor', 'middle')
					.style('fill', 'var(--ink-faint)')
					.style('font-size', '12px')
					.style('font-family', "'DM Sans', sans-serif")
					.text(`${visibleEvents.length.toLocaleString()} events · Zoom in to see details`);
			}
		} else {
			// Individual events mode
			gridG.style('opacity', 1);

			// Deterministic jitter from event id
			function jitter(id: string): number {
				let hash = 0;
				for (let i = 0; i < id.length; i++) {
					hash = ((hash << 5) - hash + id.charCodeAt(i)) | 0;
				}
				return ((hash % 20) - 10);
			}

			chartG.selectAll('circle')
				.data(visibleEvents)
				.enter()
				.append('circle')
				.attr('cx', (d) => newXScale(new Date(d.date)))
				.attr('cy', (d) => {
					const baseY = yScale(d.group || d.type || 'other') || height / 2;
					return baseY + jitter(d.id);
				})
				.attr('r', k < 3 ? 4 : 6)
				.attr('fill', (d) => GROUP_COLORS[d.group || d.type || 'other'] || GROUP_COLORS.other)
				.attr('stroke', (d) => timeline.selectedIds.has(d.id) ? 'var(--ink)' : 'none')
				.attr('stroke-width', 2)
				.attr('opacity', 0.8)
				.style('cursor', 'pointer')
				.on('click', (e: MouseEvent, d: TimelineEvent) => {
					e.stopPropagation();
					timeline.selectEvent(d.id, e.shiftKey || e.metaKey);
				})
				.on('mouseenter', (e: MouseEvent, d: TimelineEvent) => {
					const rect = wrapper.getBoundingClientRect();
					tooltip = {
						x: e.clientX - rect.left,
						y: e.clientY - rect.top - 10,
						event: d
					};
				})
				.on('mouseleave', () => {
					tooltip = null;
				});

			// Labels at deep zoom
			if (k > 4 && visibleEvents.length < 100) {
				chartG.selectAll('text.label')
					.data(visibleEvents)
					.enter()
					.append('text')
					.attr('class', 'label')
					.attr('x', (d) => newXScale(new Date(d.date)))
					.attr('y', (d) => (yScale(d.group || d.type || 'other') || height / 2) - 12)
					.text((d) => d.title.length > 30 ? d.title.substring(0, 30) + '...' : d.title)
					.style('fill', 'var(--ink-soft)')
					.style('font-size', '10px')
					.style('font-family', "'DM Sans', sans-serif")
					.style('text-anchor', 'middle')
					.style('pointer-events', 'none');
			}
		}

		// Click to navigate
		svgEl.on('click', (e: MouseEvent) => {
			const target = e.target as Element;
			if (target.tagName === 'circle') {
				const d = d3.select(target).datum() as TimelineEvent;
				if (d && !e.shiftKey && !e.metaKey) {
					window.location.href = `${SITE_BASE}/${encodeURIComponent(d.id)}`;
				}
			}
		});
	});
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="timeline-view" bind:this={wrapper} use:observeResize>
	<svg bind:this={svg}></svg>

	<!-- Zoom level indicator -->
	<div class="zoom-badge">
		{currentTransform.k.toFixed(1)}x
	</div>

	<!-- Floating control panel -->
	<div class="controls-panel">
		<!-- Date range presets -->
		<div class="presets-row">
			{#each datePresets as preset}
				<button
					class="preset-btn"
					onclick={() => preset.action()}
					title="Jump to {preset.label}"
				>
					{preset.label}
				</button>
			{/each}
		</div>

		<div class="controls-divider"></div>

		<!-- Zoom buttons -->
		<div class="zoom-buttons">
			<button class="zoom-btn" onclick={zoomIn} title="Zoom in (+)">
				<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
					<line x1="8" y1="3" x2="8" y2="13" />
					<line x1="3" y1="8" x2="13" y2="8" />
				</svg>
			</button>
			<button class="zoom-btn" onclick={zoomOut} title="Zoom out (-)">
				<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
					<line x1="3" y1="8" x2="13" y2="8" />
				</svg>
			</button>
			<button class="zoom-btn" onclick={fitAll} title="Fit all (0 / Home)">
				<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5">
					<path d="M8 2 L14 7 L14 14 L2 14 L2 7 Z" />
					<rect x="6" y="9" width="4" height="5" />
				</svg>
			</button>
		</div>

		<div class="controls-hint">
			<kbd>+</kbd><kbd>-</kbd> zoom &middot; <kbd>&larr;</kbd><kbd>&rarr;</kbd> pan
		</div>
	</div>

	<!-- Tooltip -->
	{#if tooltip}
		<div
			class="tooltip"
			style="left: {tooltip.x}px; top: {tooltip.y}px;"
		>
			<div class="tooltip-date">{tooltip.event.date}</div>
			<div class="tooltip-title">{tooltip.event.title}</div>
			{#if tooltip.event.summary}
				<div class="tooltip-summary">{tooltip.event.summary.substring(0, 80)}...</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.timeline-view {
		width: 100%;
		height: 100%;
		position: relative;
		overflow: hidden;
		background: var(--surface);
	}

	svg {
		display: block;
	}

	.zoom-badge {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		padding: 0.25rem 0.5rem;
		font-size: 0.6875rem;
		font-family: 'JetBrains Mono', monospace;
		color: var(--ink-muted);
	}

	/* ── Floating control panel ────────────────────────────────── */
	.controls-panel {
		position: absolute;
		bottom: 1rem;
		right: 1rem;
		background: rgba(31, 31, 35, 0.92);
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		padding: 0.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.375rem;
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		z-index: 5;
	}

	.presets-row {
		display: flex;
		gap: 0.25rem;
	}

	.preset-btn {
		flex: 1;
		padding: 0.25rem 0.5rem;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		color: var(--ink-soft);
		font-family: 'DM Sans', sans-serif;
		font-size: 0.6875rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.15s ease;
		white-space: nowrap;
	}

	.preset-btn:hover {
		background: var(--gold-glow);
		border-color: var(--gold-border);
		color: var(--gold);
	}

	.controls-divider {
		height: 1px;
		background: var(--border);
		margin: 0.125rem 0;
	}

	.zoom-buttons {
		display: flex;
		gap: 0.25rem;
	}

	.zoom-btn {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.375rem;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.25rem;
		color: var(--ink-soft);
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.zoom-btn:hover {
		background: var(--gold-glow);
		border-color: var(--gold-border);
		color: var(--gold);
	}

	.zoom-btn:active {
		transform: scale(0.95);
	}

	.controls-hint {
		text-align: center;
		font-size: 0.5625rem;
		color: var(--ink-faint);
		font-family: 'DM Sans', sans-serif;
		padding-top: 0.125rem;
	}

	.controls-hint kbd {
		display: inline-block;
		padding: 0 0.2rem;
		background: var(--surface-overlay);
		border: 1px solid var(--border);
		border-radius: 0.15rem;
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.5rem;
		color: var(--ink-muted);
		line-height: 1.4;
	}

	.tooltip {
		position: absolute;
		pointer-events: none;
		transform: translate(-50%, -100%);
		background: var(--surface-raised);
		border: 1px solid var(--border-light);
		border-radius: 0.5rem;
		padding: 0.625rem 0.75rem;
		max-width: 280px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		z-index: 10;
	}
	.tooltip-date {
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.6875rem;
		color: var(--gold);
		margin-bottom: 0.25rem;
	}
	.tooltip-title {
		font-weight: 600;
		font-size: 0.8125rem;
		color: var(--ink);
		line-height: 1.3;
	}
	.tooltip-summary {
		font-size: 0.75rem;
		color: var(--ink-muted);
		margin-top: 0.25rem;
		line-height: 1.3;
	}
</style>
