import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Subject} from 'rxjs/Subject';
import {API_URL} from 'src/app/env';
import { Member } from '../models/member.model';
import { Observable } from 'rxjs';
import { first } from 'rxjs/operators';



@Injectable()
export class MembersApiService {

  membersSubject = new Subject<any[]>();
  members: Member[];

  constructor(private http: HttpClient) {
  }

  emitMemberSubject() {
    this.membersSubject.next(this.members);
  }

  getMembers() {
    this.http
      .get<Member[]>(`${API_URL}/member/all`)
      .subscribe(
        (response) => {
          this.members = response;
          this.emitMemberSubject();
        },
        (error) => {
          console.log('Erreur ! : ' + error);
        }
      );
  }

  getMemberById(memberId) {
    return this.http.get(`${API_URL}/member/${memberId}`)
  }

  addMember(newMember: Member) {
    const memberObject = {
      first_name: '',
      id: 0,
      last_name: ''
    };

    memberObject.first_name = newMember.first_name;
    memberObject.last_name = newMember.last_name;
    memberObject.id = this.members[(this.members.length - 1)].id + 1;
   
    this.saveMember(memberObject)
    this.members.push(memberObject);
    this.emitMemberSubject();
  }
  

  updateMember(id, member) {
    this.http.put(`${API_URL}/member/update/${id}`, member, {responseType: 'text'})
      .subscribe(
        () => {
          console.log('Mise à jour réussi !');
        },
        (error) => {
          console.log('Erreur ! : ' + error);
        }
      );
  }


  saveMember(member) {
    this.http
      .post(`${API_URL}/member/add`, member, {responseType: 'text'})
      .subscribe(
        () => {
          console.log('Enregistrement réussi !');
        },
        (error) => {
          console.log(`Erreur ! : ${error.message}`);
        }
      );
  }

  deleteMember(member_id: number) {
    this.http
      .delete(`${API_URL}/member/delete/${member_id}`, {responseType: 'text'})
      .subscribe(
        () => {
          console.log('Suppression réussie !');
        },
        (error) => {
          console.log(`Erreur ! : ${error.message}`);
        }
      );

    const memberIndexToRemove = this.members.findIndex(
      (memberEl) => {
        if(memberEl.id == member_id) {
          return true;
        }
      }
    );

    this.members.splice(memberIndexToRemove, 1);
    this.emitMemberSubject();  
  } 


}