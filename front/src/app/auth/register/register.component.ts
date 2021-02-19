import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/user.model';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})

export class RegisterComponent implements OnInit {

  user: User = new User('', '', '');

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
  }

  onRegister() {
    console.log(this.user);
    this.auth.register(this.user).then((user) => {
      localStorage.setItem('token', user.auth_token);
      this.auth.isAuth = true;
    })
    .catch((err) => {
      console.log(err);
    });
  }

}