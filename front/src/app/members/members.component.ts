import { Component, OnInit, OnDestroy, AfterViewInit, ViewChild } from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import { Router } from '@angular/router';

import { MembersApiService } from '../services/members.service';
import { ConfirmationDialogService } from 'src/app/confirmation-dialog/confirmation-dialog.service';
import { Member } from '../models/member.model';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';


@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.css']
})

export class MembersComponent implements OnInit, OnDestroy, AfterViewInit {

  title = 'alifs-app';

  membersSubscription: Subscription = new Subscription();  
  members: Member[];
  dataSource: MatTableDataSource<Member>;

  displayedColumns: string[] = ['id', 'first_name', 'last_name', 'actions'];

  private isFetched: boolean = false;


  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;

  ngAfterViewInit() {
    // setTimeout(() => this.dataSource.paginator = this.paginator);
    console.log(this.paginator)
  }

  constructor(
    private membersApi: MembersApiService,
    private router: Router,
    private confirmationDialogService: ConfirmationDialogService
    ) { }

  ngOnInit() {
    this.membersSubscription = this.membersApi.membersSubject.subscribe(
      (members: any[]) => {
        this.members = members;
        this.dataSource = new MatTableDataSource<Member>(members);
        this.dataSource.paginator = this.paginator;
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

