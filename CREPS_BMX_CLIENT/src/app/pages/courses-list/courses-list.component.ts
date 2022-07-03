import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { timeout } from 'rxjs';
import { CoursesService } from 'src/app/services/courses.service';

@Component({
  templateUrl: './courses-list.component.html',
  styleUrls: ['./courses-list.component.scss'],
})
export class CoursesListComponent implements OnInit {
  constructor(private router: Router, private service: CoursesService) {}
  data: any = [];
  isDeleting: boolean = false;

  ngOnInit(): void {
    // retourne les courses existantes
    this.service.getAll().subscribe((d: any) => {
      const { res } = d;
      this.data = res;
    });
  }

  // navigation vers une course, si on est en mode suppression alors on supprime la course
  async goTo(index: number, K_ID: number) {
    if (this.isDeleting) {
      this.deleteCourse(K_ID);
    } else {
      this.router.navigate([
        '/course',
        { unparsedMarkers: JSON.stringify(this.data[index]) },
      ]);
    }
  }

  deleteCourse(K_ID: number) {
    this.service.deleteOne(K_ID).subscribe((d) => {
      this.service.getAll().subscribe((d: any) => {
        const { res } = d;
        this.data = res;
      });
    });
    this.isDeleting = false;
  }
}
