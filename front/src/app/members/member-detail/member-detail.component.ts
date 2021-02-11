import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import {MembersApiService} from '../../services/members.service';
import { Member} from '../../models/member.model'

@Component({
  selector: 'app-member-detail',
  templateUrl: './member-detail.component.html',
  styleUrls: ['./member-detail.component.css']
})
export class MemberDetailComponent implements OnInit {

  member: Member;

  constructor(
    private route: ActivatedRoute,
    private membersService: MembersApiService,
    private router: Router
  ) { }

  ngOnInit() {
    this.member = new Member(0, '', '');
    const id = this.route.snapshot.params['id'];

    this.membersService.getMemberById(+id).subscribe(
      (response) => {
        this.member = response['member'][0];
        console.log(this.member);
      },
      (error) => {
        console.log('Erreur ! : ' + error);
      }
    );

  }

  onBack() {
    this.router.navigate(['/alifs/members']);
  }
}
