import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from './material.module';
import { MembersComponent } from './members/members.component';

import { MembersApiService } from './services/members.service';
import { MemberFormComponent } from './members/member-form/member-form.component';
import { MemberDetailComponent } from './members/member-detail/member-detail.component';
import { ConfirmationDialogComponent } from 'src/app/confirmation-dialog/confirmation-dialog.component';
import { ConfirmationDialogService } from './confirmation-dialog/confirmation-dialog.service';
import { AuthService } from './services/auth.service';
import { AuthGuard } from './services/auth-guard.service';
import { ErrorInterceptor } from './services/error-interceptor';
import { JwtInterceptor } from './services/jwt-interceptor';


import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
// import { StatusComponent } from './auth/status/status.component';
// import { LogoutComponent } from './auth/logout/logout.component'

@NgModule({
  declarations: [
    AppComponent,
    MembersComponent,
    MemberFormComponent,
    MemberDetailComponent,
    ConfirmationDialogComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    // StatusComponent,
    // LogoutComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    NgbModule
  ],
  providers: [
    MembersApiService,
    ConfirmationDialogService,
    AuthService,
    AuthGuard,
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true }
  ],
  bootstrap: [AppComponent],
  schemas: [ CUSTOM_ELEMENTS_SCHEMA ]
})

export class AppModule { }
