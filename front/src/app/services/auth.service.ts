import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { User } from '../models/user.model';


import 'rxjs/add/operator/toPromise';

import {API_URL} from 'src/app/env';
import { Subject } from 'rxjs/Subject';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';
import { Observable } from 'rxjs/Observable';


@Injectable()
export class AuthService {

  private headers = new HttpHeaders().set('content-type', 'application/json');

  emailSubject = new Subject<string>();
  email: string;

  public isAuth: boolean;
  private theBoolean: BehaviorSubject<boolean>;

  constructor(private http: HttpClient) {
      this.theBoolean = new BehaviorSubject<boolean>(false);
    }  

  public getTheBoolean(): Observable<boolean> {
      return this.theBoolean.asObservable();
  }

  public setTheBoolean(newValue: boolean): void {
    this.theBoolean.next(newValue);
  }

  emitEmailSubject() {
    this.emailSubject.next(this.email)
  }

  login(user): Promise<any> {
    return this.http.post(`${API_URL}/auth/login`, user, { 'headers': this.headers }).toPromise();
  }

  register(user: User): Promise<any> {
    return this.http.post(`${API_URL}/auth/register`, user, { 'headers': this.headers }).toPromise();
  }

  logout(token): Promise<any> {
    let headers= new HttpHeaders()
    .set('content-type', 'application/json')
    .set('Authorization', `Bearer ${token}`);

    return this.http.get(`${API_URL}/auth/logout`, {headers: headers}).toPromise();
  }

  ensureAuthenticated(token): Promise<any> {
    let headers= new HttpHeaders()
    .set('content-type', 'application/json')
    .set('Authorization', `Bearer ${token}`);

    return this.http.get(`${API_URL}/auth/status`, {headers: headers}).toPromise();
  }
  

}
