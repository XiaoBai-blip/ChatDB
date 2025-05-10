import { Component } from '@angular/core';
import { ApiService } from './api.service';  // Import the ApiService
import { FormsModule } from '@angular/forms';
import { NgForOf } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, NgForOf, HttpClientModule],
  template: `
    <div class="container">
      <h1>QueryPal</h1>
      <div class="team-names">
        <span *ngFor="let name of teamNames">{{ name }}</span>
      </div>

      <div class="query-section">
        <input
          type="text"
          [(ngModel)]="queryInput"
          placeholder="Please enter your questions here"
          (keyup.enter)="submitQuery()"
        />
        <button (click)="submitQuery()">Submit</button>
      </div>

      <div class="results-section">
        <h2>Results</h2>
        <div class="results-content">{{ results }}</div>
      </div>

      <div class="history-section">
        <h2>Query History</h2>
        <div class="history-list">
          <div *ngFor="let query of queryHistory" class="history-item">
            {{ query }}
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    body {
      background: #fef6ef;
      font-family: 'Segoe UI', sans-serif;
    }
    .team-names {
      position: fixed;
      top: 1.5rem;
      right: 1.5rem;
      background-color: #ffffff;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      font-size: 0.9rem;
      color: #6c757d;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      font-weight: 600;
      display: flex;
      gap: 1rem;
      z-index: 1000;
    }

    .container {
      max-width: 800px;
      margin: 3rem auto;
      padding: 2rem;
      background: linear-gradient(to right top, #fef6ef, #f2f7fd);
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    }

    h1 {
      text-align: center;
      font-size: 2.5rem;
      font-weight: bold;
      color: #1d3557;
      margin-bottom: 2rem;
    }

    .query-section {
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
    }

    input {
      flex: 1;
      padding: 0.9rem 1rem;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-size: 1rem;
      background: #fff;
    }

    button {
      padding: 0.9rem 1.5rem;
      background-color: #1d75f8;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }

    button:hover {
      background-color: #0056d2;
    }

    .results-section, .history-section {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
      position: relative;
    }

    .results-section::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      width: 6px;
      background-color: #36d399;
      border-top-left-radius: 12px;
      border-bottom-left-radius: 12px;
    }

    h2 {
      margin-top: 0;
      margin-bottom: 1rem;
      font-size: 1.4rem;
      color: #1d3557;
    }

    .results-content {
      background: #f9fdff;
      border-radius: 10px;
      padding: 1rem;
      min-height: 200px;
      font-family: monospace;
      white-space: pre-wrap;
      color: #333;
    }

    .history-list {
      margin-top: 0.5rem;
    }

    .history-item {
      padding: 0.75rem;
      border-bottom: 1px solid #eee;
      font-size: 0.95rem;
      color: #444;
    }

    .history-item:last-child {
      border-bottom: none;
    }
  `]
})

export class AppComponent {
  queryInput = '';
  teamNames = ['Xiao Bai', 'Jingwen Xu', 'Xuanchen Ren'];
  results = '';
  queryHistory: string[] = [];

  constructor(private apiService: ApiService) {}

  submitQuery() {
    if (this.queryInput.trim()) {
      this.apiService.processNaturalLanguageQuery(this.queryInput).subscribe({
        next: (response: any) => {
          console.log('🔍 Full API response:', response);
  
          // Safely handle query output
          const queryContent = typeof response.query === 'string'
            ? response.query
            : response.query?.content || JSON.stringify(response.query, null, 2);
  
          // Handle result smartly
          const rawResult = response.result?.content || response.result || {};
          let resultContent = 'No result found 🫥';
  
          // Format based on type
          if (rawResult?.status === 'success') {
            resultContent = '✅ Success! Your action was completed.';
          } else if (Array.isArray(rawResult) && rawResult.length > 0) {
            resultContent = JSON.stringify(rawResult, null, 2);
          } else if (typeof rawResult === 'string') {
            resultContent = rawResult;
          } else if (typeof rawResult === 'object' && Object.keys(rawResult).length > 0) {
            resultContent = JSON.stringify(rawResult, null, 2);
          }
  
          // 🎨 Final formatted result
          this.results =
            "😁 Got it! Here's the query you requested:\n\n" + queryContent + "\n\n" +
            "🤪 Let's see the result:\n\n" + resultContent;
  
          // Store and reset
          this.queryHistory.unshift(this.queryInput);
          this.queryInput = '';
        },
        error: (error) => {
          console.error('❌ API Error:', error);
          this.results = '😭 Sorry! We couldn’t process your question. Please try rephrasing it.';
        }
      });
    }
  }
}
