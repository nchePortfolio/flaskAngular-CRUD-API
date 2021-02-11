import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MembersComponent } from './members/members.component';
import { MemberFormComponent } from './members/member-form/member-form.component'
import { MemberDetailComponent } from './members/member-detail/member-detail.component'

const routes: Routes = [
  { path: 'alifs/members', component: MembersComponent },
  { path: 'alifs/members/new', component: MemberFormComponent },
  { path: 'alifs/members/edit/:id', component: MemberFormComponent },
  { path: 'alifs/members/detail/:id', component: MemberDetailComponent },
  { path: '', redirectTo: 'alifs/members', pathMatch: 'full' },
  { path: '**', redirectTo: 'alifs/members' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
