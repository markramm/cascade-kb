export interface TimelineEvent {
	id: string;
	title: string;
	date: string;
	body: string;
	tags: string[];
	actors: string[];
	importance: number;
	status: string;
	sources: Array<{
		title?: string;
		url?: string;
		outlet?: string;
		date?: string;
	}>;
	capture_lanes?: string[];
	location?: string;
	summary?: string;
}
