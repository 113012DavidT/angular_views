import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { AuthService } from '../auth/auth';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss'],
  imports: [
    CommonModule,
    RouterLink
  ]
})
export class Dashboard implements OnInit {

  showMenu = false;

  currentUser: any = {
    username: "administrador"
  };

  sensorData = {
    temperature: 20,
    humidity: 47,
    status: "Conectado"
  };

  menuItems = [
    { label: 'Inicio', icon: 'pi pi-home', routerLink: ['/admin'] },
    { label: 'Configuración', icon: 'pi pi-cog', routerLink: ['/settings'] },
    { separator: true },
    { label: 'Salir', icon: 'pi pi-sign-out' }
  ];

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Obtener usuario actual del servicio de autenticación
    const user = this.authService.getCurrentUser();
    if (user) {
      this.currentUser = user;
    }
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
