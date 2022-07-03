import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { io } from 'socket.io-client';
import { CoursesService } from 'src/app/services/courses.service';
import { SensorType } from 'src/app/types/sensor.enum';

@Component({
  templateUrl: './start.component.html',
  styleUrls: ['./start.component.scss'],
})
export class StartComponent implements OnInit, OnDestroy {
  K_NOM: string | null = '';
  K_ID: string | null = '';
  coureurs: any[] = [];
  isStarted: boolean = false;
  SensorType = SensorType;
  isFinished = false;
  courseId: any = 0;

  url = 'http://51.75.124.195:37591'; // socket.io server

  startDate: number = 0;

  socket = io(this.url, {
    auth: { Username: 'COACH', id: 4 },
    transports: ['websocket'],
  });

  constructor(private route: ActivatedRoute, private service: CoursesService) {}

  ngOnInit(): void {
    this.K_NOM = this.route.snapshot.paramMap.get('K_NOM');
    this.K_ID = this.route.snapshot.paramMap.get('K_ID');

    this.socket.emit('get_connected', {});

    this.socket.on('s_connect', (data: any) => {
      Object.keys(data).forEach((key) => {
        if (!this.coureurs.some((d) => d.sid === data[key].sid)) {
          this.coureurs = [...this.coureurs, data[key]];
        }
      });
    });

    this.socket.on('client_connected', (data: any) => {
      if (this.coureurs.indexOf(data) === -1) {
        this.coureurs = [...this.coureurs, data];
      }
    });

    this.socket.on('client_disconnected', (data: any) => {
      this.coureurs = this.coureurs.filter((c) => c.sid !== data.sid);
    });

    this.socket.on('arrived', (data: any) => {
      console.log(data);
    });

    this.socket.on('end_record', (data: any) => {
      console.log('bite');
    });
  }

  endCourse() {
    let body = {
      F_DEBUT: this.startDate,
      F_FIN: Date.now(),
      K_PISTE: parseInt(this.K_ID as string),
      K_ID: this.courseId,
    };

    this.service.updateCourse(body).subscribe((r) => {
      console.log(r);
    });
    this.socket.emit('race_end', {});
    this.isStarted = false;

    console.table(this.coureurs);
    this.isFinished = true;
  }

  startCourse() {
    let body = {
      F_DEBUT: this.startDate,
      F_FIN: null,
      K_PISTE: this.K_ID,
    };

    this.service.createCourse(body).subscribe((r) => {
      this.startDate = Date.now();
      this.courseId = r;
      this.socket.emit('race_start', { K_ID: r, K_PISTE: this.K_ID });
      this.isStarted = true;
    });
  }

  re() {
    location.reload();
  }

  ngOnDestroy(): void {
    this.socket.disconnect();
  }
}
