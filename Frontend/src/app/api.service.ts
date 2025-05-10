import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // Define the URL to your Django backend API
  private apiUrl = 'http://18.188.170.181:8000/api/nl_query/'; // Adjust the URL as needed

  constructor(private http: HttpClient) {}

  // Method to send the natural language query to the Django backend
  processNaturalLanguageQuery(query: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { query });
  }
}