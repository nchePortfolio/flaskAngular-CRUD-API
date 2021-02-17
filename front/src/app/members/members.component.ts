import { Component, OnInit, OnDestroy } from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import { Router } from '@angular/router';

import { MembersApiService } from '../services/members.service';
import { ConfirmationDialogService } from 'src/app/confirmation-dialog/confirmation-dialog.service';


@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.css']
})

export class MembersComponent implements OnInit, OnDestroy {

  title = 'alifs-app';
  membersSubscription: Subscription = new Subscription();  
  members: any[];
  private isFetched: boolean = false;

  constructor(
    private membersApi: MembersApiService,
    private router: Router,
    private confirmationDialogService: ConfirmationDialogService
    ) { }

  ngOnInit() {
    this.membersSubscription = this.membersApi.membersSubject.subscribe(
      (members: any[]) => {
        this.members = members;
      }
    );
    this.membersApi.emitMemberSubject();
    if (this.isFetched === false) {
      this.onFetch();
      this.isFetched = true;
      }
    }

  ngOnDestroy() {
    this.membersSubscription.unsubscribe();
  }

  onFetch() {
    this.membersApi.getMembers();
  }
  
  onDetailMember(member_id) {
    this.router.navigate(['/alifs/members', 'detail', member_id]);
  }

  onNewMember() {
    this.router.navigate(['/alifs/members', 'new']);
  }

  onUpdateMember(member_id) {
    this.router.navigate(['/alifs/members', 'edit', member_id]);
  }

  // onDeleteMember(member_id) {
  //   this.membersApi.deleteMember(member_id);
  // }


  onDeleteMember(member_id) {
    var member = this.getMemberById(member_id);

    this.confirmationDialogService.confirm('Veuillez confirmer', `Voulez-vous vraiment supprimer ${member.first_name} ${member.last_name}`)
    .then((confirmed) => {
      if (confirmed) {
        this.membersApi.deleteMember(member_id);
      }
    })
    .catch(() => console.log('User dismissed the dialog (e.g., by using ESC, clicking the cross icon, or clicking outside the dialog)'));
  }

  getMemberById(id){
    var element = this.members.filter(x => x.id === id);
    return element[0];
  }

}

