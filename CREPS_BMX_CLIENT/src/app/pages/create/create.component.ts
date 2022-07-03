import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { GoogleMapsModule, MapMarker } from '@angular/google-maps';
import { Router } from '@angular/router';
import { VirtualTimeScheduler } from 'rxjs';
import { CoursesService } from 'src/app/services/courses.service';

enum MarkerType {
  START,
  END
}

@Component({
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss'],
  animations: []
})
export class CreateComponent implements OnInit {
  activeMarker : MarkerType | null = null;
  totalStart : number = 0;
  totalEnd : number = 0;
  markers : any[] = [];
  markerType = MarkerType;
  @ViewChild('input') inputName : ElementRef | null = null;
  K_ID : any = null;

  options: google.maps.MapOptions = {
    center: {lat: 47.267735, lng: -1.585619},
    zoom: 18,
    disableDefaultUI : true,
    mapTypeId: google.maps.MapTypeId.SATELLITE,   
  };


  setMarker(newMarker : MarkerType ) {
    this.activeMarker = newMarker;
  }

  reset(){
    this.totalStart = 0;
    this.totalEnd = 0;
    this.activeMarker = null;
    this.markers = [];
  }

  createMarker(event : any) {
    if((this.activeMarker === MarkerType.END && this.totalEnd >= 2) || (this.activeMarker == MarkerType.START && this.totalStart >= 2) || this.activeMarker === null ) return
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    if(this.activeMarker == MarkerType.END) {
      this.totalEnd ++;
    }else{
      this.totalStart ++;
    }

    this.markers.push({
      type: this.activeMarker,
      position : {
        lat,
        lng,
      },
      label : {
        color: this.activeMarker == MarkerType.END ? 'red' : 'green',
        text: this.activeMarker == MarkerType.END ? 'Arrivée' + this.totalEnd : 'Départ ' + this.totalStart
      },
      title: this.activeMarker == MarkerType.END ? 'Arrivée' + this.totalEnd : 'Départ ' + this.totalStart
    })
  }


  saveCourse() {
    let req : any = {};
    const DEPART = 'F_DEPART';
    const END = 'F_ARRIVEE';
    const LAT = '_LATITUDE';
    const LONG = '_LONGITUDE';

    if(!this.inputName?.nativeElement.value) {
      req['K_NOM'] = `Piste-${Math.round(Math.random() * 100)}`
    }else{
      req['K_NOM'] = this.inputName?.nativeElement.value;
    }

    this.markers.forEach(marker => {
      if(marker.type === MarkerType.START){
        if(marker.title.includes('1')){
          req[`${DEPART}1${LONG}`] = marker.position.lng;
          req[`${DEPART}1${LAT}`] = marker.position.lat;
        }else{
          req[`${DEPART}2${LONG}`] = marker.position.lng;
          req[`${DEPART}2${LAT}`] = marker.position.lat;
        }
      }else{
        if(marker.title.includes('1')){
          req[`${END}1${LONG}`] = marker.position.lng;
          req[`${END}1${LAT}`] = marker.position.lat;
        }else{
          req[`${END}2${LONG}`] = marker.position.lng;
          req[`${END}2${LAT}`] = marker.position.lat;
        }
      }
    })

    const $res = this.service.save(req)
    $res.subscribe(r =>{
      this.K_ID = r;
      this.router.navigate(['/start', {K_ID: this.K_ID, K_NOM : req['K_NOM']}])
    })

  }

  constructor(private service : CoursesService, private router : Router) { }



  ngOnInit(): void {
  }


}
