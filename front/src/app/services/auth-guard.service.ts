import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service'


@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private router: Router, private auth: AuthService) {}

  canActivate(): boolean {
    if (localStorage.getItem('token')) {
      this.auth.isAuth = true;
      return true;
    }
    else {
      this.router.navigate(['/alifs/login']);
      return false;
    }
  }
}
