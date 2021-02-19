import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service'


@Injectable()
export class AuthGuard implements CanActivate {
  is_auth: boolean;

  constructor(private router: Router, private auth: AuthService) { }

  canActivate(): boolean {
    const token = localStorage.getItem('token');
    console.log('token', token);
    if (token) {
      this.auth.ensureAuthenticated(token).then(
        (user): boolean => {
          if (user.status === 'success') {
            console.log(true);
            return true
            }
          else {
            console.log(false);
            this.router.navigate(['/alifs/login']);
            return false
          }
        }
      )
      .catch((err) => {
        console.log(err);
      });
      return true
    }
    else {
      this.router.navigate(['/alifs/login']);
      console.log(false);
      return false
    }
  }
}

