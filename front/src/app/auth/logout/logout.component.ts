import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})

export class LogoutComponent implements OnInit {

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit(): void {
    const token = localStorage.getItem('token');
    
    if (token) {
      this.auth.logout(token).then((user) => {
        console.log(user);
        if (user.status === 'success') {
          localStorage.clear();
          setTimeout(() => {
            this.router.navigate(['/alifs/home']);
            this.auth.setTheBoolean(false);
            this.auth.getTheBoolean().subscribe( val => {this.auth.isAuth = val});  
          }, 2000);

        }
      })
      .catch((err) => {
        console.log(err);
      });
    } else {
      setTimeout(() => {
        this.router.navigate(['/alifs/home']);
        this.auth.setTheBoolean(false);
        this.auth.getTheBoolean().subscribe( val => {this.auth.isAuth = val});  
      }, 2000);

    }
  }

}
