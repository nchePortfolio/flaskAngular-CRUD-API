import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from './services/auth.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  emailSubscription: Subscription = new Subscription();
  email: string;

  isAuth: boolean;

  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    this.checkAuthStatus()
    this.auth.getTheBoolean().subscribe(
      (val) => {
        this.isAuth = val;
      });

    this.auth.emitEmailSubject();
    this.emailSubscription = this.auth.emailSubject.subscribe(
      (email: string) => { this.email = email; }
    );
  }

  checkAuthStatus() {

    const token = localStorage.getItem('token');

    if (token) {
      this.auth.ensureAuthenticated(token)
      .then((user) => {
        console.log(user);
        if (user.status === 'success') {
          this.isAuth = true;

          this.auth.email = user.data.username;
          this.auth.emitEmailSubject();

          this.auth.setTheBoolean(true);
          this.auth.getTheBoolean().subscribe(
            (val) => {
              this.isAuth = val;
            }
          );
          return true          
        }
      })
      .catch((err) => {
        console.log(err);
      });
    } else {
      this.isAuth = false;
      return false
    }

  }


}
