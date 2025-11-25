import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="app-container">
      <nav>
        <h1>WalletGenie</h1>
        <div class="links">
          <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
          <a routerLink="/upload" routerLinkActive="active">Upload</a>
          <a routerLink="/chat" routerLinkActive="active">Chat</a>
        </div>
      </nav>
      <main>
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .app-container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    nav { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #3f51b5; color: white; }
    .links a { color: white; text-decoration: none; margin-left: 20px; padding: 5px 10px; border-radius: 4px; }
    .links a.active { background: rgba(255,255,255,0.2); }
    main { padding: 20px; }
  `]
})
export class App {
}
