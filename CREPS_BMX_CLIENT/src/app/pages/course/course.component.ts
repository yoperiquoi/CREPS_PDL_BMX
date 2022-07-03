import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { MarkerType } from 'src/app/types/marker.enum';

@Component({
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.scss'],
})
export class CourseComponent implements OnInit {
  unparsedMarkers: any;

  markers: any[] = [];
  options: google.maps.MapOptions = {}; // pour centrer google map sur les relais

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    let s = this.route.snapshot.paramMap.get('unparsedMarkers');
    if (s) this.unparsedMarkers = JSON.parse(s);
    this.markers = this.parseMarkers();
    this.options = {
      center: {
        lat: parseFloat(
          this.unparsedMarkers['F_DEPART1_LATITUDE'].replace(',', '.')
        ),
        lng: parseFloat(
          this.unparsedMarkers['F_DEPART1_LONGITUDE'].replace(',', '.')
        ),
      },
      zoom: 18,
      disableDefaultUI: true,
      mapTypeId: google.maps.MapTypeId.SATELLITE,
    };
  }

  // lance un course avec la piste active
  start() {
    this.router.navigate([
      '/start',
      {
        K_ID: this.unparsedMarkers['K_ID'],
        K_NOM: this.unparsedMarkers['K_NOM'],
      },
    ]);
  }

  // parse marker in url
  private parseMarkers(): any[] {
    const depart1 = {
      type: MarkerType.START,
      position: {
        lat: parseFloat(
          this.unparsedMarkers['F_DEPART1_LATITUDE'].replace(',', '.')
        ),
        lng: parseFloat(
          this.unparsedMarkers['F_DEPART1_LONGITUDE'].replace(',', '.')
        ),
      },
      label: {
        color: 'green',
        text: 'Départ 1',
      },
      title: 'Départ 1',
    };

    const depart2 = {
      type: MarkerType.START,
      position: {
        lat: parseFloat(
          this.unparsedMarkers['F_DEPART2_LATITUDE'].replace(',', '.')
        ),
        lng: parseFloat(
          this.unparsedMarkers['F_DEPART2_LONGITUDE'].replace(',', '.')
        ),
      },
      label: {
        color: 'green',
        text: 'Départ 2',
      },
      title: 'Départ 2',
    };

    const end1 = {
      type: MarkerType.END,
      position: {
        lat: parseFloat(
          this.unparsedMarkers['F_ARRIVEE1_LATITUDE'].replace(',', '.')
        ),
        lng: parseFloat(
          this.unparsedMarkers['F_ARRIVEE1_LONGITUDE'].replace(',', '.')
        ),
      },
      label: {
        color: 'red',
        text: 'Arrivée 1',
      },
      title: 'Arrivée 1',
    };

    const end2 = {
      type: MarkerType.END,
      position: {
        lat: parseFloat(
          this.unparsedMarkers['F_ARRIVEE2_LATITUDE'].replace(',', '.')
        ),
        lng: parseFloat(
          this.unparsedMarkers['F_ARRIVEE2_LONGITUDE'].replace(',', '.')
        ),
      },
      label: {
        color: 'red',
        text: 'Arrivée 2',
      },
      title: 'Arrivée 2',
    };

    this.markers;

    return [depart1, depart2, end1, end2];
  }
}
