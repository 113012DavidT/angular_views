import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, BehaviorSubject } from 'rxjs';
import { switchMap, catchError, tap, startWith, map } from 'rxjs/operators';
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
    this.startPollingLastData();
    // NO hacer polling de todos los datos, solo cargar una vez
  }

  // Polling para último dato cada 3 segundos (más rápido)
  private startPollingLastData(): void {
    interval(3000).pipe(
      startWith(0), // Ejecutar inmediatamente sin esperar 3 segundos
      switchMap(() => this.getLastData()),
      tap(data => {
        if (data) {
          console.log('✅ Last data updated:', data.temp, '°C');
          this.lastDataSubject.next(data);
        }
      }),
      catchError(err => {
        console.warn('⚠️ Error fetching last telemetry, retrying...:', err);
        // Continuar intentando aunque haya error
        return of(null);
      })
    ).subscribe();
  }

  // GET último dato
  getLastData(): Observable<LastTelemetry> {
    return this.http.get<LastTelemetry>(`${this.apiUrl}/last`).pipe(
      catchError(err => {
        console.error('❌ Error in getLastData:', err);
        return of(null as any);
      })
    );
  }

  // GET todos los datos (limitado a 20 registros)
  getAllData(): Observable<TelemetryData[]> {
    return this.http.get<TelemetryData[]>(this.apiUrl).pipe(
      tap(data => {
        // Tomar SOLO los primeros 20 registros
        const limited = data.slice(0, 20);
        console.log('📊 Telemetry data fetched: ' + limited.length + ' records');
        this.allDataSubject.next(limited);
      }),
      map(data => {
        // Retornar solo los primeros 20
        return data.slice(0, 20);
      }),
      catchError(err => {
        console.error('❌ Error in getAllData:', err);
        return of([]);
      })
    );
  }

  // GET contador
  getCount(): Observable<{ total_registros: number }> {
    return this.http.get<{ total_registros: number }>(`${this.apiUrl}/count`).pipe(
      catchError(err => {
        console.error('❌ Error in getCount:', err);
        return of({ total_registros: 0 });
      })
    );
  }
}
