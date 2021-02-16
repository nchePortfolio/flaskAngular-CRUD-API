import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Member } from '../../models/member.model';
import { MembersApiService } from '../../services/members.service';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-member-form',
  templateUrl: './member-form.component.html',
  styleUrls: ['./member-form.component.css']
})

export class MemberFormComponent implements OnInit {

  memberForm: FormGroup;

  isAddMode: boolean;
  id: string;

  member: Member;

  constructor(
    private formBuilder: FormBuilder,
    private membersService: MembersApiService,
    private router: Router,
    private route: ActivatedRoute,
    ) { }
 
  ngOnInit() {
    this.id = this.route.snapshot.params['id'];
    this.isAddMode = !this.id;
    
    this.memberForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
    });

    if (!this.isAddMode) {
        this.membersService.getMemberById(this.id)
            .subscribe(
              (x) => {
                this.memberForm.patchValue(x['member']);
                console.log(x['member'])
              }
            );
    }
  }

  onAddMember() {
    const newMember = new Member(0,
      this.memberForm.get('first_name').value,
      this.memberForm.get('last_name').value
      );

    if (!this.isAddMode) {
      this.membersService.updateMember(this.id, this.memberForm.value)
    } else {
      this.membersService.addMember(newMember)
    }

    this.router.navigate(['/alifs/members']);
  }  

}


