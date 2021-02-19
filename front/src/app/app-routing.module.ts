import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MembersComponent } from './members/members.component';
import { MemberFormComponent } from './members/member-form/member-form.component'
import { MemberDetailComponent } from './members/member-detail/member-detail.component'
import { HomeComponent } from './home/home.component'
import { LoginComponent } from './auth/login/login.component'
import { RegisterComponent } from './auth/register/register.component'
import { LogoutComponent } from './auth/logout/logout.component'
import { StatusComponent } from './auth/status/status.component'

import { AuthGuard } from './services/auth-guard.service';
import { LoginRedirect } from './services/login-redirect.service';


const routes: Routes = [
  { path: 'alifs/members', canActivate: [AuthGuard], component: MembersComponent },
  { path: 'alifs/members/new', canActivate: [AuthGuard], component: MemberFormComponent },
  { path: 'alifs/members/edit/:id', canActivate: [AuthGuard], component: MemberFormComponent },
  { path: 'alifs/members/detail/:id', canActivate: [AuthGuard], component: MemberDetailComponent },
  { path: 'alifs/home', component: HomeComponent },
  { path: 'alifs/login', component: LoginComponent },
  { path: 'alifs/logout', component: LogoutComponent },
  { path: 'alifs/register', component: RegisterComponent },
  { path: 'alifs/status', component: StatusComponent },
  { path: '', redirectTo: 'alifs/home', pathMatch: 'full' },
  { path: '**', redirectTo: 'alifs/home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
