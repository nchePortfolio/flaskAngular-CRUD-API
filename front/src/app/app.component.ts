import { Component } from '@angular/core';
import { AuthService } from './services/auth.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  isAuth: boolean;
  email: string;

  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    this.checkAuthStatus()
    this.auth.getTheBoolean().subscribe(
      (val) => {
        this.isAuth = val;
      });
}

  checkAuthStatus() {

    const token = localStorage.getItem('token');

    if (token) {
      this.auth.ensureAuthenticated(token)
      .then((user) => {
        console.log(user);
        if (user.status === 'success') {
          this.isAuth = true;
          this.email = user.data.email;
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
