import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MembersComponent } from './members/members.component';
import { MemberFormComponent } from './members/member-form/member-form.component'
import { MemberDetailComponent } from './members/member-detail/member-detail.component'
import { HomeComponent } from './home/home.component'

const routes: Routes = [
  { path: 'alifs/members', component: MembersComponent },
  { path: 'alifs/members/new', component: MemberFormComponent },
  { path: 'alifs/members/edit/:id', component: MemberFormComponent },
  { path: 'alifs/members/detail/:id', component: MemberDetailComponent },
  { path: 'alifs/home', component: HomeComponent },
  { path: '', redirectTo: 'alifs/home', pathMatch: 'full' },
  { path: '**', redirectTo: 'alifs/home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
