import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <h2>Financial Dashboard</h2>
      <div *ngIf="loading">Loading your financial data...</div>
      <div *ngIf="error" class="error">{{ error }}</div>
      <div *ngIf="summary && !loading" class="cards">
        <div class="card">
          <h3>Total Spend</h3>
          <p class="value">\${{ summary.total_spend || 0 }}</p>
        </div>
        <div class="card">
          <h3>Health Score</h3>
          <p class="value" [class.good]="summary.health_score > 70" [class.bad]="summary.health_score < 40">
            {{ summary.health_score || 0 }} / 100
          </p>
        </div>
        <div class="card">
          <h3>Top Categories</h3>
          <ul *ngIf="summary.top_categories && summary.top_categories.length > 0">
            <li *ngFor="let cat of summary.top_categories">
              {{ cat.category }}: \${{ cat.amount }}
            </li>
          </ul>
          <p *ngIf="!summary.top_categories || summary.top_categories.length === 0">No data yet. Upload a CSV to get started!</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard { padding: 20px; }
    h2 { color: #3f51b5; }
    .cards { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px; }
    .card { flex: 1; min-width: 250px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); background: white; }
    .card h3 { margin-top: 0; color: #666; }
    .value { font-size: 2.5em; font-weight: bold; color: #3f51b5; margin: 10px 0; }
    .good { color: green; }
    .bad { color: red; }
    .error { color: red; padding: 10px; background: #fee; border-radius: 4px; }
    ul { list-style: none; padding: 0; }
    li { padding: 5px 0; border-bottom: 1px solid #eee; }
  `]
})
export class DashboardComponent implements OnInit {
  summary: any;
  loading = true;
  error = '';

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.api.getSummary().subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load summary. Please try uploading a CSV first.';
        this.loading = false;
      }
    });
  }
}
