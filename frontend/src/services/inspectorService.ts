import { getData } from "./apiResponse";

export interface InspectionResult {
    file: string;
    line: number;
    severity: "error" | "warning" | "info";
    message: string;
    fixed: boolean;
    fix_detail: string;
}

export interface InspectionReport {
    total_checks: number;
    errors: number;
    warnings: number;
    info: number;
    status: string;
    results: InspectionResult[];
}

export async function runFullInspection(): Promise<InspectionReport> {
    return getData<InspectionReport>("/inspector/full");
}

export async function checkSyntax(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/syntax");
}

export async function checkImports(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/imports");
}

export async function checkModels(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/models");
}

export async function checkRoutes(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/routes");
}

export async function checkEnv(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/env");
}

export async function checkDatabase(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/database");
}

export async function checkLogs(): Promise<InspectionResult[]> {
    return getData<InspectionResult[]>("/inspector/logs");
}
