import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { AuthService } from '../auth/auth';
import { TelemetryService, LastTelemetry, TelemetryData } from '../services/telemetry.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

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
export class Dashboard implements OnInit, OnDestroy {

  showMenu = false;

  currentUser: any = {
    username: "administrador"
  };

  sensorData = {
    temperature: 0,
    humidity: 0,
    status: "Desconectado",
    lastUpdate: new Date()
  };

  telemetryHistory: TelemetryData[] = [];
  displayedTelemetry: any[] = [];
  isLoading = true;

  menuItems = [
    { label: 'Inicio', icon: 'pi pi-home', routerLink: ['/admin'] },
    { label: 'Configuración', icon: 'pi pi-cog', routerLink: ['/settings'] },
    { separator: true },
    { label: 'Salir', icon: 'pi pi-sign-out' }
  ];

  private destroy$ = new Subject<void>();

  constructor(
    private authService: AuthService,
    private router: Router,
    private telemetryService: TelemetryService
  ) {}

  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    if (user) {
      this.currentUser = user;
    }

    // Suscribirse a los últimos datos del sensor (auto-actualiza cada 5 segundos)
    this.telemetryService.lastData$
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => {
        if (data) {
          this.sensorData.temperature = data.temp;
          this.sensorData.humidity = data.hum;
          this.sensorData.status = "Conectado";
          this.sensorData.lastUpdate = new Date();
          this.isLoading = false;
          console.log('📊 Last telemetry updated:', data);
        }
      });

    // Cargar histórico de datos UNA SOLA VEZ al iniciar
    this.loadTelemetryHistory();
  }

  private loadTelemetryHistory(): void {
    this.telemetryService.getAllData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => {
        if (data && data.length > 0) {
          this.telemetryHistory = data;
          this.formatDisplayedData();
          console.log('📊 Telemetry history loaded:', data.length, 'records');
        }
      });
  }

  private formatDisplayedData(): void {
    // Los datos ya vienen limitados a 20 del servicio
    this.displayedTelemetry = this.telemetryHistory.map((item, index) => ({
      ...item,
      enviadoPor: this.formatTime(item.timestamp),
      recibidoPor: this.formatTime(item.horaRecepcion),
      guardadoEn: this.formatTime(item.horaGuardado),
      intervalo: item.intervaloSegundos ? `${item.intervaloSegundos}s` : 'N/A',
      intervaloClass: this.getIntervalClass(item.intervaloSegundos)
    }));
  }

  private formatTime(time: string): string {
    if (!time) return 'N/A';
    const date = new Date(time);
    return date.toLocaleString('es-MX', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: 'America/Mexico_City'
    });
  }

  private getIntervalClass(intervalo: number | null): string {
    if (!intervalo) return 'text-gray-500';
    if (intervalo > 120) return 'text-red-500 font-bold'; // Más de 2 minutos
    if (intervalo > 60) return 'text-yellow-500'; // Más de 1 minuto
    return 'text-green-500'; // Normal
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
