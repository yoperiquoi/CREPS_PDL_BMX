import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class CoursesService {
  constructor(private http: HttpClient) {}

  url = 'http://127.0.0.1:5000/'; // API url

  getAll() {
    return this.http.get(this.url + 'piste', { responseType: 'json' });
  }

  deleteOne(k_id: number) {
    return this.http.delete(this.url + 'piste/' + k_id);
  }

  save(body: any) {
    return this.http.post(this.url + 'piste', body);
  }

  createCourse(body: any) {
    return this.http.post(this.url + 'course', body);
  }

  updateCourse(body: any) {
    return this.http.put(this.url + 'course', body);
  }
}
