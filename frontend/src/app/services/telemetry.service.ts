import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, BehaviorSubject } from 'rxjs';
import { switchMap, catchError, tap } from 'rxjs/operators';
import { of } from 'rxjs';

export interface TelemetryData {
  _id: string;
  temp: number;
  hum: number;
  intervaloSegundos: number | null;
  timestamp: string;
  horaRecepcion: string;
  horaGuardado: string;
  createdAt: string;
  updatedAt: string;
}

export interface LastTelemetry {
  id: string;
  temp: number;
  hum: number;
  intervaloSegundos: number | null;
  enviado_por_esp: {
    utc: string;
    mexico_utc_6: string;
  };
  recibido_por_backend: {
    utc: string;
    mexico_utc_6: string;
  };
  guardado_en_mongo: {
    utc: string;
    mexico_utc_6: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class TelemetryService {
  private apiUrl = 'https://esp32-server-9ip3.onrender.com/api/telemetry';
  
  private lastDataSubject = new BehaviorSubject<LastTelemetry | null>(null);
  public lastData$ = this.lastDataSubject.asObservable();
  
  private allDataSubject = new BehaviorSubject<TelemetryData[]>([]);
  public allData$ = this.allDataSubject.asObservable();

  constructor(private http: HttpClient) {
    this.startPolling();
  }

  // Obtener último dato cada 5 segundos
  private startPolling(): void {
    interval(5000).pipe(
      switchMap(() => this.getLastData()),
      catchError(err => {
        console.error('Error fetching telemetry:', err);
        return of(null);
      })
    ).subscribe(data => {
      if (data) {
        this.lastDataSubject.next(data);
      }
    });
  }

  // GET últimdato
  getLastData(): Observable<LastTelemetry> {
    return this.http.get<LastTelemetry>(`${this.apiUrl}/last`).pipe(
      catchError(err => {
        console.error('Error:', err);
        return of(null as any);
      })
    );
  }

  // GET todos los datos
  getAllData(): Observable<TelemetryData[]> {
    return this.http.get<TelemetryData[]>(this.apiUrl).pipe(
      tap(data => this.allDataSubject.next(data)),
      catchError(err => {
        console.error('Error:', err);
        return of([]);
      })
    );
  }

  // GET contador
  getCount(): Observable<{ total_registros: number }> {
    return this.http.get<{ total_registros: number }>(`${this.apiUrl}/count`).pipe(
      catchError(err => {
        console.error('Error:', err);
        return of({ total_registros: 0 });
      })
    );
  }
}
