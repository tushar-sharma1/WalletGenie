import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="upload-container">
      <h2>Upload Bank Statement</h2>
      <input type="file" (change)="onFileSelected($event)" accept=".csv">
      <button (click)="onUpload()" [disabled]="!selectedFile">Upload</button>
      <p *ngIf="message">{{ message }}</p>
    </div>
  `,
  styles: [`
    .upload-container { padding: 20px; border: 1px solid #ccc; border-radius: 8px; max-width: 400px; margin: 20px auto; }
    button { margin-top: 10px; padding: 8px 16px; cursor: pointer; }
  `]
})
export class UploadComponent {
  selectedFile: File | null = null;
  message = '';

  constructor(private api: ApiService) { }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onUpload() {
    if (this.selectedFile) {
      this.message = 'Uploading...';
      this.api.uploadCsv(this.selectedFile).subscribe({
        next: (res) => this.message = `Success: ${res.rows_inserted} transactions inserted.`,
        error: (err) => this.message = `Error: ${err.error?.detail || err.message}`
      });
    }
  }
}
