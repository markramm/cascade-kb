export interface TimelineEvent {
	id: string;
	title: string;
	date: string;
	summary: string;
	content?: string;
	type?: 'legislative' | 'judicial' | 'financial' | 'corporate' | 'political' | 'cultural';
	tags: string[];
	entities?: string[];
	importance: number;
	status: 'confirmed' | 'likely' | 'disputed' | 'retracted';
	sources: Array<{
		url: string;
		title?: string;
		date_accessed?: string;
		tier?: '1' | '2' | '3';
	}>;
	group?: string;
}
