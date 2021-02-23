import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AuthService } from 'src/app/services/auth.service';

@Component({ templateUrl: 'login.component.html', styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
    form: FormGroup;
    loading = false;
    submitted = false;
    is_password_invalid = false;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authService: AuthService,
    ) { }

    ngOnInit() {
        this.form = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
        });
    }

    // convenience getter for easy access to form fields
    get f() { return this.form.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.form.invalid) {
            return;
        }

        this.loading = true;
        this.authService.login(this.f.username.value, this.f.password.value)
            .pipe(first())
            .subscribe({
                next: (response) => {
                    if (response.status === 'fail') {
                        console.log('from login next', response)
                        this.is_password_invalid = true;
                        this.loading = false;
                        this.f.password.setValue('');
                    }
                    // get return url from query parameters or default to home page
                    const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
                    this.router.navigateByUrl(returnUrl);
                },
                error: error => {
                    console.log('from login:', error)
                    this.loading = false;
                }
            });
    }
}