import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chat-container">
      <div class="messages">
        <div *ngFor="let msg of messages" [class.user]="msg.role === 'user'" [class.agent]="msg.role === 'agent'">
          <p>{{ msg.text }}</p>
        </div>
        <div *ngIf="loading" class="agent">Thinking...</div>
      </div>
      <div class="examples" *ngIf="messages.length < 3">
        <button *ngFor="let q of exampleQuestions" (click)="sendMessage(q)" class="chip">{{ q }}</button>
      </div>
      <div class="input-area">
        <input [(ngModel)]="newMessage" (keyup.enter)="sendMessage()" placeholder="Ask WalletGenie...">
        <button (click)="sendMessage()">Send</button>
      </div>
    </div>
  `,
  styles: [`
    .chat-container { display: flex; flex-direction: column; height: 500px; border: 1px solid #ccc; margin: 20px; border-radius: 8px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .messages { flex: 1; overflow-y: auto; padding: 20px; }
    .input-area { display: flex; padding: 10px; border-top: 1px solid #eee; }
    input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
    button { margin-left: 10px; padding: 10px 20px; }
  `]
})
export class ChatComponent {
  messages: { role: string, text: string }[] = [
    { role: 'agent', text: 'Hello! I am WalletGenie. Upload your bank statement and ask me anything about your finances.' }
  ];
  newMessage = '';
  loading = false;
  exampleQuestions = [
    "How much did I spend on Food?",
    "Why can't I save money?",
    "I want to save 5000 in 6 months."
  ];

  constructor(private api: ApiService) { }

  sendMessage(text: string | null = null) {
    const msgText = text || this.newMessage;
    if (!msgText.trim()) return;

    this.messages.push({ role: 'user', text: msgText });
    this.newMessage = '';
    this.loading = true;

    this.api.chat(msgText).subscribe({
      next: (res) => {
        this.messages.push({ role: 'agent', text: res.response });
        this.loading = false;
      },
      error: () => {
        this.messages.push({ role: 'agent', text: 'Sorry, I encountered an error.' });
        this.loading = false;
      }
    });
  }
}
