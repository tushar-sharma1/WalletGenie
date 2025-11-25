import { Routes } from '@angular/router';
import { UploadComponent } from './components/upload/upload';
import { DashboardComponent } from './components/dashboard/dashboard';
import { ChatComponent } from './components/chat/chat';

export const routes: Routes = [
    { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
    { path: 'upload', component: UploadComponent },
    { path: 'dashboard', component: DashboardComponent },
    { path: 'chat', component: ChatComponent }
];
