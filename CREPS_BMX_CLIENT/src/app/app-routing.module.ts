import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CourseComponent } from './pages/course/course.component';
import { CoursesListComponent } from './pages/courses-list/courses-list.component';
import { CreateComponent } from './pages/create/create.component';
import { StartComponent } from './pages/start/start.component';

const routes: Routes = [
  {path: 'courses', component: CoursesListComponent}, 
  {path: 'cree', component: CreateComponent},
  {path: 'course', component:CourseComponent},
  {path: 'start', component: StartComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
