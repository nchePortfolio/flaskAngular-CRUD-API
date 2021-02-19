import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/user.model';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {

  user: User = new User('', '', '');

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit(): void {
  }

  onLogin() {
    this.auth.login(this.user).then((response) => {
      if (response.status === "success") {
        localStorage.setItem('token', response.auth_token);

        this.auth.setTheBoolean(true);
        this.auth.getTheBoolean().subscribe( val => {this.auth.isAuth = val});
    
        this.router.navigate(['/alifs/home'])
        }
        console.log(response);
    })
    .catch((err) => {
      console.log(err);
    });
  }

}