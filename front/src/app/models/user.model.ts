export class User {
    id: number;
    username: string;
    password: string;
    email: string;
    isAdmin: boolean;
    registeredOn: Date;
    token?: string;
}