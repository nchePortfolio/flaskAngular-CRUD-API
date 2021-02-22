import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';import { AuthService } from './auth.service'


@Injectable()
export class AuthGuard implements CanActivate {
  is_auth: boolean;

  constructor(private router: Router, private auth: AuthService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const token = localStorage.getItem('token');

    if (token) {
      this.auth.ensureAuthenticated(token).then(
        (user): boolean => {
          if (user.status === 'success') {
            return true
            }
          else {
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

