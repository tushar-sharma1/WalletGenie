import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    // Use relative URLs so it works both locally and in production
    private baseUrl = 'https://walletgenie-1063411215664.us-central1.run.app';

    constructor(private http: HttpClient) { }

    uploadCsv(file: File): Observable<any> {
        const formData = new FormData();
        formData.append('file', file);
        return this.http.post(`${this.baseUrl}/upload`, formData);
    }

    getSummary(): Observable<any> {
        return this.http.get(`${this.baseUrl}/summary`);
    }

    chat(message: string): Observable<any> {
        return this.http.post(`${this.baseUrl}/chat`, { message });
    }
}
