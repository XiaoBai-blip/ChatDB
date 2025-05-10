import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  
  private apiUrl = 'http://18.191.236.139:8000/api/nl_query/'; // connect with EC2

  constructor(private http: HttpClient) {}

  // Method to send the natural language query to the Django backend
  processNaturalLanguageQuery(query: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { query });
  }
}