import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface SeasonalEventItem {
    id: number;
    name: string;
    event_date: string;
    prep_start: string | null;
    category: string;
    niches: string;
    strategy_notes: string;
    status: string;
    days_until: number | null;
    is_prep_phase: boolean;
}

export async function listEvents(category?: string): Promise<SeasonalEventItem[]> {
    const qs = category ? `?category=${category}` : "";
    return getData<SeasonalEventItem[]>(`/seasonal${qs}`);
}

export async function seedEvents() {
    return postData<{ created: number }, {}>("/seasonal/seed", {});
}

export async function getUpcomingEvents(days = 60): Promise<SeasonalEventItem[]> {
    return getData<SeasonalEventItem[]>(`/seasonal/upcoming?days=${days}`);
}

export async function createEvent(payload: {
    name: string;
    event_date: string;
    prep_start?: string;
    category?: string;
    niches?: string;
    strategy_notes?: string;
}) {
    return postData<{ id: number; name: string }, typeof payload>("/seasonal", payload);
}

export async function updateEvent(id: number, payload: { status?: string; strategy_notes?: string }) {
    const response = await api.patch(`/seasonal/${id}`, payload);
    return response.data.data;
}

export async function deleteEvent(id: number) {
    return deleteData(`/seasonal/${id}`);
}
