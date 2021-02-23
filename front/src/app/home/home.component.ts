import { Component } from '@angular/core';

import { User } from 'src/app/models/user.model';
import { AuthService } from 'src/app/services/auth.service';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {
    user: User;

    constructor(private authService: AuthService) {
        this.user = this.authService.currentUserValue;
        console.log('From home:', this.user)
    }
}